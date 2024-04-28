
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
