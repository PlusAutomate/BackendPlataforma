from flask import Blueprint, jsonify, request
from models import Candidato, db

candidato_bp = Blueprint("candidato", __name__, url_prefix="/candidatos")

@candidato_bp.route("", methods=["GET"])
def listar_candidatos():
    candidatos = Candidato.query.all()
    return jsonify([{
        "id_candidato": c.id_candidato,
        "nome": c.nome,
        "email": c.email,
        "telefone": c.telefone,
        "curriculo_id": c.curriculo_id_curriculo
    } for c in candidatos])

@candidato_bp.route("/<int:id>", methods=["GET"])
def detalhar_candidato(id):
    c = Candidato.query.get_or_404(id)
    return jsonify({
        "id_candidato": c.id_candidato,
        "nome": c.nome,
        "email": c.email,
        "telefone": c.telefone,
        "curriculo_id": c.curriculo_id_curriculo
    })

@candidato_bp.route("", methods=["POST"])
def criar_candidato():
    dados = request.json
    candidato = Candidato(
        nome=dados["nome"],
        email=dados["email"],
        telefone=dados["telefone"],
        curriculo_id_curriculo=dados["curriculo_id_curriculo"]
    )
    db.session.add(candidato)
    db.session.commit()
    return jsonify({"mensagem": "Candidato cadastrado com sucesso!"}), 201

@candidato_bp.route("/<int:id>", methods=["PUT"])
def editar_candidato(id):
    c = Candidato.query.get_or_404(id)
    dados = request.json
    c.nome = dados.get("nome", c.nome)
    c.email = dados.get("email", c.email)
    c.telefone = dados.get("telefone", c.telefone)
    db.session.commit()
    return jsonify({"mensagem": "Candidato atualizado!"})

@candidato_bp.route("/<int:id>", methods=["DELETE"])
def excluir_candidato(id):
    c = Candidato.query.get_or_404(id)
    db.session.delete(c)
    db.session.commit()
    return jsonify({"mensagem": "Candidato excluído com sucesso!"})
