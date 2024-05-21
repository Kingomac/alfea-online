from app.usuarios.model import CombatStats, Usuario
from db import redis_db


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
