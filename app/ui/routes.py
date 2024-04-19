from flask import Blueprint, render_template, send_from_directory
from game_data_loader import salas_csv
from db import redis_db
from app.chat import get_mensajes_from_keys

bp_ui = Blueprint('ui', __name__, url_prefix='/ui', template_folder='templates', static_folder='static')


@bp_ui.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)


@bp_ui.route('/sala/<alias>')
def sala(alias):
    datos_sala = salas_csv.get_by_alias(alias)
    print(f"{datos_sala=}")

    claves = redis_db.keys(f"chat:{alias}:*")
    mensajes = get_mensajes_from_keys(claves)

    return render_template('sala.html', sala=alias, mensajes=mensajes, **datos_sala)
