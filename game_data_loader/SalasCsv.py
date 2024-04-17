from .BaseCsvFile import BaseCsvFile


class SalasCsv(BaseCsvFile):
    def __init__(self):
        super().__init__('game_data/salas.csv')

    def get_sala(self, alias):
        return next((sala for sala in self.rows if sala['alias'] == alias), None)


salas_csv = SalasCsv()
