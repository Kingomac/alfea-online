class CombatStats:
    def __init__(self, vida_maxima: int, mana_maximo: int, poder_fisico: int, poder_magico: int, resistencia_fisica: int, resistencia_magica: int, velocidad: int) -> None:
        self.vida_maxima = vida_maxima
        self.mana_maximo = mana_maximo
        self.poder_fisico = poder_fisico
        self.poder_magico = poder_magico
        self.resistencia_fisica = resistencia_fisica
        self.resistencia_magica = resistencia_magica
        self.velocidad = velocidad

    @staticmethod
    def get_default():
        return CombatStats(vida_maxima=100, mana_maximo=100, poder_fisico=10, poder_magico=10, resistencia_fisica=10, resistencia_magica=10, velocidad=10)

    def __str__(self) -> str:
        return ",".join(map(str, [self.vida_maxima, self.mana_maximo, self.poder_fisico, self.poder_magico, self.resistencia_fisica, self.resistencia_magica]))

    @staticmethod
    def from_str(s: str):
        return CombatStats(*map(int, s.split(',')))
