# Ao rodar esse código, uma pasta chamada instance é criada
from pinterest import database, app
# Essa importação é obrigatória
from pinterest.model import User, Post

with app.app_context():
    database.create_all()