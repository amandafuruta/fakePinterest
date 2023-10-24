from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///comunidade.db"

# chave de segurança do app. é uma chave aleatória
app.config["SECRET_KEY"] = '28b0ea93dca5efaccf48015653dc609b'

# Indica em qual pasta vai ser armazenado as fotos dos usuários
app.config['UPLOAD_FOLDER'] = "static/fotos_posts"

database = SQLAlchemy(app) 
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

# Para qual pagina é direcionada se o usuário não estiver logado
login_manager.login_view = 'home'


from pinterest import view