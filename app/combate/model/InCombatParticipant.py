from db import redis_db
from app.usuarios.model import Usuario
from game_data_loader import ataques_csv, npc_csv
from game_data_loader.model import Npc, Ataque
from app.ataque.service import get_ataques_equipados_usuario


class InCombatParticipant:
    def __init__(self, nombre: str, vida: int, mana: int, poder_fisico: int, poder_magico: int, resistencia_fisica: int, resistencia_magica: int, velocidad: int, id_npc: bool = None):
        self.nombre = nombre
        self.id_npc = id_npc
        self.vida = vida
        self.mana = mana
        self.poder_fisico = poder_fisico
        self.poder_magico = poder_magico
        self.resistencia_fisica = resistencia_fisica
        self.resistencia_magica = resistencia_magica
        self.velocidad = velocidad

    @property
    def is_npc(self):
        return self.id_npc != None

    @staticmethod
    def from_usuario(usr: Usuario):
        stats = usr.get_combate_stats()
        return InCombatParticipant(usr.nombre, stats.vida_maxima, stats.mana_maximo, stats.poder_fisico, stats.poder_magico, stats.resistencia_fisica, stats.resistencia_magica, stats.velocidad)

    @staticmethod
    def from_npc(npc: Npc):
        return InCombatParticipant(npc.nombre, npc.vida_maxima, npc.mana_maximo, npc.poder_fisico, npc.poder_magico, npc.resistencia_fisica, npc.resistencia_magica, npc.velocidad, npc.id)

    def get_ataques_equipados(self):
        return list(map(ataques_csv.get_by_id, redis_db.smembers(f"ataques_equipados:{self.nombre}")))

    def __str__(self) -> str:
        return f"{self.nombre},{self.is_npc},{self.vida},{self.mana},{self.poder_fisico},{self.poder_magico},{self.resistencia_fisica},{self.resistencia_magica},{self.velocidad}"

    @staticmethod
    def load_usuario(nombre_usuario: str):
        return InCombatParticipant.from_usuario(Usuario.load(nombre_usuario))

    @staticmethod
    def load_npc(id_npc: str):
        return InCombatParticipant.from_npc(npc_csv.npc_from_dict(npc_csv.get_npc_by_id(id_npc)))

    def __dict__(self):
        return {
            "nombre": self.nombre,
            "id_npc": self.id_npc,
            "vida": self.vida,
            "mana": self.mana,
            "poder_fisico": self.poder_fisico,
            "poder_magico": self.poder_magico,
            "resistencia_fisica": self.resistencia_fisica,
            "resistencia_magica": self.resistencia_magica,
            "velocidad": self.velocidad
        }
