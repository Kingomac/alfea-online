from flask import Blueprint

from util import decode_hgetall
from .RegistroForm import RegistroForm
from .InicioSesionForm import InicioSesionForm
from flask import render_template, redirect, url_for
from db import redis_db
from .model import Usuario
import werkzeug.security as ws
import flask_login
from game_data_loader import salas_csv

bp_usuarios = Blueprint('usuarios', __name__, url_prefix='/', template_folder='templates')


@bp_usuarios.route('/registro', methods=['GET', 'POST'])
def registro():
    form = RegistroForm()
    if form.validate_on_submit():
        if redis_db.get(f"usuario:{form.nombre.data}") is not None:
            return 'Usuario ya registrado'
        usuario = Usuario(form.nombre.data, ws.generate_password_hash(form.password.data), nivel=1, experiencia=0,
                          monedas=0, foto_perfil='', titulo_nobiliario='', matrimonio='', sala_actual=1)
        redis_db.hmset(f"usuario:{form.nombre.data}", usuario.__dict__)
        return redirect(url_for('usuarios.index'))
    return render_template('registro.html', form=form)


@bp_usuarios.route('/', methods=['GET', 'POST'])
def index():
    form = InicioSesionForm()
    if form.validate_on_submit():
        dbusr = decode_hgetall(redis_db.hgetall(f"usuario:{form.nombre.data}"))
        print(f"{dbusr=}")
        if dbusr is None:
            return 'Login incorrecto'
        usr = Usuario(**dbusr)
        if not usr.check_password(form.password.data):
            return 'Login incorrecto'
        flask_login.login_user(usr)
        print(f"{usr.sala_actual=}")
        alias = salas_csv.get_by_id(str(usr.sala_actual))['alias']
        print(f"{url_for('ui.sala', alias=alias)=}")
        return redirect(url_for('ui.sala', alias=alias))
    return render_template('login.html', form=form)
