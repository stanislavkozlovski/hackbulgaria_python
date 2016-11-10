# the class for our generic in-game Spell
class Spell():
    def __init__(self, name: str, damage: int, mana_cost: int, cast_range: int):
        self.name = name
        self.damage = damage
        self.mana_cost = mana_cost
        self.cast_range = cast_range