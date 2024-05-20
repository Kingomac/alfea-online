from app.usuarios.model import Usuario
from db import redis_db
from game_data_loader import salas_csv


def desplazar_usuario(usuario: Usuario, id_sala_destino: str) -> None:
    sala_actual = salas_csv.get_by_id(usuario.sala_actual)
    sala_destino = salas_csv.get_by_id(id_sala_destino)
    if sala_actual['grupo'] != sala_destino['grupo']:
        if usuario.monedas < 3:  # Si no puede pagar se queda en la sala que está
            return sala_actual
        redis_db.hincrby(f"usuario:{usuario.nombre}",
                         "monedas", -3)
    redis_db.hset(f"usuario:{usuario.nombre}", "sala_actual", id_sala_destino)
    return sala_destino
