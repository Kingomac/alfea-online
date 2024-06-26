from flask import Blueprint, redirect, render_template, url_for
from game_data_loader import salas_csv, raids_csv, npc_csv
from db import redis_db
from app.usuarios.model import CombatStats
from flask_login import current_user
from app.chat import get_mensajes_sala
from app.ataque.service import get_ataques_equipados_usuario
from app.combate.model import InCombat
from flask_login import login_required

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
@login_required
def lobby_raid(id_raid):
    datos_raid = raids_csv.get_by_id(id_raid)
    heroes = npc_csv.getm_npc_by_id(datos_raid['heroes'].split(','))
    villanos = npc_csv.getm_npc_by_id(datos_raid['villanos'].split(','))
    usuarios_heroes = add_usuarios_listlobby(id_raid, 'heroes', heroes)
    usuarios_villanos = add_usuarios_listlobby(id_raid, 'villanos', villanos)
    puede_unirse = current_user.nombre not in usuarios_heroes and current_user.nombre not in usuarios_villanos
    mensajes = get_mensajes_sala(f'raid-{id_raid}')
    return render_template('lobby.html', nombre_raid=datos_raid['nombre'], n_heroes=len(usuarios_heroes), n_villanos=len(usuarios_villanos), puede_unirse=puede_unirse, heroes=heroes, villanos=villanos, id_raid=id_raid, mensajes=mensajes)


@bp_combate.route('/combate/<id_combate>')
@login_required
def combate(id_combate):
    if not InCombat.tiene_acceso(current_user.nombre, id_combate):
        return redirect(url_for('usuarios.index'))
    ataques_equipados = get_ataques_equipados_usuario(current_user.nombre)
    incombat = InCombat.load(id_combate)
    es_heroe = any(
        map(lambda x: x.nombre == current_user.nombre, incombat.heroes))
    es_villano = not es_heroe
    return render_template('combate.html', id_combate=id_combate, heroes=incombat.heroes, villanos=incombat.villanos, ataques=ataques_equipados, es_heroe=es_heroe, es_villano=es_villano)


@bp_combate.route('/lobby/duelo/<usr1>/<usr2>')
def duelo():
    return 'Lobby de duelo'


@bp_combate.route('/raids')
def raids():
    raids = {}
    for raid in raids_csv.rows:
        heroes = npc_csv.getm_npc_by_id(raid['heroes'].split(','))
        villanos = npc_csv.getm_npc_by_id(raid['villanos'].split(','))
        raids[raid['id']] = {
            'nombre': raid['nombre'],
            'heroes': heroes,
            'villanos': villanos
        }

    return render_template('raids.html', raids=raids)
