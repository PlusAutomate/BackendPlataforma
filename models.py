from config import db
from datetime import datetime


class Usuario(db.Model):
    __tablename__ = 'usuario'

    id_usuario = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(45), nullable=False)
    tipo = db.Column(db.Enum('GESTOR', 'RH'), nullable=False)
    vagas = db.relationship('Vaga', backref='usuario', lazy=True)

    def __repr__(self):
        return f"<Usuario {self.nome}>"


class Vaga(db.Model):
    __tablename__ = 'vaga'

    id_vaga = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(255))
    status = db.Column(db.String(100), default='aberta')
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    usuario_id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'), nullable=False)
    ativo = db.Column(db.Boolean, default=True, nullable=False)

    def __repr__(self):
        return f"<Vaga {self.titulo}>"


class Curriculo(db.Model):
    __tablename__ = 'curriculo'

    id_curriculo = db.Column(db.Integer, primary_key=True)
    caminho = db.Column(db.String(255), nullable=False)
    candidatos = db.relationship('Candidato', backref='curriculo', lazy=True)

    def __repr__(self):
        return f"<Curriculo {self.caminho}>"


class Candidato(db.Model):
    __tablename__ = 'candidato'

    id_candidato = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    telefone = db.Column(db.String(20))
    curriculo_id_curriculo = db.Column(db.Integer, db.ForeignKey('curriculo.id_curriculo'))
    ativo = db.Column(db.Boolean, default=True, nullable=False)

    def __repr__(self):
        return f"<Candidato {self.nome}>"


class ProcessoSeletivo(db.Model):
    __tablename__ = 'processo_seletivo'

    vaga_id_vaga = db.Column(db.Integer, db.ForeignKey('vaga.id_vaga'), primary_key=True)
    candidato_id_candidato = db.Column(db.Integer, db.ForeignKey('candidato.id_candidato'), primary_key=True)

    def __repr__(self):
        return f"<ProcessoSeletivo Vaga={self.vaga_id_vaga} Candidato={self.candidato_id_candidato}>"
