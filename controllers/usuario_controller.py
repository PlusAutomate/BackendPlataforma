from flask import Blueprint, jsonify, request
from models import Usuario  # seu modelo SQLAlchemy

usuario_bp = Blueprint("usuario", __name__, url_prefix="/usuario")

@usuario_bp.route("/<int:id>", methods=["GET"])
def get_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    return jsonify({
        "id_usuario": usuario.id_usuario,
        "nome": usuario.nome,
        "email": usuario.email,
        "tipo": usuario.tipo
    })

from flask import Blueprint, jsonify, request
from models import Usuario

usuario_bp = Blueprint("usuario", __name__, url_prefix="/usuario")


# -----------------------------
# 🔹 LOGIN RH
# -----------------------------
@usuario_bp.route("/login_rh", methods=["POST"])
def login_rh():
    dados = request.get_json()

    email = dados.get("email")
    senha = dados.get("senha")

    if not email or not senha:
        return jsonify({"erro": "Email e senha são obrigatórios"}), 400

    usuario = Usuario.query.filter_by(email=email).first()

    if not usuario or usuario.senha != senha:
        return jsonify({"erro": "Email ou senha inválidos"}), 401

    # Permite apenas RH
    if usuario.tipo != "RH":
        return jsonify({"erro": "Usuário não autorizado para acessar o sistema RH"}), 403

    return jsonify({
        "mensagem": "Login RH bem-sucedido!",
        "usuario": {
            "id_usuario": usuario.id_usuario,
            "nome": usuario.nome,
            "email": usuario.email,
            "tipo": usuario.tipo
        }
    }), 200


# -----------------------------
# 🔹 LOGIN GESTOR
# -----------------------------
@usuario_bp.route("/login_gestor", methods=["POST"])
def login_gestor():
    dados = request.get_json()

    email = dados.get("email")
    senha = dados.get("senha")

    if not email or not senha:
        return jsonify({"erro": "Email e senha são obrigatórios"}), 400

    usuario = Usuario.query.filter_by(email=email).first()

    if not usuario or usuario.senha != senha:
        return jsonify({"erro": "Email ou senha inválidos"}), 401

    # Permite apenas GESTOR
    if usuario.tipo != "GESTOR":
        return jsonify({"erro": "Usuário não autorizado para acessar o sistema Gestor"}), 403

    return jsonify({
        "mensagem": "Login Gestor bem-sucedido!",
        "usuario": {
            "id_usuario": usuario.id_usuario,
            "nome": usuario.nome,
            "email": usuario.email,
            "tipo": usuario.tipo
        }
    }), 200
