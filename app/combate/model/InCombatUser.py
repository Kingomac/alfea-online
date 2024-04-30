from db import redis_db
from app.usuarios.model import Usuario
from game_data_loader import ataques_csv


class InCombatUser:
    def __init__(self, nombre: str, is_npc: bool, vida: int, mana: int, poder_fisico: int, poder_magico: int, resistencia_fisica: int, resistencia_magica: int, velocidad: int):
        self.nombre = nombre
        self.is_npc = is_npc
        self.vida = vida
        self.mana = mana
        self.poder_fisico = poder_fisico
        self.poder_magico = poder_magico
        self.resistencia_fisica = resistencia_fisica
        self.resistencia_magica = resistencia_magica
        self.velocidad = velocidad

    @staticmethod
    def from_usuario(usr: Usuario):
        stats = usr.get_combate_stats()
        return InCombatUser(usr.nombre, False, stats.vida_maxima, stats.mana_maximo, stats.poder_fisico, stats.poder_magico, stats.resistencia_fisica, stats.resistencia_magica, stats.velocidad)

    @staticmethod
    def from_npc_csv(npc):
        return InCombatUser(npc["nombre"], True, npc["vida_maxima"], npc["mana_maximo"], npc["poder_fisico"], npc["poder_magico"], npc["resistencia_fisica"], npc["resistencia_magica"], npc["velocidad"])

    def get_ataques_equipados(self):
        return list(map(ataques_csv.get_by_id, redis_db.smembers(f"ataques_equipados:{self.nombre}")))

    def __str__(self) -> str:
        return f"{self.nombre},{self.is_npc},{self.vida},{self.mana},{self.poder_fisico},{self.poder_magico},{self.resistencia_fisica},{self.resistencia_magica},{self.velocidad}"
