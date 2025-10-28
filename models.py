from config import db
from datetime import datetime
from sqlalchemy.dialects.mysql import ENUM, JSON

# =========================
# USUARIO
# =========================


class Usuario(db.Model):
    __tablename__ = 'usuario'

    id_usuario = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(45), nullable=False)
    tipo = db.Column(ENUM('GESTOR', 'RH'), nullable=False)

    vagas = db.relationship('Vaga', backref='usuario', lazy=True)

    def __repr__(self):
        return f"<Usuario {self.nome}>"


# =========================
# DEPARTAMENTO
# =========================
class Departamento(db.Model):
    __tablename__ = 'departamento'

    id_departamento = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), unique=True, nullable=False)

    vagas = db.relationship('Vaga', backref='departamento', lazy=True)

    def __repr__(self):
        return f"<Departamento {self.nome}>"


# =========================
# CURRICULO
# =========================
# =========================
# CURRICULO
# =========================
class Curriculo(db.Model):
    __tablename__ = 'curriculo'

    id_curriculo = db.Column(db.Integer, primary_key=True)
    caminho = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"<Curriculo {self.caminho}>"



# =========================
# CANDIDATO
# =========================
class Candidato(db.Model):
    __tablename__ = 'candidato'

    id_candidato = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120))
    telefone = db.Column(db.String(20))
    skill = db.Column(db.String(100))
    origem = db.Column(
        ENUM('Upload RH', 'Indicação', 'LinkedIn', 'Plataforma', 'Outro'),
        default='Upload RH'
    )
    data_criacao = db.Column(
        db.TIMESTAMP, server_default=db.func.current_timestamp())

    # Relacionamento com Processo Seletivo
    processos = db.relationship(
        'ProcessoSeletivo', backref='candidato', lazy=True)

    def __repr__(self):
        return f"<Candidato {self.nome}>"


# =========================
# VAGA
# =========================
class Vaga(db.Model):
    __tablename__ = 'vaga'

    id_vaga = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150), nullable=False)
    id_departamento = db.Column(db.Integer, db.ForeignKey(
        'departamento.id_departamento'), nullable=False)
    id_usuario = db.Column(db.Integer, db.ForeignKey(
        'usuario.id_usuario'), nullable=False)
    localizacao = db.Column(
        ENUM('Remoto', 'Presencial', 'Híbrido'), nullable=False)
    cidade = db.Column(db.String(100))
    tipo_contratacao = db.Column(
        ENUM('CLT', 'PJ', 'Estágio', 'Temporário'), nullable=False)
    nivel_vaga = db.Column(
        ENUM('Junior', 'Pleno', 'Senior', 'Lead', 'Manager'), nullable=False)
    motivo = db.Column(ENUM('Substituição', 'Crescimento',
                       'Projeto Temporário', 'Reestruturação'), nullable=False)
    numero_vagas = db.Column(db.Integer, default=1, nullable=False)
    urgencia = db.Column(ENUM('Normal', 'Alta', 'Crítica'),
                         default='Normal', nullable=False)
    projeto = db.Column(db.String(100))
    prazo = db.Column(db.Date)
    descricao = db.Column(db.Text, nullable=False)
    skills = db.Column(db.String(250))
    status = db.Column(ENUM('Solicitada', 'Em Análise', 'Aprovada', 'Rejeitada',
                       'Aberta', 'Fechada'), default='Solicitada', nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    data_atualizacao = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    detalhe_rh = db.relationship(
        'DetalheRH', backref='vaga', lazy=True, uselist=False)
    processos = db.relationship('ProcessoSeletivo', backref='vaga', lazy=True)

    def __repr__(self):
        return f"<Vaga {self.titulo}>"


# =========================
# DETALHE_RH
# =========================
class DetalheRH(db.Model):
    __tablename__ = 'detalhe_rh'

    id_detalhe_rh = db.Column(db.Integer, primary_key=True)
    id_vaga = db.Column(db.Integer, db.ForeignKey(
        'vaga.id_vaga'), nullable=False)
    salario_min = db.Column(db.Numeric(10, 2))
    salario_max = db.Column(db.Numeric(10, 2))
    beneficios = db.Column(db.Text)
    responsavel_rh = db.Column(db.String(100))
    data_atualizacao = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<DetalheRH Vaga {self.id_vaga}>"


# =========================
# PROCESSO_SELETIVO
# =========================
class ProcessoSeletivo(db.Model):
    __tablename__ = 'processo_seletivo'

    id_vaga = db.Column(db.Integer, db.ForeignKey(
        'vaga.id_vaga'), primary_key=True)
    id_candidato = db.Column(db.Integer, db.ForeignKey(
        'candidato.id_candidato'), primary_key=True)
    status = db.Column(ENUM('Novo', 'Triagem', 'Entrevista',
                       'Aprovado', 'Contratado', 'Rejeitado'), default='Novo')
    analise_automatica = db.Column(JSON, nullable=True)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    data_atualizacao = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<ProcessoSeletivo Vaga {self.id_vaga} Candidato {self.id_candidato}>"
