from flask import Blueprint, request
from db.util import decode_hgetall
from .RegistroForm import RegistroForm
from .InicioSesionForm import InicioSesionForm
from flask import render_template, redirect, url_for
from db import redis_db
import werkzeug.security as ws
import flask_login
from game_data_loader import salas_csv
from .model import CombatStats, Usuario

bp_usuarios = Blueprint('usuarios', __name__,
                        url_prefix='/', template_folder='templates')


@bp_usuarios.route('/registro', methods=['GET', 'POST'])
def registro():
    form = RegistroForm()
    if form.validate_on_submit():
        if redis_db.exists(f"usuario:{form.nombre.data}") > 0:
            return 'Usuario ya registrado'
        usuario = Usuario(form.nombre.data, ws.generate_password_hash(form.password.data), experiencia=0,
                          monedas=50, titulo_nobiliario='', matrimonio='', sala_actual=1, combate_stats_str=str(CombatStats.get_default()))
        redis_db.hmset(f"usuario:{form.nombre.data}", usuario.__dict__)
        redis_db.sadd(f'ataques:{usuario.nombre}', *form.ataques.data)
        redis_db.sadd(f'ataques_equipados:{
                      usuario.nombre}', *form.ataques.data)
        form.foto_perfil.data.save(
            'static/img/fotos_perfil/' + form.nombre.data + '.webp')
        return redirect(url_for('usuarios.index'))
    return render_template('registro.html', form=form)


@bp_usuarios.route('/', methods=['GET', 'POST'])
def index():
    if flask_login.current_user.is_authenticated:
        alias = salas_csv.get_by_id(
            str(flask_login.current_user.sala_actual))['alias']
        return redirect(url_for('salas.lugar', alias=alias))
    form = InicioSesionForm()
    if form.validate_on_submit():
        dbusr = decode_hgetall(redis_db.hgetall(f"usuario:{form.nombre.data}"))
        if dbusr:
            usr = Usuario(**dbusr)
            if usr.check_password(form.password.data):
                flask_login.login_user(usr)
                print(f"{usr.sala_actual=}")
                alias = salas_csv.get_by_id(str(usr.sala_actual))['alias']
                print(f"{url_for('salas.lugar', alias=alias)=}")
                return redirect(url_for('salas.lugar', alias=alias))
            form.errors = {'nombre': [u'Contraseña incorrecta']}
        else:
            form.errors = {'nombre': [u'Usuario no registrado']}
    print(f"{form.errors=}")
    return render_template('login.html', form=form)
