from flask import Blueprint, render_template
from .service import get_recompensas_usuario, dar_recompensa
from flask_login import current_user

bp_recompensas = Blueprint('recompensas', __name__, url_prefix='/recompensas',
                           template_folder='templates', static_folder='static')


@bp_recompensas.route('/')
def index():
    recompensas = get_recompensas_usuario(current_user.nombre)
    return render_template('recompensas.html', recompensas=recompensas)


@bp_recompensas.route('/dar')
def dar():
    dar_recompensa(current_user.nombre)
    return 'Recompensa dada'
