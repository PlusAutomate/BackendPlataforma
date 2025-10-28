from flask import Blueprint, jsonify, request
from config import db
from sqlalchemy import text

dashboard_gestor_bp = Blueprint("dashboard_gestor", __name__, url_prefix="/dashboard/gestor")

def run_query(sql):
    """Executa SELECT seguro e sempre retorna lista (mesmo se vazio)."""
    try:
        result = db.session.execute(text(sql))
        rows = [dict(row._mapping) for row in result]
        return rows
    except Exception as e:
        print(f"[ERRO DASHBOARD GESTOR] {e}")
        return []


# 1) Status das vagas — donut
@dashboard_gestor_bp.route("/status", methods=["GET"])
def status_vagas():
    rows = run_query("SELECT * FROM vw_status_vagas;")
    return jsonify(rows)


# 2) SLA (Fechar vs Contratar) — linha + KPIs
@dashboard_gestor_bp.route("/sla", methods=["GET"])
def sla_contratacao():
    # mensal
    mensais_fech = run_query("SELECT * FROM vw_sla_fechamento_mes;")
    mensais_contr = run_query("SELECT * FROM vw_sla_contratacao_mes;")
    # kpi médio
    medio_fech = run_query("SELECT * FROM vw_sla_fechamento_medio;")
    medio_cont = run_query("SELECT * FROM vw_sla_contratacao_medio;")

    return jsonify({
        "fechamento_mensal": mensais_fech,
        "contratacao_mensal": mensais_contr,
        "fechamento_medio": medio_fech[0] if medio_fech else {"fechar_medio_dias": 0},
        "contratacao_medio": medio_cont[0] if medio_cont else {"contratar_medio_dias": 0}
    })


# 3) Tempo médio por departamento — barras
@dashboard_gestor_bp.route("/departamento", methods=["GET"])
def tempo_por_departamento():
    rows = run_query("SELECT * FROM vw_tempo_medio_departamento;")
    return jsonify(rows)


# 4) Urgências — barras
@dashboard_gestor_bp.route("/urgencia", methods=["GET"])
def urgencia_vagas():
    rows = run_query("SELECT * FROM vw_urgencia_vagas;")
    return jsonify(rows)


# 5) Fechamentos por mês — linha
@dashboard_gestor_bp.route("/fechamentos", methods=["GET"])
def fechamentos_mes():
    rows = run_query("SELECT * FROM vw_fechamentos_mes;")
    return jsonify(rows)
