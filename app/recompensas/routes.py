from flask import Blueprint, render_template, redirect
from .service import get_recompensas_usuario, reclamar_recompensas
from flask_login import current_user

bp_recompensas = Blueprint('recompensas', __name__, url_prefix='/recompensas',
                           template_folder='templates', static_folder='static')


@bp_recompensas.route('/')
def index():
    recompensas = get_recompensas_usuario(current_user.nombre)
    return render_template('recompensas.html', recompensas=recompensas)


@bp_recompensas.route('/reclamar')
def reclamar():
    total = reclamar_recompensas(current_user.nombre)
    return render_template('reclamar.html', total=total)
