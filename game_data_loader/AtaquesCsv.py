from .BaseCsvFile import BaseCsvFile
from .model import Ataque


class AtaquesCsv(BaseCsvFile):
    def __init__(self):
        super().__init__('game_data/combate/ataques.csv')

    def get_by_id(self, ataque_id):
        datos = next(
            (ataque for ataque in self.rows if ataque['id'] == ataque_id), None)
        # id;nombre;ataque_fisico;ataque_magico;defensa_fisica;defensa_magica;precision;coste_mana;prob_critico;lanzamiento;forma;descripcion
        return Ataque(datos['id'], datos['nombre'], int(datos['ataque_fisico']), int(datos['ataque_magico']), int(datos['defensa_fisica']), int(datos['defensa_magica']), int(datos['precision']), int(datos['coste_mana']), int(datos['prob_critico']), datos['lanzamiento'], datos['forma'], datos['descripcion'])

    def get_choices_iniciales(self):
        return [(datos['id'], datos['nombre']) for datos in self.rows[:12]]

    def get_all(self):
        return [Ataque(datos['id'], datos['nombre'], int(datos['ataque_fisico']), int(datos['ataque_magico']), int(datos['defensa_fisica']), int(datos['defensa_magica']), int(datos['precision']), int(datos['coste_mana']), int(datos['prob_critico']), datos['lanzamiento'], datos['forma'], datos['descripcion']) for datos in self.rows]


ataques_csv = AtaquesCsv()
