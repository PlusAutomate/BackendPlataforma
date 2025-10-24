from flask import Blueprint, jsonify, request
from models import ProcessoSeletivo, db, Vaga, Candidato

processo_bp = Blueprint("processo", __name__, url_prefix="/processo-seletivo")


@processo_bp.route("", methods=["POST"])
def criar_processo_seletivo():
    dados = request.json
    vaga_id = dados.get("vaga_id_vaga")
    candidato_id = dados.get("candidato_id_candidato")

    vaga = Vaga.query.get(vaga_id)
    candidato = Candidato.query.get(candidato_id)
    if not vaga or not candidato:
        return jsonify({"erro": "Vaga ou candidato não encontrados"}), 404

    processo = ProcessoSeletivo(
        vaga_id_vaga=vaga_id,
        candidato_id_candidato=candidato_id
    )

    db.session.add(processo)
    db.session.commit()

    return jsonify({
    "mensagem": "Processo seletivo criado com sucesso!",
    "vaga_id_vaga": processo.vaga_id_vaga,
    "candidato_id_candidato": processo.candidato_id_candidato
}), 201

@processo_bp.route("", methods=["GET"])
def listar_processos():
    processos = ProcessoSeletivo.query.all()
    return jsonify([{
        "vaga_id_vaga": p.vaga_id_vaga,
        "candidato_id_candidato": p.candidato_id_candidato
    } for p in processos])

@processo_bp.route("", methods=["DELETE"])
def excluir_processo_seletivo():
    dados = request.json
    vaga_id = dados.get("vaga_id_vaga")
    candidato_id = dados.get("candidato_id_candidato")

    if not vaga_id or not candidato_id:
        return jsonify({"erro": "Informe vaga_id_vaga e candidato_id_candidato"}), 400

    processo = ProcessoSeletivo.query.filter_by(
        vaga_id_vaga=vaga_id,
        candidato_id_candidato=candidato_id
    ).first()

    if not processo:
        return jsonify({"erro": "Registro não encontrado"}), 404

    db.session.delete(processo)
    db.session.commit()
    return jsonify({"mensagem": "Processo seletivo excluído com sucesso!"})
