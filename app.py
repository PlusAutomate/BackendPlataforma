from flask import Flask
from config import create_app, db
from controllers.usuario_controller import usuario_bp
from controllers.vaga_controller import vaga_bp
from controllers.candidato_controller import candidato_bp
from controllers.curriculo_controller import curriculo_bp

app = create_app()

# Registrar blueprints
app.register_blueprint(usuario_bp)
app.register_blueprint(vaga_bp)
app.register_blueprint(candidato_bp)
app.register_blueprint(curriculo_bp)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
