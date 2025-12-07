from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://backenduser:SenhaForte123!@23.21.188.183:3306/sistema_rh'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # 🔹 Permitir apenas o seu frontend atual
    CORS(app, origins=[
        "http://127.0.0.1:5000",
        "http://localhost:5000,"
        "http://44.195.153.109:5000"
    ])

    return app
