from db import redis_db
from app.usuarios.model import Usuario
from game_data_loader import ataques_csv, npc_csv
from game_data_loader.model import Npc
from app.usuarios.model import CombatStats


class InCombatParticipant:
    def __init__(self, nombre: str, vida: int, mana: int, combat_stats: CombatStats, id_npc: str = None):
        self.nombre = nombre
        self.id_npc = id_npc
        self.vida = vida
        self.mana = mana
        self.combat_stats = combat_stats

    @property
    def is_npc(self):
        return self.id_npc != None

    @staticmethod
    def from_usuario(usr: Usuario):
        stats = usr.get_combate_stats()
        return InCombatParticipant(usr.nombre, stats.vida_maxima, stats.mana_maximo, stats)

    @staticmethod
    def from_npc(npc: Npc):
        return InCombatParticipant(npc.nombre, npc.vida_maxima, npc.mana_maximo, CombatStats(npc.vida_maxima, npc.mana_maximo, npc.poder_fisico, npc.poder_magico, npc.resistencia_fisica, npc.resistencia_magica, npc.velocidad), npc.id)

    def get_ataques_equipados(self):
        if self.is_npc:
            return list(map(ataques_csv.get_by_id, npc_csv.get_npc_by_id(self.id_npc)["ataques"].split(",")))
        return list(map(ataques_csv.get_by_id, redis_db.smembers(f"ataques_equipados:{self.nombre}")))

    @staticmethod
    def load_usuario(nombre_usuario: str):
        return InCombatParticipant.from_usuario(Usuario.find_by_name(nombre_usuario))

    @staticmethod
    def load_npc(id_npc: str):
        return InCombatParticipant.from_npc(npc_csv.npc_from_dict(npc_csv.get_npc_by_id(id_npc)))

    @staticmethod
    def from_combat(nombre: str, vida: int, mana: int, id_npc: str = None):
        if id_npc:
            npc = InCombatParticipant.load_npc(id_npc)
            npc.vida = vida
            npc.mana = mana
            return npc
        usr = InCombatParticipant.load_usuario(nombre)
        usr.vida = vida
        usr.mana = mana
        return usr

    def __dict__(self):
        return {
            "nombre": self.nombre,
            "id_npc": self.id_npc,
            "vida": self.vida,
            "mana": self.mana
        }
