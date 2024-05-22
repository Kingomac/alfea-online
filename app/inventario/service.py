from app.usuarios.model import Usuario
from db import redis_db


def equipar_ataque(usuario: Usuario, ataque_id: str):
    n_equipados = redis_db.scard(f'ataques_equipados:{usuario.nombre}')
    if n_equipados >= 5:
        return {"error": "Ya tienes 5 ataques equipados"}
    redis_db.sadd(f'ataques_equipados:{usuario.nombre}', ataque_id)
    return {"todo": "ok"}


def desequipar_ataque(usuario: Usuario, ataque_id: str):
    redis_db.srem(f'ataques_equipados:{usuario.nombre}', ataque_id)
    return {"todo": "ok"}
