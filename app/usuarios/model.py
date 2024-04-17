import flask_login
from flask_login import UserMixin
import werkzeug.security as ws
from db import redis_db
import json


class Usuario(UserMixin):
    def __init__(self, nombre, password, nivel, experiencia, monedas, foto_perfil, titulo_nobiliario, matrimonio,
                 inventario, transformaciones, hechizos, sala_actual):
        self.nombre = nombre
        self.password = password
        self.nivel = nivel
        self.experiencia = experiencia
        self.monedas = monedas
        self.foto_perfil = foto_perfil
        self.titulo_nobiliario = titulo_nobiliario
        self.matrimonio = matrimonio
        self.inventario = inventario
        self.transformaciones = transformaciones
        self.hechizos = hechizos
        self.sala_actual = sala_actual

    def check_password(self, password):
        return ws.check_password_hash(self.password, password)

    def get_id(self):
        return self.nombre

    @staticmethod
    def current():
        usr = flask_login.current_user
        if usr.is_anonymous:
            flask_login.logout_user()
            usr = None
        return usr

    @staticmethod
    def find_by_name(nombre):
        fetch = redis_db.get(f"usuario:{nombre}")
        if fetch is None:
            return None
        return Usuario(nombre, **json.loads(fetch))

    def __dict__(self):
        return {
            'password': self.password,
            'nivel': self.nivel,
            'experiencia': self.experiencia,
            'monedas': self.monedas,
            'foto_perfil': self.foto_perfil,
            'titulo_nobiliario': self.titulo_nobiliario,
            'matrimonio': self.matrimonio,
            'inventario': self.inventario,
            'transformaciones': self.transformaciones,
            'hechizos': self.hechizos,
            'sala_actual': self.sala_actual
        }
