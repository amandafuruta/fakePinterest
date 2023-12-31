from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import os

app = Flask(__name__)
# Local
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///comunidade.db"

# Variável de ambiente criado no Render
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('DATABASE_URL')

# Link externo do Render para criar um bd online.. depois de criado, não precisa mais
# app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://fake_pintereste_bd_user:2dtPrZmn6sqLBgMzJGhXszA2BBYJQdol@dpg-ckrvc5fd47qs73esvoag-a.oregon-postgres.render.com/fake_pintereste_bd'


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