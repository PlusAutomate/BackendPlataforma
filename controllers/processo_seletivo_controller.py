from flask import Blueprint, jsonify, request
from models import ProcessoSeletivo, db, Vaga, Candidato, Curriculo

processo_bp = Blueprint("processo", __name__, url_prefix="/processo-seletivo")


# =========================
# Criar novo processo seletivo
# =========================
@processo_bp.route("", methods=["POST"])
def criar_processo_seletivo():
    dados = request.json
    id_vaga = dados.get("id_vaga")
    id_candidato = dados.get("id_candidato")

    vaga = Vaga.query.get(id_vaga)
    candidato = Candidato.query.get(id_candidato)
    if not vaga or not candidato:
        return jsonify({"erro": "Vaga ou candidato não encontrados"}), 404

    processo = ProcessoSeletivo(
        id_vaga=id_vaga,
        id_candidato=id_candidato
    )

    db.session.add(processo)
    db.session.commit()

    return jsonify({
        "mensagem": "Processo seletivo criado com sucesso!",
        "id_vaga": processo.id_vaga,
        "id_candidato": processo.id_candidato
    }), 201


# =========================
# Listar candidatos por vaga (com currículo)
# =========================
@processo_bp.route("/vaga/<int:id_vaga>", methods=["GET"])
def listar_candidatos_por_vaga(id_vaga):
    processos = ProcessoSeletivo.query.filter_by(id_vaga=id_vaga).all()
    if not processos:
        return jsonify([]), 200

    vaga = Vaga.query.get(id_vaga)
    resultado = []

    for p in processos:
        candidato = Candidato.query.get(p.id_candidato)
        if candidato:
            # busca o currículo relacionado, se houver
            curriculo = Curriculo.query.get(candidato.id_curriculo)
            resultado.append({
                "id_candidato": candidato.id_candidato,
                "nome": candidato.nome,
                "email": candidato.email,
                "telefone": candidato.telefone,
                "status": p.status,
                "vaga": vaga.titulo if vaga else None,
                "id_vaga": id_vaga,
                "curriculo": curriculo.caminho if curriculo else None
            })

    return jsonify(resultado), 200


# =========================
# Listar todos os processos
# =========================
@processo_bp.route("", methods=["GET"])
def listar_processos():
    processos = ProcessoSeletivo.query.all()

    resultado = []
    for p in processos:
        vaga = p.vaga  # relacionamento
        candidato = p.candidato  # relacionamento

        resultado.append({
            "id_vaga": p.id_vaga,
            "titulo_vaga": vaga.titulo if vaga else None,
            "id_candidato": p.id_candidato,
            "nome": candidato.nome if candidato else None,
            "email": candidato.email if candidato else None,
            "status": p.status,
            "data_criacao": p.data_criacao.strftime("%Y-%m-%d %H:%M:%S"),
            "data_atualizacao": p.data_atualizacao.strftime("%Y-%m-%d %H:%M:%S")
        })

    return jsonify(resultado)


# =========================
# Excluir processo seletivo
# =========================
@processo_bp.route("", methods=["DELETE"])
def excluir_processo_seletivo():
    dados = request.json
    id_vaga = dados.get("id_vaga")
    id_candidato = dados.get("id_candidato")

    if not id_vaga or not id_candidato:
        return jsonify({"erro": "Informe id_vaga e id_candidato"}), 400

    processo = ProcessoSeletivo.query.filter_by(
        id_vaga=id_vaga,
        id_candidato=id_candidato
    ).first()

    if not processo:
        return jsonify({"erro": "Registro não encontrado"}), 404

    db.session.delete(processo)
    db.session.commit()
    return jsonify({"mensagem": "Processo seletivo excluído com sucesso!"})
