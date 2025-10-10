import os
from flask import Blueprint, jsonify, request
from werkzeug.utils import secure_filename
from models import Curriculo, db

curriculo_bp = Blueprint("curriculo", __name__, url_prefix="/curriculos")

UPLOAD_FOLDER = "uploads"

@curriculo_bp.route("/upload", methods=["POST"])
def upload_curriculo():
    if "file" not in request.files:
        return jsonify({"erro": "Nenhum arquivo enviado"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"erro": "Nome de arquivo inválido"}), 400

    filename = secure_filename(file.filename)
    caminho = os.path.join(UPLOAD_FOLDER, filename)
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    file.save(caminho)

    curriculo = Curriculo(caminho=caminho)
    db.session.add(curriculo)
    db.session.commit()

    return jsonify({"mensagem": "Currículo enviado com sucesso!", "id": curriculo.id_curriculo}), 201

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
    if os.path.exists(c.caminho):
        os.remove(c.caminho)
    db.session.delete(c)
    db.session.commit()
    return jsonify({"mensagem": "Currículo excluído com sucesso!"})
