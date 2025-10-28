from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://Tom:Tom4002!@localhost:3306/sistema_rh'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # 🔹 Permitir apenas o seu frontend atual
    CORS(app, origins=[
        "http://127.0.0.1:55222",
        "http://localhost:55222"
    ])

    return app
