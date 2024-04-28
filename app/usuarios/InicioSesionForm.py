from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, ValidationError
from wtforms.validators import DataRequired
from db import redis_db
import werkzeug.security as ws


class ComprobarUsuarioRegistrado:
    def __init__(self, message=None):
        if not message:
            message = 'Usuario no registrado'
        self.message = message

    def __call__(self, form, field):
        if not redis_db.exists(f"usuario:{field.data}"):
            raise ValidationError(self.message)


class ComprobarUsuarioPassword:
    def __init__(self, message=None):
        if not message:
            message = 'Contraseña incorrecta'
        self.message = message

    def __call__(self, form, field):
        password = redis_db.hget(f"usuario:{form.nombre.data}", 'password')
        print(f"{password=}")
        print(f"{field.data=}")
        if not password or not ws.check_password_hash(password.decode(), form.password.data):
            raise ValidationError(self.message)


class InicioSesionForm(FlaskForm):
    nombre = StringField('Nombre de usuario', validators=[
                         DataRequired(), ComprobarUsuarioRegistrado(), ComprobarUsuarioPassword()])
    password = PasswordField('Contraseña', validators=[
                             DataRequired()])
    submit = SubmitField('Iniciar sesión')
