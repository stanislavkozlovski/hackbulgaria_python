class Error(Exception):
    pass


class ConstructionError(Error):
    pass


class InvalidGameSizeError(Error):
    pass


class DirectionError(Error):
    pass


class InvalidWorldError(Error):
    pass


class CollisionError(Error):
    pass


class OutOfWorldError(Error):
    pass
