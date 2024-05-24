from .BaseCsvFile import BaseCsvFile
from .SalasCsv import salas_csv


class SalasGruposCsv(BaseCsvFile):
    def __init__(self):
        super().__init__('game_data/salas_grupos.csv')

    def get_by_id(self, grupo_id):
        return next((grupo for grupo in self.rows if grupo['id'] == grupo_id), None)

    def group_by_grupo(self):
        salas = {}
        for sala in salas_csv.rows:
            if sala['grupo'] not in salas:
                salas[sala['grupo']] = {'nombre': self.get_by_id(
                    sala['grupo'])['nombre'], 'salas': []}
            salas[sala['grupo']]['salas'].append(sala)
        return salas


salas_grupos_csv = SalasGruposCsv()
