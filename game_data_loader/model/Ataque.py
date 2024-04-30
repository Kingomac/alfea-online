class Ataque:
    # id;nombre;ataque_fisico;ataque_magico;defensa_fisica;defensa_magica;precision;coste_mana;prob_critico;lanzamiento;forma;descripcion
    def __init__(self, id: str, nombre: str, ataque_fisico: int, ataque_magico: int, defensa_fisica: int, defensa_magica: int, precision: int, coste_mana: int, prob_critico: int, lanzamiento: str, forma: str, descripcion: str) -> None:
        self.__id = id
        self.__nombre = nombre
        self.__ataque_fisico = ataque_fisico
        self.__ataque_magico = ataque_magico
        self.__defensa_fisica = defensa_fisica
        self.__defensa_magica = defensa_magica
        self.__precision = precision
        self.__coste_mana = coste_mana
        self.__prob_critico = prob_critico
        self.__lanzamiento = lanzamiento
        self.__forma = forma
        self.__descripcion = descripcion

    @property
    def id(self):
        return self.__id

    @property
    def nombre(self):
        return self.__nombre

    @property
    def ataque_fisico(self):
        return self.__ataque_fisico

    @property
    def ataque_magico(self):
        return self.__ataque_magico

    @property
    def defensa_fisica(self):
        return self.__defensa_fisica

    @property
    def defensa_magica(self):
        return self.__defensa_magica

    @property
    def precision(self):
        return self.__precision

    @property
    def coste_mana(self):
        return self.__coste_mana

    @property
    def prob_critico(self):
        return self.__prob_critico

    @property
    def lanzamiento(self):
        return self.__lanzamiento

    @property
    def forma(self):
        return self.__forma

    @property
    def descripcion(self):
        return self.__descripcion
