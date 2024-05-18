from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user
from game_data_loader import salas_grupos_csv
from .service import desplazar_usuario

bp_desplazamiento = Blueprint('desplazamiento', __name__, url_prefix='/desplazamiento',
                              template_folder='templates', static_folder='static')


@bp_desplazamiento.route('/')
def index():
    salas = salas_grupos_csv.get_salas_by_grupo()
    return render_template('desplazamiento.html', salas_by_grupo=salas.items())


@bp_desplazamiento.route('/desplazar', methods=['POST'])
def desplazar():
    id_sala_destino = request.form.get('id_sala_destino')
    sala_destino = desplazar_usuario(current_user, id_sala_destino)
    return redirect(url_for('salas.lugar', alias=sala_destino['alias']))
