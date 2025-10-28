from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://backenduser:sua_senha_forte@54.88.151.87:3306/sistema_rh'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # 🔹 Permitir apenas o seu frontend atual
    CORS(app, origins=[
        "http://127.0.0.1:58006",
        "http://localhost:58006,"
        "http://18.234.110.104:58006"
    ])

    return app
