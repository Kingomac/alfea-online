import flask_login
from flask_login import UserMixin
import werkzeug.security as ws


class Usuario(UserMixin):
    def __init__(self, id, nombre, password, nivel, experiencia, monedas, foto_perfil, titulo_nobiliario, matrimonio,
                 inventario, transformaciones, hechizos, sala_actual):
        self.id = id
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
        ws.check_password_hash(self.password, password)

    @staticmethod
    def current():
        usr = flask_login.current_user
        if usr.is_anonymous:
            flask_login.logout_user()
            usr = None
        return usr
