from flask import Blueprint, jsonify, request
from models import ProcessoSeletivo, db, Vaga, Candidato, Curriculo, Usuario

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


@processo_bp.route("/gestor/<int:id_usuario>", methods=["GET"])
def listar_candidatos_por_gestor(id_usuario):
    try:
        resultados = (
            db.session.query(
                Vaga.id_vaga,
                Vaga.titulo.label("titulo_vaga"),
                Vaga.id_usuario,
                Usuario.nome.label("nome_gestor"),
                Candidato.id_candidato,
                Candidato.nome.label("nome_candidato"),
                Candidato.email.label("email_candidato"),
                ProcessoSeletivo.status
            )
            .join(Vaga, ProcessoSeletivo.id_vaga == Vaga.id_vaga)
            .join(Usuario, Usuario.id_usuario == Vaga.id_usuario)
            .join(Candidato, ProcessoSeletivo.id_candidato == Candidato.id_candidato)
            .filter(Vaga.id_usuario == id_usuario)
            .all()
        )

        if not resultados:
            return jsonify([]), 200

        dados = [
            {
                "id_vaga": r.id_vaga,
                "titulo_vaga": r.titulo_vaga,
                "id_usuario": r.id_usuario,
                "nome_gestor": r.nome_gestor,
                "id_candidato": r.id_candidato,
                "nome_candidato": r.nome_candidato,
                "email_candidato": r.email_candidato,
                "status": r.status
            }
            for r in resultados
        ]

        return jsonify(dados), 200

    except Exception as e:
        return jsonify({"erro": str(e)}), 500

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
            resultado.append({
                "id_candidato": candidato.id_candidato,
                "nome": candidato.nome,
                "email": candidato.email,
                "telefone": candidato.telefone,
                "status": p.status,
                "vaga": vaga.titulo if vaga else None,
                "id_vaga": id_vaga,
                "curriculo": None  # não há vínculo direto
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
            "candidato_telefone": candidato.telefone,
            "nome": candidato.nome if candidato else None,
            "email": candidato.email if candidato else None,
            "status": p.status,
            "data_criacao": p.data_criacao.strftime("%Y-%m-%d %H:%M:%S"),
            "data_atualizacao": p.data_atualizacao.strftime("%Y-%m-%d %H:%M:%S"),
            "cvDetalhe": {
                "skill": candidato.skill.split(',') if candidato and candidato.skill else []
            }
        })

    return jsonify(resultado)


@processo_bp.route("/candidato/<int:id_candidato>", methods=["GET"])
def listar_processos_candidato(id_candidato):
    # Busca apenas os processos do candidato específico
    processos = ProcessoSeletivo.query.filter_by(
        id_candidato=id_candidato).all()

    resultado = []
    for p in processos:
        vaga = p.vaga  # relacionamento com a vaga
        candidato = p.candidato  # relacionamento com o candidato

        resultado.append({
            "id_vaga": p.id_vaga,
            "titulo_vaga": vaga.titulo if vaga else None,
            "id_candidato": p.id_candidato,
            "candidato_telefone": candidato.telefone if candidato else None,
            "nome": candidato.nome if candidato else None,
            "email": candidato.email if candidato else None,
            "status": p.status,
            "data_criacao": p.data_criacao.strftime("%Y-%m-%d %H:%M:%S") if p.data_criacao else None,
            "data_atualizacao": p.data_atualizacao.strftime("%Y-%m-%d %H:%M:%S") if p.data_atualizacao else None,
            "cvDetalhe": {
                "skills": candidato.skill.split(',') if candidato and candidato.skill else []
            },
            "vagaSkills": vaga.skills.split(',') if vaga and vaga.skills else []
        })

    return jsonify(resultado), 200


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

# =========================
# Atualizar status do processo seletivo
# =========================


@processo_bp.route("/<int:id_vaga>/<int:id_candidato>", methods=["PUT"])
def atualizar_status_processo(id_vaga, id_candidato):
    try:
        dados = request.json
        novo_status = dados.get("status")

        if not novo_status:
            return jsonify({"erro": "O campo 'status' é obrigatório."}), 400

        processo = ProcessoSeletivo.query.filter_by(
            id_vaga=id_vaga,
            id_candidato=id_candidato
        ).first()

        if not processo:
            return jsonify({"erro": "Processo seletivo não encontrado."}), 404

        processo.status = novo_status
        db.session.commit()

        return jsonify({
            "mensagem": "Status atualizado com sucesso!",
            "id_vaga": id_vaga,
            "id_candidato": id_candidato,
            "novo_status": novo_status
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": str(e)}), 500
