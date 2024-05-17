from flask import Blueprint, render_template, request, redirect, url_for
from game_data_loader import salas_grupos_csv

bp_desplazamiento = Blueprint('desplazamiento', __name__, url_prefix='/desplazamiento',
                              template_folder='templates', static_folder='static')


@bp_desplazamiento.route('/')
def index():
    salas = salas_grupos_csv.get_salas_by_grupo()
    return render_template('desplazamiento.html', salas_by_grupo=salas.items())
