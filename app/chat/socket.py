from datetime import datetime
import json
from app.chat.model import Mensaje
from db import redis_db
from flask_socketio import SocketIO, join_room, leave_room, emit
from flask import request


def registar_sockets(socketio: SocketIO):
    @socketio.on('conectar_sala')
    def conectar_sala(data: str):
        data = json.loads(data)
        print(f"{request.sid=}")
        print(f"{data['usuario']} conectado a la sala {data['sala']}")
        join_room(data['sala'])
        redis_db.set(f"conexion-sala:{data['sala']}:{request.sid}", data['usuario'])
        emit(f'add_usuario_sala_{data["sala"]}', data['usuario'], broadcast=True)
        print(f'Emitiendo evento: add_usuario_sala_{data["sala"]}')

    @socketio.on('disconnect')
    def handle_disconnect():
        print(f"Desconectado {request.sid}")
        for key in redis_db.scan_iter(f"conexion-sala:*:{request.sid}"):
            sala = key.decode().split(':')[1]
            usuario = redis_db.get(key).decode()
            redis_db.delete(key)
            emit(f'rm_usuario_sala_{sala}', usuario, broadcast=True)

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

    @socketio.on('get_usuarios_en_sala')
    def get_usuarios_en_sala(sala):
        usuarios = list(socketio.server.manager.rooms[sala])
        emit('usuarios_en_sala', {'usuarios': usuarios})
