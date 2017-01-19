from settings import PYTHON_BODY_SIZE
from exceptions import DirectionError
from direction import Direction
from world import Vector2D

class PythonPart(Vector2D):
    def move_to(self, position: Vector2D):
        self.x = position.x
        self.y = position.y

    def __str__(self):
        return '●'


class PythonHead(PythonPart):
    def __str__(self):
        return '🐍'


class Python:
    def __init__(self, x: int, y: int):
        # build python
        self.head = PythonHead(x, y)
        self.body = [self.head]
        self.size = PYTHON_BODY_SIZE
        self.direction = Direction.LEFT
        self.energy = 0
        self.build_body_from_head()

    def eat_food(self, energy: int, x, y):
        self.energy += energy
        self.body.append(PythonPart(x, y))

    def build_body_from_head(self):
        """
        Builds the snake body SIZE blocks from the head on the same row
        """
        size = self.size
        x, y = self.head.x, self.head.y
        while size > 0:
            y += 1
            size -= 1
            self.body.append(PythonPart(x, y))

    def move(self, direction=None) -> (int, int):
        """
        Move the snake in the given direction, starting from the tail and ending with the final movement of the head
        Afterwards, send the coordinates of the head back, so that the game world can watch for collisions
        """
        if direction is None:
            direction = self.direction
        if not self.direction.can_switch_to(direction):
            raise DirectionError(f'You cannot move from {self.direction} to {direction}!')
        tail = self.body[-1]
        tail_x, tail_y = tail.x, tail.y

        # Move the snake starting from the back
        for idx in reversed(range(1, len(self.body))):
            self.body[idx].move_to(self.body[idx-1])
        # Move the head and return the coordinates for the game world to watch for collisions
        head_x, head_y = self.head.move(direction)
        self.direction = direction
        return head_x, head_y, tail_x, tail_y
