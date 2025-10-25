from flask import Blueprint, jsonify, request
from models import Vaga, db

vaga_bp = Blueprint("vaga", __name__, url_prefix="/vagas")


@vaga_bp.route("", methods=["GET"])
def listar_vagas():
    vagas = Vaga.query.filter_by(ativo=True).all()  # ← apenas vagas ativas
    return jsonify([{
        "id_vaga": v.id_vaga,
        "titulo": v.titulo,
        "descricao": v.descricao,
        "status": v.status,
        "data_criacao": v.data_criacao,
        "ativo": v.ativo
    } for v in vagas])


@vaga_bp.route("/<int:id>", methods=["GET"])
def detalhar_vaga(id):
    vaga = Vaga.query.get_or_404(id)
    if not vaga.ativo:
        return jsonify({"erro": "Vaga inativa"}), 404
    return jsonify({
        "id_vaga": vaga.id_vaga,
        "titulo": vaga.titulo,
        "descricao": vaga.descricao,
        "status": vaga.status,
        "data_criacao": vaga.data_criacao,
        "ativo": vaga.ativo
    })


@vaga_bp.route("", methods=["POST"])
def criar_vaga():
    dados = request.json
    vaga = Vaga(
        titulo=dados["titulo"],
        descricao=dados.get("descricao"),
        status="aberta",
        usuario_id_usuario=dados["usuario_id_usuario"]
    )
    db.session.add(vaga)
    db.session.commit()
    return jsonify({"mensagem": "Vaga criada com sucesso!"}), 201


@vaga_bp.route("/<int:id>", methods=["PUT"])
def editar_vaga(id):
    vaga = Vaga.query.get_or_404(id)
    if not vaga.ativo:
        return jsonify({"erro": "Não é possível editar uma vaga inativa."}), 400

    dados = request.json
    vaga.titulo = dados.get("titulo", vaga.titulo)
    vaga.descricao = dados.get("descricao", vaga.descricao)
    vaga.status = dados.get("status", vaga.status)

    db.session.commit()
    return jsonify({"mensagem": "Vaga atualizada com sucesso!"})


@vaga_bp.route("/<int:id>", methods=["DELETE"])
def excluir_vaga(id):
    vaga = Vaga.query.get_or_404(id)
    if not vaga.ativo:
        return jsonify({"mensagem": "Vaga já está inativa."}), 400

    vaga.ativo = False  # ← marca como inativa
    db.session.commit()
    return jsonify({"mensagem": "Vaga marcada como inativa com sucesso!"})


@vaga_bp.route("/<int:id>/aprovar", methods=["PUT"])
def aprovar_vaga(id):
    vaga = Vaga.query.get_or_404(id)
    if not vaga.ativo:
        return jsonify({"erro": "Não é possível aprovar uma vaga inativa."}), 400

    vaga.status = "Aberta"
    db.session.commit()
    return jsonify({"mensagem": "Vaga aprovada!"})
