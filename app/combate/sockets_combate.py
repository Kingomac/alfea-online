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

        # Si el usuario está vivo se permite el ataque
        if incombat.get_participant_by_nombre(data['usuarioNombre']).vida > 0:
            incombat.ataquesTurno.append(AtaqueTurno(
                data["ataqueId"], data["usuarioNombre"], data["objetivoNombre"]))

        # Comprobar que todos los participantes han atacado
        num_vivos_no_npcs = sum(1 for x in incombat.heroes if x.vida > 0 and not x.is_npc) + \
            sum(1 for x in incombat.villanos if x.vida > 0 and not x.is_npc)
        print(f"{num_vivos_no_npcs=}")
        print(f"{len(incombat.ataquesTurno)=}")

        if len(incombat.ataquesTurno) == num_vivos_no_npcs:

            # Ataques de NPCs
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

            mensajes = []
            # Gestión de escudos
            escudos = {}
            for x in incombat.ataquesTurno:
                ataque = ataques_csv.get_by_id(x.ataque)
                escudos[x.usuario] = (
                    ataque.defensa_fisica, ataque.defensa_magica)
                if ataque.defensa_fisica > 0:
                    mensajes.append(
                        f"{x.usuario} ha activado un escudo físico de {ataque.defensa_fisica} de potencia")
                if ataque.defensa_magica > 0:
                    mensajes.append(
                        f"{x.usuario} ha activado un escudo mágico de {ataque.defensa_magica} de potencia")

            def get_escudo_objetivo(objetivo):
                return escudos[objetivo] if objetivo in escudos else (0, 0)

            # Ordernar ataques turno por velocidad de ataque
            incombat.ataquesTurno.sort(key=lambda x: incombat.get_participant_by_nombre(
                x.usuario).combat_stats.velocidad, reverse=True)

            # Calcular daños de cada ataque
            for x in incombat.ataquesTurno:
                ataque = ataques_csv.get_by_id(x.ataque)
                atacante = incombat.get_participant_by_nombre(x.usuario)
                objetivo = incombat.get_participant_by_nombre(x.objetivo)

                # Restar maná
                atacante.mana -= ataque.coste_mana

                # Si atacas sin maná te haces daño
                if atacante.mana < 0:
                    atacante.vida += atacante.mana * 1.16
                    mensajes.append(
                        f"{atacante.nombre} se ha hecho {atacante.mana * 1.16} de daño por atacar sin maná")

                # Inflingir daño a objetivo
                if objetivo.vida > 0:
                    dano = ataque.ataque_fisico + \
                        atacante.combat_stats.poder_fisico - \
                        get_escudo_objetivo(x.objetivo)[0]
                    dano += ataque.ataque_magico + \
                        atacante.combat_stats.poder_magico - \
                        get_escudo_objetivo(x.objetivo)[1]
                    objetivo.vida -= dano
                    mensajes.append(
                        f"{atacante.nombre} ha hecho {dano} de daño a {objetivo.nombre}")
                    if objetivo.vida < 0:
                        objetivo.vida = 0
                        mensajes.append(f"{objetivo.nombre} ha muerto")

            # Enviar actualización a los clientes
            socketio.emit(f'nuevo_turno_{data['idCombate']}', {'combate': incombat.__dict__(), 'mensajes': mensajes},
                          namespace='/combate')

            # Reset estado turno
            incombat.npc_han_atacado = False
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

        incombat.save()
