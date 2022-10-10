from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import SECRET_KEY

app = Flask(__name__)
app.config.from_pyfile('config.py')
app.secret_key = SECRET_KEY
db = SQLAlchemy(app)

from views import * 

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

