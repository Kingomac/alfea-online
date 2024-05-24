import flask_login
from flask_login import UserMixin
import werkzeug.security as ws
from .CombatStats import CombatStats
from db import redis_db
import json
from db.util import decode_hgetall


class Usuario(UserMixin):

    def __init__(self, nombre: str, password, experiencia: int, monedas: int, sala_actual: str, combate_stats_str: str):
        self.nombre: str = nombre
        self.password: str = password
        self.experiencia: int = experiencia
        self.monedas: int = monedas
        self.sala_actual: int = sala_actual
        self.combate_stats_str: str = combate_stats_str

    def check_password(self, password):
        return ws.check_password_hash(self.password, password)

    def get_combate_stats(self):
        return CombatStats.from_str(self.combate_stats_str)
        # return CombatStats(*map(int, self.combate_stats_str.split(',')))

    @staticmethod
    def find_by_name(nombre):
        fetch = decode_hgetall(redis_db.hgetall(f"usuario:{nombre}"))
        if fetch is None:
            return None
        return Usuario(fetch['nombre'], fetch['password'], int(fetch['experiencia']),
                       int(fetch['monedas']
                           ), fetch['sala_actual'], fetch['combate_stats_str'])
