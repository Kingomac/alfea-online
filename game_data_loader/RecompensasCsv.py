from .BaseCsvFile import BaseCsvFile
from .model import Recompensa


class RecompensasCsv(BaseCsvFile):
    def __init__(self):
        super().__init__('game_data/recompensas.csv')

    def getm_by_id(self, ids: list[str]) -> tuple[Recompensa]:
        return tuple(map(lambda id: next(Recompensa(**x) for x in self.rows if x['id'] == id), ids))


recompensas_csv = RecompensasCsv()
