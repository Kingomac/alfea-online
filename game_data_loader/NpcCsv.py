from .BaseCsvFile import BaseCsvFile
from .model import Npc
from .AtaquesCsv import ataques_csv


class NpcCsv(BaseCsvFile):
    def __init__(self, file_path):
        super().__init__(file_path)

    def get_npc_by_id(self, npc_id: str):
        return next((npc for npc in self.rows if npc["id"] == npc_id), None)

    def getm_npc_by_id(self, npc_ids: list[str]):
        return list(filter(lambda x: True if x["id"] in npc_ids else False, self.rows))

    def npc_from_dict(self, npc_dict: dict):
        return Npc(npc_dict["id"], npc_dict["nombre"], int(npc_dict["vida_maxima"]), int(npc_dict["mana_maximo"]), int(npc_dict["poder_fisico"]), int(npc_dict["poder_magico"]), int(npc_dict["resistencia_fisica"]), int(npc_dict["resistencia_magica"]), int(npc_dict["velocidad"]), map(ataques_csv.get_by_id, npc_dict["ataques"].split(',')))


npc_csv = NpcCsv('game_data/combate/npc_stats.csv')
