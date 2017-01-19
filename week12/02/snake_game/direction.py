class DirectionBase:
    def can_switch_to(self, given_dir):
        return given_dir is not self.opposite_direction

    def __str__(self):
        return f'{self.__class__.__name__}'

    def __repr__(self):
        return self.__str__()


class DOWN(DirectionBase):
    """
    From DOWN you can switch to every direction except UP
    """

    def __init__(self, opposite_direction):
        self.opposite_direction = opposite_direction


class UP(DirectionBase):
    """
    From UP you can switch to every direction except DOWN
    """

    def __init__(self, opposite_direction):
        self.opposite_direction = opposite_direction


class RIGHT(DirectionBase):
    """
    From RIGHT you can switch to every direction except left
    """

    def __init__(self, opposite_direction):
        self.opposite_direction = opposite_direction


class LEFT(DirectionBase):
    """
    from LEFT you can switch to every direction except right
    """

    def __init__(self, opposite_direction):
        self.opposite_direction = opposite_direction


class Direction:
    LEFT = LEFT(RIGHT)
    RIGHT = RIGHT(LEFT)
    UP = UP(DOWN)
    DOWN = DOWN(UP)
