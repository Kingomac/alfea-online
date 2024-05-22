from db import redis_db
from game_data_loader import ataques_csv


def get_ataques_usuario(nombre: str):
    return list(map(lambda x: ataques_csv.get_by_id(x.decode()), redis_db.smembers(f"ataques:{nombre}")))


def get_ids_ataques_usuario(nombre: str):
    return list(map(lambda x: x.decode(), redis_db.smembers(f"ataques:{nombre}")))


def get_ataques_equipados_usuario(nombre: str):
    return list(map(lambda x: ataques_csv.get_by_id(x.decode()), redis_db.smembers(f"ataques_equipados:{nombre}")))
