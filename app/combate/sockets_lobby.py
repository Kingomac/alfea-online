from flask_socketio import SocketIO
from db import redis_db
import json


def registrar_sockets_lobby_combate(socketio: SocketIO):

    @socketio.on('unirse_bando', namespace='/lobby_combate')
    def unirse_bando(data):
        bando, id_raid, usuario = data['bando'], data['id_raid'], data['usuario']
        redis_db.sadd(f'lobby_combate:{id_raid}:{bando}', usuario)
        socketio.emit(f'actualizar_lobby_{id_raid}', {'bando': bando, 'usuarios': [x.decode() for x in redis_db.smembers(
            f'lobby_combate:{id_raid}:{bando}')]}, namespace='/lobby_combate')
        print(f'Usuario {usuario} se unió al bando {bando} del raid {id_raid}')
