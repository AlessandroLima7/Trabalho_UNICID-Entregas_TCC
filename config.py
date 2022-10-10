import os

SECRET_KEY = 'globalEmpresArioDjaneiro'

SQLALCHEMY_DATABASE_URI = \
    '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
        SGBD = 'mysql+mysqlconnector',
        usuario = 'root',
        senha = '',
        servidor = 'localhost',
        database = 'gerenciador'
    )

UPLOAD_PATH = os.path.dirname(os.path.abspath(__file__)) + '/arquivos'