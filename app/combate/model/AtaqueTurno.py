class AtaqueTurno:
    def __init__(self, ataque, usuario, objetivo):
        self.ataque = ataque
        self.usuario = usuario
        self.objetivo = objetivo

    def __dict__(self):
        return {
            'ataque': self.ataque,
            'usuario': self.usuario,
            'objetivo': self.objetivo
        }
