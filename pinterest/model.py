# Cria estrutura do banco de dados
# database e login_manager está localizado em __init__
from pinterest import database, login_manager
from datetime import datetime
from flask_login import UserMixin

# Encontra usuário de acordo com ID
# O nome da função é padrão: load_
@login_manager.user_loader
def load_user(id_user):
    return User.query.get(int(id_user))

# UserMixin diz qual a class vai gerenciar o sistema de login
class User(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key = True)
    username = database.Column(database.String, nullable = False, unique = True)
    email = database.Column(database.String, nullable = False)
    password = database.Column(database.String, nullable = False)
    # photos não é uma coluna (Nome da classe que vai se relacionar, um backref)
    # o backref é como se fosse o relationship no caminho contrário, ligando a classe Post
    photos = database.relationship("Post", backref="usuario", lazy = True)

class Post(database.Model):
    id = database.Column(database.Integer, primary_key = True)
    # image vai ser string pq vai ser o caminho da imagem
    image = database.Column(database.String, default="default.png")
    # o default do date_creation registra o horário na hora
    date_creation = database.Column(database.DateTime, nullable= False, default= datetime.utcnow())
    id_user = database.Column(database.Integer,  database.ForeignKey('user.id'), nullable= False)