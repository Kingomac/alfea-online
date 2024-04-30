from .Ataque import Ataque
from ..AtaquesCsv import ataques_csv


class Npc:
    def __init__(self, id: str, nombre: str, vida_maxima: int, mana_maximo: int, poder_fisico: int, poder_magico: int, resistencia_fisica: int, resistencia_magica: int, velocidad: int, ataques: list[Ataque]) -> None:
        self.__id = id
        self.__nombre = nombre
        self.__vida_maxima = vida_maxima
        self.__mana_maximo = mana_maximo
        self.__poder_fisico = poder_fisico
        self.__poder_magico = poder_magico
        self.__resistencia_fisica = resistencia_fisica
        self.__resistencia_magica = resistencia_magica
        self.__velocidad = velocidad
        self.__ataques = ataques

    @property
    def id(self):
        return self.__id

    @property
    def nombre(self):
        return self.__nombre

    @property
    def vida_maxima(self):
        return self.__vida_maxima

    @property
    def mana_maximo(self):
        return self.__mana_maximo

    @property
    def poder_fisico(self):
        return self.__poder_fisico

    @property
    def poder_magico(self):
        return self.__poder_magico

    @property
    def resistencia_fisica(self):
        return self.__resistencia_fisica

    @property
    def resistencia_magica(self):
        return self.__resistencia_magica

    @property
    def velocidad(self):
        return self.__velocidad

    @property
    def ataques(self):
        return self.__ataques
