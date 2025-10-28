# controllers/dashboard_rh_controller.py

from flask import Blueprint, jsonify
from config import db
from sqlalchemy import text

dashboard_rh_bp = Blueprint("dashboard_rh", __name__, url_prefix="/dashboard/rh")

# ------------------------------------------------
# Função padrão segura (mesma do gestor)
# ------------------------------------------------
def run_query(sql):
    try:
        result = db.session.execute(text(sql))
        rows = [dict(row._mapping) for row in result]
        return rows
    except Exception as e:
        print(f"[ERRO DASH RH] {e}")
        return []

# ------------------------------------------------
# 1) Tempo médio por etapa
# ------------------------------------------------
@dashboard_rh_bp.route("/tempo-etapas", methods=["GET"])
def get_tempo_etapas():
    rows = run_query("SELECT * FROM vw_tempo_medio_etapas;")
    return jsonify(rows)

# ------------------------------------------------
# 2) Taxa de aprovação (linha única)
# ------------------------------------------------
@dashboard_rh_bp.route("/taxa-aprovacao", methods=["GET"])
def get_taxa_aprovacao():
    rows = run_query("SELECT * FROM vw_taxa_aprovacao_entrevista;")
    return jsonify(rows[0] if rows else {
        "taxa_percent": 0,
        "aprovados": 0,
        "avaliados": 0
    })

# ------------------------------------------------
# 3) Áreas mais requisitadas
# ------------------------------------------------
@dashboard_rh_bp.route("/areas", methods=["GET"])
def get_areas():
    rows = run_query("SELECT * FROM vw_areas_mais_requisitadas;")
    return jsonify(rows)

# ------------------------------------------------
# 4) Tempo médio de fechamento por vaga
# ------------------------------------------------
@dashboard_rh_bp.route("/tempo-fechamento", methods=["GET"])
def get_tempo_fechamento():
    rows = run_query("SELECT * FROM vw_tempo_medio_fechamento_vaga;")
    return jsonify(rows)

# ------------------------------------------------
# 5) Origem dos candidatos (pizza)
# ------------------------------------------------
@dashboard_rh_bp.route("/origem", methods=["GET"])
def get_origem():
    rows = run_query("SELECT * FROM vw_origem_candidatos;")
    return jsonify(rows)

# ------------------------------------------------
# 6) Urgência x volume
# ------------------------------------------------
@dashboard_rh_bp.route("/urgencia", methods=["GET"])
def get_urgencia():
    rows = run_query("SELECT * FROM vw_urgencia_vagas;")
    return jsonify(rows)

# ------------------------------------------------
# 7) Funil do processo
# ------------------------------------------------
@dashboard_rh_bp.route("/funil", methods=["GET"])
def get_funil():
    rows = run_query("SELECT * FROM vw_funil_processo;")
    return jsonify(rows)

# ------------------------------------------------
# 8) Crescimento do banco de talentos
# ------------------------------------------------
@dashboard_rh_bp.route("/talentos", methods=["GET"])
def get_talentos():
    rows = run_query("SELECT * FROM vw_talentos_mes;")
    return jsonify(rows)

# ------------------------------------------------
# 9) Taxa de abandono
# ------------------------------------------------
@dashboard_rh_bp.route("/abandono", methods=["GET"])
def get_abandono():
    rows = run_query("SELECT * FROM vw_taxa_abandono_mes;")
    return jsonify(rows)
