from .BaseCsvFile import BaseCsvFile


class RaidsCsv(BaseCsvFile):
    def __init__(self):
        super().__init__('game_data/combate/raids.csv')


raids_csv = RaidsCsv()
