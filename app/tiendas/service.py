from app.usuarios.model import CombatStats, Usuario
from db import redis_db
from game_data_loader import ataques_csv, precios_ataques_csv


def mejorar_estadisticas(usuario: Usuario, nuevas_combat_stats: CombatStats):
    ATRIBS = ('vida_maxima', 'mana_maximo', 'poder_fisico',
              'poder_magico', 'resistencia_fisica', 'resistencia_magica', 'velocidad')
    actuales = usuario.get_combate_stats()
    actuales_total = sum([actuales.__dict__[x] for x in ATRIBS])
    nuevas_total = sum([nuevas_combat_stats.__dict__[x] for x in ATRIBS])
    if nuevas_total - actuales_total > usuario.experiencia:
        return {'error': f'Tienes {usuario.experiencia} e intentas gastar {nuevas_total - actuales_total}'}
    redis_db.hincrby(f'usuario:{usuario.nombre}',
                     'experiencia', -(nuevas_total - actuales_total))
    redis_db.hset(f'usuario:{usuario.nombre}',
                  'combate_stats_str', str(nuevas_combat_stats))
    return {'todo': 'ok'}


def get_ataques_con_precios():
    return [{'precio': precios_ataques_csv.get_by_id(x.id), 'ataque': x} for x in ataques_csv.get_all()]


def comprar_ataque(usuario: Usuario, ataque_id: str):
    print(f'Comprar ataque: {ataque_id}')
    precio = precios_ataques_csv.get_by_id(ataque_id)
    if precio == -1:
        return {'error': 'No existe ese ataque'}
    if usuario.monedas >= precio:
        redis_db.sadd(f'ataques:{usuario.nombre}', ataque_id)
        redis_db.hincrby(f'usuario:{usuario.nombre}', 'monedas', -precio)
        return {'monedas': usuario.monedas - precio}
    return {'error': 'No tienes suficiente dinero'}
