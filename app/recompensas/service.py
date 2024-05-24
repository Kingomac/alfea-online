from db import redis_db
from game_data_loader import recompensas_csv


def get_recompensas_usuario(usuario: str):
    return recompensas_csv.getm_by_id([x.decode() for x in redis_db.lrange(f"recompensas:{usuario}", 0, -1)])


def reclamar_recompensas(usuario: str):
    recompensas = get_recompensas_usuario(usuario)
    total = {'experiencia': 0, 'monedas': 0}
    for rec in recompensas:
        redis_db.hincrby(f"usuario:{usuario}", "experiencia", rec.experiencia)
        redis_db.hincrby(f"usuario:{usuario}", "monedas", rec.monedas)
    redis_db.delete(f"recompensas:{usuario}")
    return total


def dar_recompensa(usuario: str):
    recompensas = recompensas_csv.getm_by_id(['1'])
    for recompensa in recompensas:
        redis_db.lpush(f"recompensas:{usuario}", recompensa.id)
    return recompensas
