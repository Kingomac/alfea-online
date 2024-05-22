from .BaseCsvFile import BaseCsvFile


class PreciosAtaquesCsv(BaseCsvFile):
    def __init__(self):
        super().__init__('game_data/precios_ataques.csv')

    def get_by_id(self, ataque_id):
        return int(next(
            (ataque['precio'] for ataque in self.rows if ataque['id'] == ataque_id), '-1'))
        # id;precio


precios_ataques_csv = PreciosAtaquesCsv()
