from flask_socketio import SocketIO
from app.combate.model import InCombat, AtaqueTurno
import random


def registrar_sockets_combate(socketio: SocketIO):
    @socketio.on('connect', namespace='/combate')
    def connect():
        print('Usuario conectado a la sala de combate')

    @socketio.on('atacar', namespace='/combate')
    def atacar(data):
        # usuario, id_ataque, id_combate, objetivo
        print(f"{data=}")
        incombat = InCombat.load(data['idCombate'])
        incombat.ataquesTurno.append(AtaqueTurno(
            data["ataqueId"], data["usuarioNombre"], data["objetivoNombre"]))
        if not incombat.npc_han_atacado:
            for villano in incombat.villanos:
                if villano.is_npc:
                    ataque = random.choice(villano.get_ataques_equipados())
                    incombat.ataquesTurno.append(AtaqueTurno(
                        ataque.id, villano.nombre, random.choice(incombat.heroes).nombre))

            for heroe in incombat.heroes:
                if heroe.is_npc:
                    ataque = random.choice(heroe.get_ataques_equipados())
                    incombat.ataquesTurno.append(AtaqueTurno(
                        ataque.id, heroe.nombre, random.choice(incombat.villanos).nombre))
            incombat.npc_han_atacado = True
