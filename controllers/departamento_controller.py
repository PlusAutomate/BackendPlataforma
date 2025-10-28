from flask import Blueprint, jsonify
from models import Departamento

departamento_bp = Blueprint("departamento", __name__, url_prefix="/departamentos")

@departamento_bp.route("", methods=["GET"])
def listar_departamentos():
    """
    Retorna a lista de todos os departamentos cadastrados.
    Exemplo de retorno:
    [
        {"id_departamento": 1, "nome": "Tecnologia"},
        {"id_departamento": 2, "nome": "Financeiro"}
    ]
    """
    departamentos = Departamento.query.order_by(Departamento.nome).all()
    resultado = [
        {"id_departamento": d.id_departamento, "nome": d.nome}
        for d in departamentos
    ]
    return jsonify(resultado), 200
