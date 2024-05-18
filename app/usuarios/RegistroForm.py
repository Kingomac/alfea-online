from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, SelectMultipleField, ValidationError
from wtforms.validators import DataRequired
from flask_wtf.file import FileAllowed
from game_data_loader import ataques_csv


class ComprobarAtaques:
    def __init__(self, message=None):
        if not message:
            message = 'Selecciona 4 ataques normales y una convergencia'
        self.message = message

    def __call__(self, form, field):
        if len(field.data) != 5:
            raise ValidationError(self.message)
        normales = 0
        convergencia = 0
        for x in field.data:
            data = ataques_csv.get_by_id(x)
            if data.lanzamiento == 'normal':
                normales += 1
            else:
                convergencia += 1
        if normales != 4 or convergencia != 1:
            raise ValidationError(self.message)


class RegistroForm(FlaskForm):
    nombre = StringField('Nombre de usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    foto_perfil = FileField('Foto de perfil', validators=[
                            FileAllowed(['webp'], "Solo imágenes webp")])
    ataques = SelectMultipleField(
        'Ataques', choices=ataques_csv.get_choices_iniciales(), validators=[DataRequired(), ComprobarAtaques()])
    submit = SubmitField('Registrarse')
