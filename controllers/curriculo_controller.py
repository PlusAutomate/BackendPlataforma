import os
import io
import uuid
import re
import json
import boto3
import fitz  # PyMuPDF
from flask import Blueprint, jsonify, request
from werkzeug.utils import secure_filename
from models import Curriculo, db

curriculo_bp = Blueprint("curriculo", __name__, url_prefix="/curriculos")

UPLOAD_FOLDER = "uploads"
S3_BUCKET = os.environ.get("S3_BUCKET", "my-bucket")

# ---------------------
# Lista de possíveis nomes para cada seção
SECOES = {
    "formacao": ["Formação", "Educação", "Acadêmico", "Estudos"],
    "experiencia": ["Experiência", "Histórico Profissional", "Carreira", "Trabalho"],
    "skills": ["Skills", "Competências", "Habilidades", "Conhecimentos"]
}


def buscar_secao(texto, palavras_chave, proximas_secoes):
    """Encontra uma seção do currículo com base em palavras-chave e delimitadores"""
    padrao = r'(' + "|".join(map(re.escape, palavras_chave)) + r').*?(' + "|".join(map(re.escape, proximas_secoes)) + r'|$)'
    return re.search(padrao, texto, re.S | re.I)


def extrair_nome(linhas):
    """Extrai o nome evitando links, emails, telefones, cidades, estados e anos"""
    for l in linhas[:10]:  # só as 10 primeiras linhas
        linha = l.strip()
        if not linha:
            continue
        # ignora links, emails, números, anos e siglas de estado
        if (re.search(r'http|www|linkedin|github|@', linha, re.I) or
            re.fullmatch(r'[\d\-\(\)\s]+', linha) or
            re.search(r'\b\d{4}\b', linha) or
            re.search(r'\bSP|RJ|MG|RS|SC|PR|BA|PE|CE\b', linha)):
            continue
        palavras = linha.split()
        # 2 a 4 palavras com iniciais maiúsculas
        if 2 <= len(palavras) <= 4 and all(p[0].isupper() for p in palavras if p[0].isalpha()):
            return linha
    # fallback: primeira linha válida sem links, emails, números ou anos
    for l in linhas[:10]:
        linha = l.strip()
        if (linha and not re.search(r'http|www|linkedin|github|@', linha, re.I) and
            not re.fullmatch(r'[\d\-\(\)\s]+', linha) and
            not re.search(r'\b\d{4}\b', linha) and
            not re.search(r'\bSP|RJ|MG|RS|SC|PR|BA|PE|CE\b', linha)):
            return linha
    return None


def analisar_curriculo(texto):
    """Extrai informações estruturadas de um currículo"""
    dados = {
        "dados_pessoais": {
            "nome": None,
            "email": None,
            "telefone": None,
            "linkedin": None
        },
        "formacao": [],
        "experiencia": [],
        "skills": []
    }

    linhas = [l.strip() for l in texto.splitlines() if l.strip()]

    # Nome
    dados["dados_pessoais"]["nome"] = extrair_nome(linhas)

    # Email
    email = re.search(r'[\w\.-]+@[\w\.-]+', texto)
    if email:
        dados["dados_pessoais"]["email"] = email.group(0)

    # Telefone (padrão BR)
    telefone = re.search(r'(\(?\d{2}\)?\s)?(\d{4,5}-?\d{4})', texto)
    if telefone:
        dados["dados_pessoais"]["telefone"] = telefone.group(0)

    # LinkedIn
    linkedin = re.search(r'(https?://(www\.)?linkedin\.com/in/[^\s]+)', texto)
    if linkedin:
        dados["dados_pessoais"]["linkedin"] = linkedin.group(0)

    # Formação Acadêmica
    formacao = buscar_secao(
        texto,
        SECOES["formacao"],
        SECOES["experiencia"] + SECOES["skills"]
    )
    if formacao:
        for linha in formacao.group(0).split("\n"):
            if linha.strip() and not re.search("|".join(map(re.escape, SECOES["formacao"] + SECOES["experiencia"] + SECOES["skills"])), linha, re.I):
                dados["formacao"].append(linha.strip())

    # Experiência Profissional
    experiencia = buscar_secao(
        texto,
        SECOES["experiencia"],
        SECOES["formacao"] + SECOES["skills"]
    )
    if experiencia:
        for linha in experiencia.group(0).split("\n"):
            if linha.strip() and not re.search("|".join(map(re.escape, SECOES["formacao"] + SECOES["experiencia"] + SECOES["skills"])), linha, re.I):
                dados["experiencia"].append(linha.strip())

    # Skills / Competências
    skills = buscar_secao(
        texto,
        SECOES["skills"],
        SECOES["formacao"] + SECOES["experiencia"]
    )
    if skills:
        for linha in skills.group(0).split("\n"):
            if linha.strip() and not re.search("|".join(map(re.escape, SECOES["formacao"] + SECOES["experiencia"] + SECOES["skills"])), linha, re.I):
                dados["skills"].append(linha.strip())

    return dados


@curriculo_bp.route("/upload", methods=["POST"])
def upload_curriculo():
    if "file" not in request.files:
        return jsonify({"erro": "Nenhum arquivo enviado"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"erro": "Nome de arquivo inválido"}), 400

    filename = secure_filename(file.filename)

    # lê bytes do arquivo em memória
    file_bytes = file.read()

    # extrai texto do PDF (em memória)
    try:
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        texto = ""
        for pagina in doc:
            texto += pagina.get_text()
        doc.close()
    except Exception as e:
        return jsonify({"erro": "Erro ao ler PDF: %s" % str(e)}), 400

    # analisa o currículo
    dados_extraidos = analisar_curriculo(texto)

    # envia para S3
    s3 = boto3.client('s3')
    key = f"curriculos/{uuid.uuid4().hex}_{filename}"
    try:
        s3.upload_fileobj(io.BytesIO(file_bytes), S3_BUCKET, key, ExtraArgs={'ContentType': file.content_type or 'application/pdf'})
    except Exception as e:
        return jsonify({"erro": "Falha ao enviar para S3: %s" % str(e)}), 500

    s3_url = f"https://{S3_BUCKET}.s3.amazonaws.com/{key}"

    # salva caminho S3 no banco
    curriculo = Curriculo(caminho=s3_url)
    db.session.add(curriculo)
    db.session.commit()

    return jsonify({
        "mensagem": "Currículo enviado com sucesso!",
        "id": curriculo.id_curriculo,
        "s3_url": s3_url,
        "dados_extraidos": dados_extraidos
    }), 201


@curriculo_bp.route("", methods=["GET"])
def listar_curriculos():
    curriculos = Curriculo.query.all()
    return jsonify([{
        "id_curriculo": c.id_curriculo,
        "caminho": c.caminho
    } for c in curriculos])


@curriculo_bp.route("/<int:id>", methods=["DELETE"])
def excluir_curriculo(id):
    c = Curriculo.query.get_or_404(id)

    # se for arquivo local, remove do disco
    if isinstance(c.caminho, str) and c.caminho.startswith(UPLOAD_FOLDER) and os.path.exists(c.caminho):
        os.remove(c.caminho)
    else:
        # tenta remover do S3 se parecer ser uma URL do bucket configurado
        prefix = f"https://{S3_BUCKET}.s3.amazonaws.com/"
        if isinstance(c.caminho, str) and c.caminho.startswith(prefix):
            key = c.caminho[len(prefix):]
            try:
                s3 = boto3.client('s3')
                s3.delete_object(Bucket=S3_BUCKET, Key=key)
            except Exception:
                pass

    db.session.delete(c)
    db.session.commit()
    return jsonify({"mensagem": "Currículo excluído com sucesso!"})
