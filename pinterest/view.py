# A pasta 'templates' tem que ter esse nome obrigatoriamente, o render_template do Flask localiza pelo nome
# O url_for é importado dessa forma mesmo. Ele é o responsável pelas rotas das páginas serem por meio do nome das funcoes. Veja como fica, ex: profilepage.htmls
# Links do site

from flask import render_template, url_for, redirect
from pinterest import app, database, bcrypt
from pinterest.model import User, Post
from flask_login import login_required, login_user, logout_user, current_user
from pinterest.forms import FormCriarConta, FormLogin, FormFoto
import os
from werkzeug.utils import secure_filename

@app.route("/", methods=['GET', 'POST'])
def home():
    formlogin = FormLogin()

    # Se ele preencheu corretamento o formulário e os dados estão válidos
    if formlogin.validate_on_submit():
        usuario = User.query.filter_by(email = formlogin.email.data).first()

        # Se ele encontra um usuário e a senha for compatível
        if usuario and bcrypt.check_password_hash(usuario.password, formlogin.password.data):
            # Verifica se a senha está correta
            ## bcrypt.check_password_hash(usuario.password, formlogin.password.data)

            login_user(usuario)
            return redirect(url_for("profile", user_id = usuario.id))

    return render_template("homepage.html", form = formlogin)


@app.route('/criarconta', methods=['GET', 'POST'])
def criarconta():
    formcriarconta = FormCriarConta()

    # Verificar dados estão validos. Se sim:
    if formcriarconta.validate_on_submit():
        # criptografa a senha
        senha = bcrypt.generate_password_hash(formcriarconta.password.data)
        usuario = User(username= formcriarconta.username.data , email= formcriarconta.email.data , password= senha )

        # Grava no BD
        database.session.add(usuario)
        database.session.commit()
        # Remeber vai lembrar que usuário está logado
        login_user(usuario, remember= True)

        return redirect(url_for("profile", user_id = usuario.id))

    return render_template('criarconta.html', form = formcriarconta)


# Requer login para acessar essa página
@app.route("/profile/<user_id>", methods=['GET', 'POST'])
@login_required
def profile(user_id):    

    # Verificar se o usuário está vendo o próprio perfil
    # Dentro do próprio perfil, ele pode carregar fotos
    if int(user_id) == int(current_user.id):
        formFoto = FormFoto()

        if formFoto.validate_on_submit():
            arquivo = formFoto.foto.data
            nome_tratado = secure_filename(arquivo.filename)

            # salvar o arquivo na pasta foto_post
            # caminho = nome do diretório + static + nome do arquivo
            caminho = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], nome_tratado)
            arquivo.save(caminho)

            # registrar no bd
            foto = Post(image = nome_tratado, id_user = current_user.id )
            database.session.add(foto)
            database.session.commit()

        return render_template("profilepage.html", usuario = current_user, form = formFoto)
    
    # Ou se está vendo perfil de outra pessoa
    else:        
        usuario = User.query.get(int(user_id))
        return render_template("profilepage.html", usuario = usuario, form = None)


# Logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))

# Feed
@app.route("/feed")
@login_required
def feed():
    # as 100 primeiras fotos
    fotos = Post.query.order_by(Post.date_creation).all()[:100]
    return render_template("feed.html", fotos = fotos)