import json

from flask import Blueprint, render_template, send_from_directory
from game_data_loader import salas_csv, movil_apps_csv
from db import redis_db
from app.chat import get_mensajes_from_keys

bp_salas = Blueprint('salas', __name__, url_prefix='/salas',
                     template_folder='templates', static_folder='static')


@bp_salas.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)


@bp_salas.route('/lugar/<alias>')
def lugar(alias):
    datos_sala = salas_csv.get_by_alias(alias)
    print(f"{datos_sala=}")

    claves = redis_db.keys(f"chat:{alias}:*")
    mensajes = get_mensajes_from_keys(claves)
    usuarios_sala = map(lambda x: redis_db.get(x).decode(),
                        redis_db.scan_iter(match=f"conexion-sala:{alias}:*"))
    print(f"{usuarios_sala=}")
    # tuple(map(lambda x: json.loads(x)['usuario'], redis_db.lrange(f"usuarios-sala:{alias}", 0, -1)))
    desplazamientos_cercanos = salas_csv.get_desplazamientos_cercanos(
        datos_sala['grupo'])

    return render_template('sala.html', sala=alias, mensajes=mensajes, movil_apps=movil_apps_csv.rows,
                           usuarios_sala=usuarios_sala, desplazamientos_cercanos=desplazamientos_cercanos, **datos_sala)
