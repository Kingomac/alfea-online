from .InCombatParticipant import InCombatParticipant
from .AtaqueTurno import AtaqueTurno
from uuid import uuid4
from db import redis_db
from redis.commands.json.path import Path
from game_data_loader import ataques_csv
import json


class InCombat:
    def __init__(self, id: str, heroes: list[InCombatParticipant], villanos: list[InCombatParticipant], ataquesTurno: list[AtaqueTurno]) -> None:
        self.id = id
        self.heroes: list[InCombatParticipant] = heroes
        self.villanos: list[InCombatParticipant] = villanos
        # id usuario -> id ataque
        self.ataquesTurno: list[AtaqueTurno] = ataquesTurno

    def get_participant_by_nombre(self, nombre: str):
        for x in self.heroes:
            if x.nombre == nombre:
                return x
        for x in self.villanos:
            if x.nombre == nombre:
                return x
        return None

    def save(self):
        redis_db.set(f"combate:{self.id}", json.dumps(self.__dict__()))
        return self.id

    def delete(self):
        redis_db.delete(f"combate:{self.id}")

    @staticmethod
    def tiene_acceso(usuario, id_combate):
        if redis_db.exists(f"combate:{id_combate}"):
            combate = InCombat.load(id_combate)
            return any(map(lambda x: x.nombre == usuario, combate.heroes + combate.villanos))
        return False

    @staticmethod
    def load(id: str):
        data = json.loads(redis_db.get(f"combate:{id}").decode())
        if data:
            return InCombat(data["id"],
                            [InCombatParticipant.from_combat(
                                x['nombre'], int(x['vida']), int(x['mana']), x['id_npc']) for x in data["heroes"]],
                            [InCombatParticipant.from_combat(
                                x['nombre'], int(x['vida']), int(x['mana']), x['id_npc']) for x in data["villanos"]],
                            [AtaqueTurno(**x) for x in data["ataquesTurno"]])
        return None

    @staticmethod
    def create(heroes: list[InCombatParticipant], villanos: list[InCombatParticipant]):
        return InCombat(str(uuid4()), heroes, villanos, {})

    def __dict__(self):
        return {
            "id": self.id,
            "heroes": [x.__dict__() for x in self.heroes],
            "villanos": [x.__dict__() for x in self.villanos],
            "ataquesTurno": [x.__dict__() for x in self.ataquesTurno]
        }
