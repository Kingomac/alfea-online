from flask_socketio import SocketIO
from db import redis_db


def registrar_sockets_lobby_combate(socketio: SocketIO):

    @socketio.on('unirse_bando', namespace='/lobby_combate')
    def unirse_bando(data):
        bando, id_raid, usuario = data['bando'], data['id_raid'], data['usuario']
        redis_db.lpush(f'lobby_combate:{id_raid}:{bando}', usuario)
        socketio.emit(f'actualizar_lobby_{id_raid}', {'bando': bando, 'usuarios': redis_db.lrange(
            f'lobby_combate:{id_raid}:{bando}', 0, -1)})
        print(f'Usuario {usuario} se unió al bando {bando} del raid {id_raid}')
