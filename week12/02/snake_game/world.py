from exceptions import ConstructionError
from settings import DIRECTION_VALUES


class Vector2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        self.x += other.x
        self.y += other.y

    def __sub__(self, other):
        self.x -= other.x
        self.y -= other.y

    def __neg__(self):
        return Vector2D(-self.x, -self.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def move(self, direction):
        """
        Move the Vector according to the direction given
        :param direction: An instance of either LEFT, RIGHT, UP or DOWN
        """
        for _dir, values in DIRECTION_VALUES.items():
            if isinstance(direction, _dir):
                self.x += values[0]
                self.y += values[1]
                return self.x, self.y


class WorldObject:
    """
    The most basic class for an object in the Snake world
    """
    pass


class BlackHole(WorldObject):
    def __str__(self):
        return '⛳'


class Wall(WorldObject):
    def __str__(self):
        return '■'


class Food(WorldObject):
    def __init__(self, name, energy: int):
        self.name = name
        self.energy = energy

    def __str__(self):
        return '🍌'


class Cell:
    def __init__(self,content: WorldObject=None):
        self.content: WorldObject = content

    def __str__(self):
        if self.content is None:
            return '□'

        return str(self.content)

    def __repr__(self):
        return f'Cell at {self.x}:{self.y}'

    def is_empty(self):
        return self.content is None

    def validate_content(self):
        if self.content is not None and not isinstance(self.content, WorldObject):
            raise ConstructionError(f'{self.content} is not a valid World Object!')