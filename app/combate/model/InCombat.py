from .InCombatUser import InCombatParticipant
from uuid import uuid4
from db import redis_db
from redis.commands.json.path import Path


class InCombat:
    def __init__(self, id: str, participantes: list[InCombatParticipant], ataquesTurno: dict[str, int]) -> None:
        self.id = id
        self.participantes: list[InCombatParticipant] = participantes
        # id usuario -> id ataque
        self.ataquesTurno: dict[str, str] = ataquesTurno

    def save(self):
        redis_db.json().set(f"combate:{self.id}", Path.root_path(), {
            "id": self.id,
            "participantes_usuarios": [x.nombre for x in self.participantes if not x.is_npc],
            "participantes_npcs": [x.id_npc for x in self.participantes if x.is_npc],
            "ataquesTurno": self.ataquesTurno
        }, )
        return self.id

    @staticmethod
    def load(id: str):
        data = redis_db.json().get(f"combate:{id}")
        if data:
            return InCombat(data["id"], [InCombatParticipant.load_usuario(x) for x in data["participantes_usuarios"]] + [InCombatParticipant.load_npc(x) for x in data["participantes_npcs"]], data["ataquesTurno"])
        return None

    @staticmethod
    def create(participantes: list[InCombatParticipant]):
        return InCombat(str(uuid4()), participantes, {})
