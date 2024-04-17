from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for
from db import redis_db
from .ChatForm import ChatForm
from .model import Mensaje
import json
import flask_login

bp_chat = Blueprint('chat', __name__, url_prefix='/chat', template_folder='templates')

"""
async def handle_mensaje_nuevo(mensaje, sala):
    clave = f"chat:{sala}:{datetime.now().timestamp()}"
    redis_db.set(clave, json.dumps(Mensaje(mensaje).__dict__()))
    redis_db.expire(clave, 7200)
    for cliente in clientes[sala]:
        await cliente.send(json.dumps(
            {'mensaje': mensaje, 'usuario': flask_login.current_user.nombre, 'timestamp': datetime.now().timestamp()}))

"""

"""
@socketio.on('mensaje_nuevo')
def handle_mensaje_nuevo(mensaje, sala):
    clave = f"chat:{sala}:{datetime.now().timestamp()}"
    redis_db.set(clave, json.dumps(Mensaje(mensaje).__dict__()))
    redis_db.expire(clave, 7200)
    emit('mensaje_nuevo', json.dumps(Mensaje(mensaje).__dict__()), room=sala)
"""


@bp_chat.route('/sala/<sala>', methods=['GET', 'POST'])
@flask_login.login_required
def chat_sala(sala):
    form = ChatForm()
    if form.validate_on_submit():
        # emit('mensaje_nuevo', form.mensaje.data, sala)
        return redirect(url_for('chat.chat_sala', sala=sala))
    else:
        claves = redis_db.keys(f"chat:{sala}:*")
        mensajes = [Mensaje(timestamp=clave.decode().split(':')[-1], **json.loads(redis_db.get(clave.decode()))) for
                    clave in claves]
        mensajes.sort(key=lambda x: x.timestamp)
        return render_template('chat.html', sala=sala, mensajes=mensajes, form=form)


@bp_chat.route('/privado/<usr1>/<usr2>', methods=['GET', 'POST'])
def chat_privado(usr1, usr2):
    return 'Chat privado'
