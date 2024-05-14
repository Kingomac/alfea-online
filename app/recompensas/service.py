from db import redis_db
from game_data_loader import recompensas_csv


def get_recompensas_usuario(usuario: str):
    return recompensas_csv.getm_by_id([x.decode() for x in redis_db.lrange(f"recompensas:{usuario}", 0, -1)])


def dar_recompensa(usuario: str):
    recompensas = recompensas_csv.getm_by_id(['1'])
    for recompensa in recompensas:
        redis_db.lpush(f"recompensas:{usuario}", recompensa.id)
    return recompensas
