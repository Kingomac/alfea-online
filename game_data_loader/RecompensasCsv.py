from .BaseCsvFile import BaseCsvFile
from .model import Recompensa
import random


class RecompensasCsv(BaseCsvFile):
    def __init__(self):
        super().__init__('game_data/recompensas.csv')

    def getm_by_id(self, ids: list[str]) -> tuple[Recompensa]:
        return tuple(map(lambda id: next(Recompensa(x['id'], int(x['experiencia']), int(x['monedas'])) for x in self.rows if x['id'] == id), ids))

    def get_random(self):
        rec = random.choice(self.rows)
        return Recompensa(rec['id'], int(rec['experiencia']), int(rec['monedas']))


recompensas_csv = RecompensasCsv()
