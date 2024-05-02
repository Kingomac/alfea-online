from .InCombatParticipant import InCombatParticipant
from uuid import uuid4
from db import redis_db
from redis.commands.json.path import Path


class InCombat:
    def __init__(self, id: str, heroes: list[InCombatParticipant], villanos: list[InCombatParticipant], ataquesTurno: dict[str, int]) -> None:
        self.id = id
        self.heroes: list[InCombatParticipant] = heroes
        self.villanos: list[InCombatParticipant] = villanos
        # id usuario -> id ataque
        self.ataquesTurno: dict[str, str] = ataquesTurno

    def save(self):
        redis_db.json().set(f"combate:{self.id}", Path.root_path(), {
            "id": self.id,
            "heroes": [x.__dict__() for x in self.heroes],
            "villanos": [x.__dict__() for x in self.villanos],
            "ataquesTurno": self.ataquesTurno
        }, )
        return self.id

    @staticmethod
    def load(id: str):
        data = redis_db.json().get(f"combate:{id}")
        if data:
            return InCombat(data["id"], [InCombatParticipant(**x) for x in data["heroes"]] + [InCombatParticipant(**x) for x in data["villanos"]], data["ataquesTurno"])
        return None

    @staticmethod
    def create(heroes: list[InCombatParticipant], villanos: list[InCombatParticipant]):
        return InCombat(str(uuid4()), heroes, villanos, {})
