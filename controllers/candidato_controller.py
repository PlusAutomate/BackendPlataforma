from flask import Blueprint, jsonify, request
from models import Candidato, db

candidato_bp = Blueprint("candidato", __name__, url_prefix="/candidatos")

@candidato_bp.route("", methods=["GET"])
def listar_candidatos():
    candidatos = Candidato.query.filter_by(ativo=True).all()  # ← apenas ativos
    return jsonify([{
        "id_candidato": c.id_candidato,
        "nome": c.nome,
        "email": c.email,
        "telefone": c.telefone,
        "curriculo_id": c.curriculo_id_curriculo,
        "ativo": c.ativo
    } for c in candidatos])

@candidato_bp.route("/<int:id>", methods=["GET"])
def detalhar_candidato(id):
    c = Candidato.query.get_or_404(id)
    return jsonify({
        "id_candidato": c.id_candidato,
        "nome": c.nome,
        "email": c.email,
        "telefone": c.telefone,
        "skill": c.skill,
        "origem": c.origem
    })

@candidato_bp.route("", methods=["POST"])
def criar_candidato():
    dados = request.json
    candidato = Candidato(
        nome=dados["nome"],
        email=dados["email"],
        telefone=dados.get("telefone"),
        curriculo_id_curriculo=dados.get("curriculo_id_curriculo"),
        ativo=True
    )
    db.session.add(candidato)
    db.session.commit()
    return jsonify({"mensagem": "Candidato cadastrado com sucesso!"}), 201

@candidato_bp.route("/<int:id>", methods=["PUT"])
def editar_candidato(id):
    c = Candidato.query.get_or_404(id)
    if not c.ativo:
        return jsonify({"erro": "Não é possível editar um candidato inativo."}), 400

    dados = request.json
    c.nome = dados.get("nome", c.nome)
    c.email = dados.get("email", c.email)
    c.telefone = dados.get("telefone", c.telefone)
    db.session.commit()
    return jsonify({"mensagem": "Candidato atualizado!"})

@candidato_bp.route("/<int:id>", methods=["DELETE"])
def excluir_candidato(id):
    c = Candidato.query.get_or_404(id)
    if not c.ativo:
        return jsonify({"mensagem": "Candidato já está inativo."}), 400

    c.ativo = False  # ← marca como inativo
    db.session.commit()
    return jsonify({"mensagem": "Candidato marcado como inativo com sucesso!"})
