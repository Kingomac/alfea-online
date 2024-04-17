from flask import Blueprint, render_template, send_from_directory
from game_data_loader import salas_csv

bp_salas = Blueprint('salas', __name__, url_prefix='/salas', template_folder='templates', static_folder='static')


@bp_salas.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)


@bp_salas.route('/<alias>')
def sala(alias):
    datos_sala = salas_csv.get_sala(alias)
    print(f"{datos_sala=}")
    return render_template('sala.html', **datos_sala)
