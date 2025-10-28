from flask import Flask
from config import create_app, db
from controllers.usuario_controller import usuario_bp
from controllers.vaga_controller import vaga_bp
from controllers.candidato_controller import candidato_bp
from controllers.curriculo_controller import curriculo_bp
from controllers.processo_seletivo_controller import processo_bp
from controllers.departamento_controller import departamento_bp
from controllers.dashboard_rh_controller import dashboard_rh_bp
from controllers.dashboard_gestor_controller import dashboard_gestor_bp
    
app = create_app()

# Registrar blueprints
app.register_blueprint(usuario_bp)
app.register_blueprint(vaga_bp)
app.register_blueprint(candidato_bp)
app.register_blueprint(curriculo_bp)
app.register_blueprint(processo_bp)
app.register_blueprint(departamento_bp)
app.register_blueprint(dashboard_rh_bp)
app.register_blueprint(dashboard_gestor_bp)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
