from flask_socketio import SocketIO
from app.combate.model import InCombat, AtaqueTurno, InCombatParticipant
from game_data_loader import ataques_csv
from game_data_loader.model import Ataque
import random
import math
from .util import negativeIsZero


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
            print("Se han enviado todos los ataques, se procede a calcular el turno")

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
                ataque: Ataque = ataques_csv.get_by_id(x.ataque)
                acierta = random.random() * 100 < ataque.precision
                critico = random.random() * 100 < ataque.prob_critico
                porcentaje_critico = random.uniform(
                    1.01, 1.5) if critico else 1

                if acierta:
                    if critico:
                        escudos[x.usuario] = (
                            ataque.defensa_fisica * porcentaje_critico, ataque.defensa_magica * porcentaje_critico)
                    escudos[x.usuario] = (
                        ataque.defensa_fisica, ataque.defensa_magica)
                else:
                    escudos[x.usuario] = (0, 0)
                    mensajes.append(
                        f"{x.usuario} ha fallado el escudo {ataque.nombre}")
                if ataque.defensa_fisica > 0 and ataque.defensa_magica > 0 and critico:
                    mensajes.append(
                        f"{x.usuario} ha usado {ataque.nombre}, obtiene un escudo físico de {escudos[x.usuario][0]} y mágico de {escudos[x.usuario][1]} de potencia{f' que ha aumentado por su suerte un {int((porcentaje_critico-1)*100)}%'if critico else ''}")
                elif ataque.defensa_fisica > 0:
                    mensajes.append(
                        f"{x.usuario} ha usado {ataque.nombre}, obtiene un escudo físico de {escudos[x.usuario][0]} de potencia{f' que ha aumentado por su suerte un {int((porcentaje_critico-1)*100)}%'if critico else ''}")
                elif ataque.defensa_magica > 0:
                    mensajes.append(
                        f"{x.usuario} ha usado {ataque.nombre}, obtiene un escudo mágico de {escudos[x.usuario][0]} de potencia{f' que ha aumentado por su suerte un {int((porcentaje_critico-1)*100)}%'if critico else ''}")

            def get_escudo_objetivo(objetivo):
                return escudos[objetivo] if objetivo in escudos else (0, 0)

            # Ordernar ataques turno por velocidad de ataque
            incombat.ataquesTurno.sort(key=lambda x: incombat.get_participant_by_nombre(
                x.usuario).combat_stats.velocidad, reverse=True)

            # Calcular daños de cada ataque
            for x in incombat.ataquesTurno:
                ataque: Ataque = ataques_csv.get_by_id(x.ataque)
                atacante: InCombatParticipant = incombat.get_participant_by_nombre(
                    x.usuario)
                objetivo = incombat.get_participant_by_nombre(x.objetivo)

                acierta = random.random() * 100 < ataque.precision
                critico = random.random() * 100 < ataque.prob_critico
                porcentaje_critico = random.uniform(
                    1.01, 1.5) if critico else 1

                # Restar maná
                atacante.mana -= ataque.coste_mana

                # Si atacas sin maná te haces daño
                if atacante.mana < 0:
                    atacante.vida += atacante.mana * 1.16
                    mensajes.append(
                        f"{atacante.nombre} se ha hecho {abs(atacante.mana * 1.16)} de daño por usar {ataque.nombre} sin maná")

                # Inflingir daño a objetivo
                if objetivo.vida > 0:
                    if acierta:
                        # Sumar daño físico
                        dano = 0
                        if ataque.ataque_fisico > 0:
                            dano += math.sqrt(ataque.ataque_fisico) * math.log10(ataque.ataque_fisico) * atacante.combat_stats.poder_fisico / math.sqrt(
                                1 + atacante.combat_stats.poder_fisico) - get_escudo_objetivo(x.objetivo)[0] - objetivo.combat_stats.resistencia_fisica / math.sqrt(objetivo.combat_stats.resistencia_fisica + 1)
                        if ataque.ataque_magico > 0:
                            dano += math.sqrt(ataque.ataque_magico) * math.log10(ataque.ataque_magico) * atacante.combat_stats.poder_magico / math.sqrt(
                                1 + atacante.combat_stats.poder_magico) - get_escudo_objetivo(x.objetivo)[1] - objetivo.combat_stats.resistencia_magica / math.sqrt(objetivo.combat_stats.resistencia_magica + 1)
                        dano *= porcentaje_critico
                        dano = math.floor(max(dano, 0))
                        objetivo.vida -= dano
                        if dano > 0:
                            mensajes.append(
                                f"{atacante.nombre} ha usado {ataque.nombre} y ha hecho {dano} de daño a {objetivo.nombre}{f' que por ser crítico ha infligido un {int((porcentaje_critico-1)*100)}% de daño adicional'if critico else ''}")
                        elif ataque.ataque_fisico > 0 or ataque.ataque_magico > 0:
                            mensajes.append(
                                f"El escudo de {objetivo.nombre} ha parado completamente el {ataque.nombre} de {atacante.nombre}")
                        if objetivo.vida < 0:
                            objetivo.vida = 0
                            mensajes.append(f"{objetivo.nombre} ha muerto")
                    else:
                        if ataque.ataque_fisico > 0 or ataque.ataque_magico > 0:
                            mensajes.append(
                                f"{atacante.nombre} ha fallado el ataque {ataque.nombre}")

            # Enviar actualización a los clientes
            socketio.emit(f'nuevo_turno_{data['idCombate']}', {'combate': incombat.__dict__(), 'mensajes': mensajes},
                          namespace='/combate')

            # Reset estado turno
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
