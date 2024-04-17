from datetime import datetime
import json
from app.chat.model import Mensaje
from db import redis_db

from flask_socketio import SocketIO, join_room, leave_room, emit


def registar_sockets(socketio: SocketIO):
    @socketio.on('conectar_sala')
    def conectar_sala(sala):
        print(f"Conectado a la sala {sala}")
        join_room(sala)

    @socketio.on('desconectar_sala')
    def desconectar_sala(sala):
        print(f"Desconectado de la sala {sala}")
        leave_room(sala)

    def guardar_mensaje(data) -> tuple[Mensaje, str, str]:
        data = json.loads(data)
        sala, mensaje, usuario, timestamp = data['sala'], data['mensaje'], data['usuario'], datetime.now().timestamp()
        clave = f"chat:{sala}:{timestamp}"
        obj_mensaje = Mensaje(mensaje=mensaje, usuario=usuario, timestamp=timestamp)
        redis_db.set(clave, json.dumps(obj_mensaje.__dict__()))
        return obj_mensaje, clave, sala

    @socketio.on('mensaje_nuevo_sala')
    def handle_mensaje_nuevo(data):
        obj_mensaje, clave, sala = guardar_mensaje(data)
        redis_db.expire(clave, 7200)
        emit('mensaje_nuevo',
             {'mensaje': obj_mensaje.mensaje, 'usuario': obj_mensaje.usuario,
              'fecha_bonita': obj_mensaje.get_fecha_bonita()},
             broadcast=True, room=sala)

    @socketio.on('mensaje_nuevo_priv')
    def handle_mensaje_nuevo_privado(data):
        obj_mensaje, clave, sala = guardar_mensaje(data)
        emit('mensaje_nuevo',
             {'mensaje': obj_mensaje.mensaje, 'usuario': obj_mensaje.usuario,
              'fecha_bonita': obj_mensaje.get_fecha_bonita()},
             broadcast=True, room=sala)
