from .BaseCsvFile import BaseCsvFile


class RaidsCsv(BaseCsvFile):
    def __init__(self):
        super().__init__('game_data/combate/raids.csv')
        
    def get_by_id(self, raid_id: str):
        return next((raid for raid in self.rows if raid["id"] == raid_id), None)


raids_csv = RaidsCsv()
