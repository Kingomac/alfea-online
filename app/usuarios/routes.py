from flask import Blueprint
from .RegistroForm import RegistroForm
from .InicioSesionForm import InicioSesionForm
from flask import render_template

bp_usuarios = Blueprint('usuarios', __name__, url_prefix='/', template_folder='templates')


@bp_usuarios.route('/registro', methods=['GET', 'POST'])
def registro():
    form = RegistroForm()
    if form.validate_on_submit():
        return 'Usuario registrado'
    return render_template('registro.html', form=form)


@bp_usuarios.route('/')
def index():
    form = InicioSesionForm()
    return render_template('login.html', form=form)
