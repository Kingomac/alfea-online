from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class ChatForm(FlaskForm):
    mensaje = StringField('Mensaje', validators=[DataRequired()])
    submit = SubmitField('Enviar')
