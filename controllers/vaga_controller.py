from flask import Blueprint, jsonify, request
from models import Vaga, db

vaga_bp = Blueprint("vaga", __name__, url_prefix="/vagas")


# =========================
# Listar todas as vagas ativas
# =========================
@vaga_bp.route("", methods=["GET"])
def listar_vagas():
    vagas_ativas = Vaga.query.filter(
        Vaga.status.in_(["Aberta", "Em Análise", "Solicitada"])
    ).all()

    resultado = [{
        "id_vaga": v.id_vaga,
        "titulo": v.titulo,
        "descricao": v.descricao,
        "status": v.status,
        "data_criacao": v.data_criacao.strftime("%Y-%m-%d %H:%M:%S")
    } for v in vagas_ativas]

    return jsonify(resultado)


# =========================
# Listar vagas de um gestor específico
# =========================
@vaga_bp.route("/gestor/<int:usuario_id>", methods=["GET"])
def listar_vagas_por_gestor(usuario_id):
    vagas = Vaga.query.filter(
        Vaga.id_usuario == usuario_id,
        Vaga.status.in_(["Aberta", "Em Análise", "Solicitada"])
    ).all()

    return jsonify([{
        "id_vaga": v.id_vaga,
        "titulo": v.titulo,
        "descricao": v.descricao,
        "status": v.status,
        "data_criacao": v.data_criacao.strftime("%Y-%m-%d %H:%M:%S"),
        "id_usuario": v.id_usuario
    } for v in vagas])


# =========================
# Detalhar vaga
# =========================
@vaga_bp.route("/<int:id>", methods=["GET"])
def detalhar_vaga(id):
    vaga = Vaga.query.get_or_404(id)
    if vaga.status not in ["Aberta", "Em Análise", "Solicitada"]:
        return jsonify({"erro": "Vaga não está ativa"}), 404

    return jsonify({
        "id_vaga": vaga.id_vaga,
        "titulo": vaga.titulo,
        "descricao": vaga.descricao,
        "status": vaga.status,
        "data_criacao": vaga.data_criacao.strftime("%Y-%m-%d %H:%M:%S")
    })


# =========================
# Criar vaga
# =========================
@vaga_bp.route("", methods=["POST"])
def criar_vaga():
    dados = request.json
    vaga = Vaga(
        titulo=dados["titulo"],
        descricao=dados.get("descricao", ""),
        status=dados.get("status", "Solicitada"),
        id_usuario=dados["id_usuario"],
        id_departamento=dados["id_departamento"],
        localizacao=dados["localizacao"],
        tipo_contratacao=dados["tipo_contratacao"],
        nivel_vaga=dados["nivel_vaga"],
        motivo=dados["motivo"],
        numero_vagas=dados.get("numero_vagas", 1),
        urgencia=dados.get("urgencia", "Normal"),
        projeto=dados.get("projeto"),
        prazo=dados.get("prazo"),
        skills=dados.get("skills")
    )
    db.session.add(vaga)
    db.session.commit()
    return jsonify({"mensagem": "Vaga criada com sucesso!", "id_vaga": vaga.id_vaga}), 201


# =========================
# Editar vaga
# =========================
@vaga_bp.route("/<int:id>", methods=["PUT"])
def editar_vaga(id):
    vaga = Vaga.query.get_or_404(id)

    dados = request.json
    vaga.titulo = dados.get("titulo", vaga.titulo)
    vaga.descricao = dados.get("descricao", vaga.descricao)
    vaga.status = dados.get("status", vaga.status)
    vaga.localizacao = dados.get("localizacao", vaga.localizacao)
    vaga.tipo_contratacao = dados.get(
        "tipo_contratacao", vaga.tipo_contratacao)
    vaga.nivel_vaga = dados.get("nivel_vaga", vaga.nivel_vaga)
    vaga.motivo = dados.get("motivo", vaga.motivo)
    vaga.numero_vagas = dados.get("numero_vagas", vaga.numero_vagas)
    vaga.urgencia = dados.get("urgencia", vaga.urgencia)
    vaga.projeto = dados.get("projeto", vaga.projeto)
    vaga.prazo = dados.get("prazo", vaga.prazo)
    vaga.skills = dados.get("skills", vaga.skills)

    db.session.commit()
    return jsonify({"mensagem": "Vaga atualizada com sucesso!"})


# =========================
# Marcar vaga como fechada
# =========================
@vaga_bp.route("/<int:id>", methods=["DELETE"])
def excluir_vaga(id):
    vaga = Vaga.query.get_or_404(id)

    # Usando status para "inativar"
    if vaga.status == "Fechada":
        return jsonify({"mensagem": "Vaga já está fechada."}), 400

    vaga.status = "Fechada"
    db.session.commit()
    return jsonify({"mensagem": "Vaga marcada como fechada com sucesso!"})


# =========================
# Aprovar vaga
# =========================
@vaga_bp.route("/<int:id>/aprovar", methods=["PUT"])
def aprovar_vaga(id):
    vaga = Vaga.query.get_or_404(id)

    if vaga.status == "Fechada":
        return jsonify({"erro": "Não é possível aprovar uma vaga fechada."}), 400

    vaga.status = "Aberta"
    db.session.commit()
    return jsonify({"mensagem": "Vaga aprovada!"})
