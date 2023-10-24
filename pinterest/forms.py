
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, ValidationError, FileField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from pinterest.model import User

# Essas classes não são para o BD
class FormLogin(FlaskForm):
    email = StringField("E-mail", validators= [DataRequired(), Email()])
    password = PasswordField("Senha", validators=[DataRequired()])
    confirm_button = SubmitField("Fazer login")

    def validate_email(self, email):
        usuario = User.query.filter_by(email = email.data).first()
        if not usuario:
            raise ValidationError('Usuário não encontrado, crie uma conta')

class FormCriarConta(FlaskForm):
    username = StringField("Usuário", validators=[DataRequired()])
    email = StringField("E-mail", validators= [DataRequired(), Email()])
    password = PasswordField("Senha", validators=[DataRequired(), Length(6, 20)])
    confirm_password = PasswordField("Confirmar Senha", validators=[DataRequired(), EqualTo("password")])
    confirm_button = SubmitField("Criar conta")

    def validate_email(self, email):
        usuario = User.query.filter_by(email = email.data).first()
        # Se existe usuário
        if usuario:
            raise ValidationError("Email já cadastrado")

class FormFoto(FlaskForm):
    foto = FileField("Foto", validators=[DataRequired()])
    confirm_button = SubmitField('Enviar')