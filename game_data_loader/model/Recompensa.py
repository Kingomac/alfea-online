from app.usuarios.model import CombatStats
from game_data_loader.AtaquesCsv import ataques_csv


class Recompensa:
    # readonly id;experiencia;monedas;combate_stats;ataque
    def __init__(self, id: str, experiencia: int, monedas: int, combat_stats: str, ataque: str) -> None:
        self.__id = id
        self.__experiencia = experiencia
        self.__monedas = monedas
        self.__combate_stats_str = combat_stats
        self.__ataque = ataque

    @property
    def id(self):
        return self.__id

    @property
    def experiencia(self):
        return self.__experiencia

    @property
    def monedas(self):
        return self.__monedas

    @property
    def combate_stats_str(self):
        return self.__combate_stats_str

    @property
    def combate_stats(self):
        return CombatStats.from_str(self.__combate_stats_str)

    @property
    def ataque(self):
        return self.__ataque

    @property
    def ataque_obj(self):
        return ataques_csv.get_by_id(self.__ataque)
