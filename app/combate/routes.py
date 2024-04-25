from flask import Blueprint, render_template
from game_data_loader import salas_csv, raids_csv, npc_csv

bp_combate = Blueprint('combate', __name__, url_prefix='/combate', template_folder='templates', static_folder='static')


@bp_combate.route('/lobby/raid/<id_raid>')
def lobby_raid(id_raid):
    datos_raid = raids_csv.get_by_id(id_raid)
    datos_sala = salas_csv.get_by_alias(datos_raid['sala'])
    heroes = npc_csv.getm_npc_by_id(datos_raid['heroes'].split(','))
    villanos = npc_csv.getm_npc_by_id(datos_raid['villanos'].split(','))
    return render_template('lobby.html', heroes=heroes, villanos=villanos, datos_sala=datos_sala)


@bp_combate.route('/lobby/duelo/<usr1>/<usr2>')
def duelo():
    return 'Lobby de duelo'
