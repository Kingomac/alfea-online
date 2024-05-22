from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user
from .service import mejorar_estadisticas, get_ataques_con_precios, comprar_ataque
from app.usuarios.model import CombatStats
from app.ataque.service import get_ids_ataques_usuario
import json


bp_tienda = Blueprint(
    'tienda', __name__, url_prefix='/tienda', template_folder='templates')


@bp_tienda.route('/experiencia', methods=['GET'])
def mejorar_estadisticas_get():
    combat_stats = current_user.get_combate_stats()
    return render_template('mejorar_estadisticas.html', combat_stats=combat_stats)


@bp_tienda.route('/experiencia', methods=['POST'])
def mejorar_estadisticas_post():
    if request.content_type != 'application/json':
        return {'error': 'Content-Type must be application/json'}, 400
    nuevas_combat_stats = {
        'vida_maxima': int(request.json['vida_maxima']),
        'mana_maximo': int(request.json['mana_maximo']),
        'poder_fisico': int(request.json['poder_fisico']),
        'poder_magico': int(request.json['poder_magico']),
        'resistencia_fisica': int(request.json['resistencia_fisica']),
        'resistencia_magica': int(request.json['resistencia_magica']),
        'velocidad': int(request.json['velocidad'])
    }
    return json.dumps(mejorar_estadisticas(current_user, CombatStats(**nuevas_combat_stats)))


@bp_tienda.route('/ataques', methods=['GET'])
def tienda_ataques_get():
    ataques_totales = get_ataques_con_precios()
    ataques_usuario = get_ids_ataques_usuario(current_user.nombre)
    dif = [x for x in ataques_totales if x['ataque'].id not in ataques_usuario]
    return render_template('tienda_ataques.html', ataques=dif)


@bp_tienda.route('/ataques', methods=['POST'])
def tienda_ataques_post():
    if request.content_type != 'application/json':
        return {'error': 'Content-Type must be application/json'}, 400
    ataque_id = request.json['ataque_id']
    return json.dumps(comprar_ataque(current_user, ataque_id))
