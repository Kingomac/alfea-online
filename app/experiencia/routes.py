from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user
from .service import mejorar_estadisticas
from app.usuarios.model import CombatStats
import json


bp_experiencia = Blueprint(
    'experiencia', __name__, url_prefix='/experiencia', template_folder='templates')


@bp_experiencia.route('/mejorar-estadisticas', methods=['GET'])
def mejorar_estadisticas_get():
    combat_stats = current_user.get_combate_stats()
    return render_template('mejorar_estadisticas.html', combat_stats=combat_stats)


@bp_experiencia.route('/mejorar-estadisticas', methods=['POST'])
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
