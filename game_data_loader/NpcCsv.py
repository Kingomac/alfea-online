from .BaseCsvFile import BaseCsvFile

class NpcCsv(BaseCsvFile):
    def __init__(self, file_path):
        super().__init__(file_path)

    def get_npc_by_id(self, npc_id: str):
        return next((npc for npc in self.rows if npc["id"] == npc_id), None)

    def getm_npc_by_id(self, npc_ids: list[str]):
        return tuple(filter(lambda x: True if x["id"] in npc_ids else False, self.rows))
    
npc_csv = NpcCsv('game_data/combate/npc_stats.csv')