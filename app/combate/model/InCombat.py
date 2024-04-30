from .InCombatUser import InCombatUser
from uuid import uuid4
from db import redis_db
import json


class InCombat:
    def __init__(self, id: str, participantes: list[InCombatUser], ataquesTurno: dict[str, int]) -> None:
        self.id = id
        self.participantes: list[InCombatUser] = participantes
        self.ataquesTurno: dict[str, int] = ataquesTurno  # ids de los ataques

    def save(self):
        redis_db.json().set(f"combate:{self.id}", json.dumps(self))
        return self.id

    @staticmethod
    def load(id: str):
        return json.loads(redis_db.json().get(f"combate:{id}"))

    @staticmethod
    def new(participantes: list[InCombatUser]):
        return InCombat(str(uuid4()), participantes, {})
