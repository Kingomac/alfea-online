from .InCombatUser import InCombatUser


class InCombat:
    def __init__(self) -> None:
        self.id = ""
        self.participantes: list[InCombatUser] = []
        self.ataquesTurno: dict[str, int] = {}  # ids de los ataques
