from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for
from db import redis_db
from .model import Mensaje
import json
import flask_login

bp_chat = Blueprint('chat', __name__, url_prefix='/chat', template_folder='templates')


@bp_chat.route('/sala/<sala>')
@flask_login.login_required
def chat_sala(sala):
    claves = redis_db.keys(f"chat:{sala}:*")
    mensajes = get_mensajes_from_keys(claves)
    return render_template('chat.html', sala=sala, mensajes=mensajes)


@bp_chat.route('/privado/<usr1>/<usr2>', methods=['GET', 'POST'])
def chat_privado(usr1, usr2):
    claves = redis_db.keys(f"chat:priv:{usr1}:{usr2}:*")
    sala = f"priv:{usr1}:{usr2}"
    mensajes = get_mensajes_from_keys(claves)
    return render_template('chat.html', sala=sala, mensajes=mensajes)


def get_mensajes_from_keys(claves):
    mensajes = [Mensaje(timestamp=clave.decode().split(':')[-1], **json.loads(redis_db.get(clave.decode()))) for
                clave in claves]
    mensajes.sort(key=lambda x: x.timestamp)
    return mensajes
