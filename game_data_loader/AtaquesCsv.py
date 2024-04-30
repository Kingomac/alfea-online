from .BaseCsvFile import BaseCsvFile
from .model import Ataque


class AtaquesCsv(BaseCsvFile):
    def __init__(self):
        super().__init__('game_data/combate/ataques.csv')

    def get_by_id(self, ataque_id):
        datos = next(
            (ataque for ataque in self.rows if ataque['id'] == ataque_id), None)
        return Ataque(**datos)


ataques_csv = AtaquesCsv()
