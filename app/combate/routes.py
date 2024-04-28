from flask import Blueprint, render_template
from game_data_loader import salas_csv, raids_csv, npc_csv
from db import redis_db
from app.usuarios.model import CombatStats
from flask_login import current_user

bp_combate = Blueprint('combate', __name__, url_prefix='/combate',
                       template_folder='templates', static_folder='static')


def add_usuarios_listlobby(id_raid: str, bando: str, listlobby: list) -> list[str]:
    usuarios = list(map(lambda x: x.decode(), redis_db.smembers(
        f'lobby_combate:{id_raid}:{bando}')))

    for usuario in usuarios:
        datos = redis_db.hgetall(f'usuario:{usuario}')
        stats = CombatStats.from_str(datos[b'combate_stats_str'].decode())
        listlobby.append({
            'nombre': datos[b'nombre'].decode(),
            'vida_maxima': stats.vida_maxima,
            'mana_maximo': stats.mana_maximo,
            'poder_fisico': stats.poder_fisico,
            'poder_magico': stats.poder_magico,
            'resistencia_fisica': stats.resistencia_fisica,
            'resistencia_magica': stats.resistencia_magica
        })

    return usuarios


@bp_combate.route('/lobby/raid/<id_raid>')
def lobby_raid(id_raid):
    datos_raid = raids_csv.get_by_id(id_raid)
    datos_sala = salas_csv.get_by_alias(datos_raid['sala'])
    heroes = npc_csv.getm_npc_by_id(datos_raid['heroes'].split(','))
    villanos = npc_csv.getm_npc_by_id(datos_raid['villanos'].split(','))
    usuarios_heroes = add_usuarios_listlobby(id_raid, 'heroes', heroes)
    usuarios_villanos = add_usuarios_listlobby(id_raid, 'villanos', villanos)
    puede_unirse = current_user.nombre not in usuarios_heroes and current_user.nombre not in usuarios_villanos

    return render_template('lobby.html', n_heroes=len(usuarios_heroes), n_villanos=len(usuarios_villanos), puede_unirse=puede_unirse, heroes=heroes, villanos=villanos, datos_sala=datos_sala, id_raid=id_raid)


@bp_combate.route('/lobby/duelo/<usr1>/<usr2>')
def duelo():
    return 'Lobby de duelo'
