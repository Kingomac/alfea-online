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

        # Los NPCs atacan si no han atacado todavía
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
        print(f"{num_vivos=}")
        print(f"{len(incombat.ataquesTurno)=}")

        if len(incombat.ataquesTurno) == num_vivos:
            escudos = {}
            # Gestión de escudos
            for x in incombat.ataquesTurno:
                ataque = ataques_csv.get_by_id(x.id_ataque)
                escudos[x.id_usuario] = (
                    ataque.defensa_fisica, ataque.defensa_magica)

            def get_escudo_objetivo(objetivo):
                return escudos[objetivo] if objetivo in escudos else (0, 0)

            # Ordernar ataques turno por velocidad de ataque
            incombat.ataquesTurno.sort(key=lambda x: incombat.get_participant_by_nombre(
                x.id_usuario).combat_stats.velocidad, reverse=True)

            # Calcular daños de cada ataque
            for x in incombat.ataquesTurno:
                ataque = ataques_csv.get_by_id(x.id_ataque)
                atacante = incombat.get_participant_by_nombre(x.id_usuario)
                objetivo = incombat.get_participant_by_nombre(x.id_objetivo)

                # Restar maná
                atacante.mana -= ataque.coste_mana

                # Si atacas sin maná te haces daño
                if atacante.mana < 0:
                    atacante.vida *= 0.75

                # Inflingir daño a objetivo
                if objetivo.vida > 0:
                    dano = ataque.ataque_fisico + \
                        atacante.combat_stats.poder_fisico - \
                        get_escudo_objetivo(x.id_objetivo)[0]
                    dano += ataque.ataque_magico + \
                        atacante.combat_stats.poder_magico - \
                        get_escudo_objetivo(x.id_objetivo)[1]
                    objetivo.vida -= dano
                    if objetivo.vida < 0:
                        objetivo.vida = 0

            # Enviar actualización a los clientes
            socketio.emit(f'nuevo_turno_{data['idCombate']}', incombat.__dict__(),
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
