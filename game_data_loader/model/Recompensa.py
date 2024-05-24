from app.usuarios.model import CombatStats
from game_data_loader.AtaquesCsv import ataques_csv


class Recompensa:
    # readonly id;experiencia;monedas
    def __init__(self, id: str, experiencia: int, monedas: int) -> None:
        self.__id = id
        self.__experiencia = experiencia
        self.__monedas = monedas

    @property
    def id(self):
        return self.__id

    @property
    def experiencia(self):
        return self.__experiencia

    @property
    def monedas(self):
        return self.__monedas
