from .BaseCsvFile import BaseCsvFile


class SalasCsv(BaseCsvFile):
    def __init__(self):
        super().__init__('game_data/salas.csv')

    def get_by_alias(self, alias):
        return next((sala for sala in self.rows if sala['alias'] == alias), None)

    def get_by_id(self, sala_id):
        return next((sala for sala in self.rows if sala['id'] == sala_id), None)


salas_csv = SalasCsv()
