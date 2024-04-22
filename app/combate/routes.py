from flask import Blueprint, render_template
from game_data_loader import salas_csv, raids_csv

bp_combate = Blueprint('combate', __name__, url_prefix='/combate', template_folder='templates', static_folder='static')


@bp_combate.route('/lobby/raid/<alias_sala>/<heroes>/vs/<villanos>')
def lobby_raid(alias_sala, heroes, villanos):
    datos_sala = salas_csv.get_by_alias(alias_sala)
    return render_template('raid.html', heroes=heroes, villanos=villanos, datos_sala=datos_sala)


@bp_combate.route('/lobby/duelo/<usr1>/<usr2>')
def duelo():
    return 'Lobby de duelo'
