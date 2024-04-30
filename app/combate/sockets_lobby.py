from flask_socketio import SocketIO
from db import redis_db
from game_data_loader import raids_csv, npc_csv
from util import decode_hgetall
from app.usuarios import Usuario
from app.combate.model import InCombatUser


def registrar_sockets_lobby_combate(socketio: SocketIO):

    @socketio.on('unirse_bando', namespace='/lobby_combate')
    def unirse_bando(data):
        bando, id_raid, usuario = data['bando'], data['id_raid'], data['usuario']
        redis_db.sadd(f'lobby_combate:{id_raid}:{bando}', usuario)
        socketio.emit(f'actualizar_lobby_{id_raid}', {'bando': bando, 'usuarios': [x.decode() for x in redis_db.smembers(
            f'lobby_combate:{id_raid}:{bando}')]}, namespace='/lobby_combate')
        print(f'Usuario {usuario} se unió al bando {bando} del raid {id_raid}')

    @socketio.on('iniciar_combate', namespace='/lobby_combate')
    def iniciar_combate_raid(data):
        id_raid = data['id_raid']
        datos_raid = raids_csv.get_by_id(id_raid)

        def convertir_usuario_participante(nombre_usuario: str):
            usr = Usuario(
                **decode_hgetall(redis_db.hgetall(f'usuario:{nombre_usuario.decode()}')))
            return InCombatUser.from_usuario(usr)

        participantes = list(map(convertir_usuario_participante,
                             redis_db.smembers(f'lobby_combate:{id_raid}:villanos').union(redis_db.smembers(f'lobby_combate:{id_raid}:heroes'))))

        for p in ",".join((datos_raid['heroes'], datos_raid['villanos'])).split(','):
            datos_npc = npc_csv.get_npc_by_id(p)
            participantes.append(InCombatUser.from_npc_csv(datos_npc))

        print(f"{list(map(str, participantes))=}")
