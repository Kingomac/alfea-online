from datetime import datetime
from flask_login import current_user


class Mensaje:
    def __init__(self, mensaje, usuario=None, timestamp=str(datetime.now().timestamp())):
        self.mensaje = mensaje
        if usuario is None and current_user.is_authenticated:
            usuario = current_user.nombre
        self.usuario = usuario
        self.timestamp = timestamp

    def get_fecha_bonita(self):
        return datetime.fromtimestamp(float(self.timestamp)).strftime('%H:%M:%S')

    def __dict__(self):
        return {
            'mensaje': self.mensaje,
            'usuario': self.usuario
        }

    def __str__(self):
        return f'{self.usuario}: {self.mensaje}'
