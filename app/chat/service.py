from app.chat.model import Mensaje
from db import redis_db
import json


def get_mensajes_from_keys(claves):
    mensajes = [Mensaje(timestamp=clave.decode().split(':')[-1], **json.loads(redis_db.get(clave.decode()))) for
                clave in claves]
    mensajes.sort(key=lambda x: x.timestamp)
    return mensajes


def get_mensajes_sala(sala):
    claves = redis_db.keys(f"chat:{sala}:*")
    return get_mensajes_from_keys(claves)


def get_lista_amigos(usuario: str):
    amigos = redis_db.lrange(f"amigos:{usuario}", 0, -1)
    return [amigo.decode() for amigo in amigos]
