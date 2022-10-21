from main import db
from sqlalchemy import ForeignKey

class Professores(db.Model):
    id_professor = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(40), nullable=False) 
    senha = db.Column(db.String(8), nullable=False)
    permissao = db.Column(db.String(20), nullable=True)
    def __repr__(self):
        return '<Name %r>' % self.name
    
class Grupos(db.Model):
    nome = db.Column(db.String(80), primary_key=True, nullable=False)
    email = db.Column(db.String(40), nullable=False) 
    senha = db.Column(db.String(8), nullable=False) 
    orientador = db.Column(db.Integer, ForeignKey(Professores.id_professor))
    turma = db.Column(db.String(40), nullable=False)
    def __repr__(self):
        return '<Name %r>' % self.name   

class Documentos(db.Model):
    id_documento = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(80), nullable=False)
    turma = db.Column(db.String(80), nullable=True)
    grupo = db.Column(db.String(80), ForeignKey(Grupos.nome))
    data_hora = db.Column(db.Date, nullable=True)
    arquivo = db.Column(db.String(200), nullable=True)
    avaliacao = db.Column(db.String(30), nullable=True)
    def __repr__(self):
        return '<Name %r>' % self.name


