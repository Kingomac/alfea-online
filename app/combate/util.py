from game_data_loader.model import Recompensa
from game_data_loader import recompensas_csv
from db import redis_db


def dar_recompensa_aleatoria(usuario: str):
    recompensa = recompensas_csv.get_random()
    redis_db.lpush(f"recompensas:{usuario}", recompensa.id)
    return recompensa
