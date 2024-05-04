from flask_socketio import SocketIO
from app.combate.model import InCombat, AtaqueTurno
from game_data_loader import ataques_csv
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
        if incombat.get_participant_by_nombre(data['usuarioNombre']).vida <= 0:
            return
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

        # Comprobar que todos los participantes han atacado
        num_vivos = sum(1 for x in incombat.heroes if x.vida > 0) + \
            sum(1 for x in incombat.villanos if x.vida > 0)

        if len(incombat.ataquesTurno) == num_vivos:
            escudos = {}
            # Gestión de escudos
            for x in incombat.ataquesTurno:
                ataque = ataques_csv.get_by_id(x.id_ataque)
                escudos[x.id_usuario] = (
                    ataque.defensa_fisica, ataque.defensa_magica)

            for x in incombat.ataquesTurno:
                objetivo = incombat.get_participant_by_nombre(x.id_objetivo)
                if objetivo.vida > 0:
                    atacante = incombat.get_participant_by_nombre(x.id_usuario)
                    ataque = ataques_csv.get_by_id(x.id_ataque)
                    dano = ataque.ataque_fisico + \
                        atacante.combat_stats.poder_fisico - \
                        escudos[x.id_objetivo][0]
                    dano += ataque.ataque_magico + \
                        atacante.combat_stats.poder_magico - \
                        escudos[x.id_objetivo][1]
                    objetivo.vida -= dano
                    if objetivo.vida < 0:
                        objetivo.vida = 0

            # Limpiar ataques
            incombat.ataquesTurno = []

            # Determinar si el combate ha terminado
            num_heroes_vivos = sum(1 for x in incombat.heroes if x.vida > 0)
            num_villanos_vivos = sum(
                1 for x in incombat.villanos if x.vida > 0)
            if num_heroes_vivos == 0 or num_villanos_vivos == 0:
                ganadores = ''
                if num_heroes_vivos == 0 and num_villanos_vivos == 0:
                    ganadores = 'empate'
                elif num_heroes_vivos == 0:
                    ganadores = 'villanos'
                else:
                    ganadores = 'heroes'
                socketio.emit('fin_combate', {
                              'ganador': ganadores}, namespace='/combate')
                incombat.delete()
                return

            socketio.emit('nuevo_turno', incombat.__dict__(),
                          namespace='/combate')

        incombat.save()
