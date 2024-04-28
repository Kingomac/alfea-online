import flask_login
from flask_login import UserMixin
import werkzeug.security as ws
from db import redis_db
import json

from util import decode_hgetall


class Usuario(UserMixin):

    def __init__(self, nombre, password, nivel, experiencia, monedas, foto_perfil, titulo_nobiliario, matrimonio,
                 sala_actual, combate_stats_str: str):
        self.nombre: str = nombre
        self.password: str = password
        self.nivel: int = nivel
        self.experiencia: int = experiencia
        self.monedas: int = monedas
        self.foto_perfil: str = foto_perfil
        self.titulo_nobiliario: str = titulo_nobiliario
        self.matrimonio: str = matrimonio
        self.sala_actual: int = sala_actual
        self.combate_stats_str: str = combate_stats_str

    def check_password(self, password):
        return ws.check_password_hash(self.password, password)

    def get_id(self):
        return self.nombre

    @property
    def combate_stats(self):
        return CombateStats.from_str(self.combate_stats_str)

    @staticmethod
    def current():
        usr = flask_login.current_user
        if usr.is_anonymous:
            flask_login.logout_user()
            usr = None
        return usr

    @staticmethod
    def find_by_name(nombre):
        fetch = decode_hgetall(redis_db.hgetall(f"usuario:{nombre}"))
        if fetch is None:
            return None
        return Usuario(**fetch)
