from datetime import datetime
from contextlib import contextmanager

from game import Game
from world import Wall, Food
from direction import Direction


# this context manager is here otherwise we'd end up in an infinite loop importing game/context_managers
@contextmanager
def start_game(size):
    with open('games', 'a') as g_log:
        g_log.write(f"Game started at {datetime.now()}!\n")
        yield Game(size)
        g_log.write(f"Game ended at {datetime.now()}!\n")


# aa = Game(15)
with start_game(15) as game:
    game.add_cell(Wall(), 0, 4)
    game.add_cell(Wall(), 0, 8)
    game.add_cell(Wall(), 0, 12)
    game.add_cell(Wall(), 1, 12)
    game.add_cell(Food('Brocolli', 5), 3, 1)
    game.add_cell(Food('Mashed Potatoes', 5), 3, 2)
    game.add_cell(Food('MEAT', 5), 3, 3)
    game.add_cell(Food('garbage', 5), 3, 4)
    game.add_cell(Food('mcdonalds', 5), 3, 5)
    game.add_cell(Food('Taco Bell', 5), 3, 6)
    game.add_cell(Food('Wendys', 5), 3, 7)
    game.add_cell(Food('The Habit', 5), 3, 8)
    game.add_cell(Food('Five Guys', 5), 3, 9)
    game.add_cell(Food('burger king', 5), 3, 10)
    game.add_cell(Food('Doner', 5), 3, 11)
    game.add_cell(Food('Pizza', 5), 3, 12)
    game.add_cell(Food("Ben & Jerry's", 5), 3, 13)
    game.add_cell(Food('Sometthing', 5), 3, 14)
    # print(aa)
    game.move_python(Direction.UP)
    # print(aa)
    game.move_python(Direction.UP)
    game.move_python(Direction.LEFT)
    game.move_python(Direction.LEFT)
    #
    game.move_python(Direction.LEFT)
    game.move_python(Direction.LEFT)
    game.move_python(Direction.LEFT)
    game.move_python(Direction.UP)
    print(game)

    game.move_python(Direction.RIGHT)
    print(game)

    game.move_python(Direction.LEFT)
    game.move_python(Direction.LEFT)
    game.move_python(Direction.UP)
    print(game)

    # print(aa)
    # aa.move_python(UP)
    # print(aa)
    # print(aa)
    # aa.move_python(UP)
    # print(aa)
    # aa.move_python(DOWN)


