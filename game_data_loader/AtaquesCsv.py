from .BaseCsvFile import BaseCsvFile


class AtaquesCsv(BaseCsvFile):
    def __init__(self):
        super().__init__('game_data/combate/ataques.csv')

    def get_by_id(self, ataque_id):
        return next((ataque for ataque in self.rows if ataque['id'] == ataque_id), None)
