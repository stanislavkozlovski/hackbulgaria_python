import random

from player import Python, PythonPart
from exceptions import ConstructionError, InvalidGameSizeError, InvalidWorldError, OutOfWorldError, CollisionError, DirectionError
from direction import Direction
from world import BlackHole, Wall, Food, Cell, WorldObject
from context_managers import error_logger, step_logger, food_logger


class Game:
    COLLISION_CELL_TYPES = [BlackHole, Wall, PythonPart]

    def __init__(self, size):
        if not isinstance(size, int) or size < 6:
            raise InvalidGameSizeError('Game size must be an integer that is bigger than 6!')
        self.size = size
        self.world = self.build_world()
        self.python: Python = None
        self.spawn_python()
        self.food_count = 0

    def __str__(self):
        rows = []
        for row in self.world:
            rows.append(' '.join(str(p) for p in row))
        return '\n'.join(rows)

    def build_world(self) -> list:
        world: [[Cell]] = []

        for row in range(self.size):
            new_row: [Cell] = []

            for col in range(self.size):
                new_row.append(Cell())

            world.append(new_row)

        return world

    def spawn_python(self):
        """
        Spawn a Python in the game world
        """
        # free_spots = self._find_free_spot()
        # if len(free_spots) == 0:
        #     raise InvalidWorldError('There is no room to spawn a snake!')
        #
        # x, y = random.choice(free_spots)
        x, y = 5, 5
        self.python = Python(x, y)
        print(f'Python spawned at {x}:{y}!')
        # update the game world
        self.update_world()

    def move_python(self, direction=None):
        try:
            head_x, head_y, old_tail_x, old_tail_y = self.python.move(direction)
            with step_logger() as step_loggr:
                step_loggr.write(f'The Python moved {self.python.direction}')
            try:
                if head_x >= self.size or head_x < 0 or head_y < 0 or head_y >= self.size:
                    raise OutOfWorldError('Your Python has left the bounds of the world!')

                python_head: Cell = self.world[head_x][head_y]  # the cell the python moved to

                if any(isinstance(python_head.content, collision_cell) for collision_cell in self.COLLISION_CELL_TYPES):
                    raise CollisionError('The Python has hit something and is now dead! :(')

                if isinstance(python_head.content, Food):
                    meal: Food = python_head.content
                    with food_logger() as food_loggr:
                        food_loggr.write(f'The Python ate {meal.name}')
                    self.food_count -= 1

                    if self.food_count == 0:
                        print("!!! CONGRATULATIONS, YOU WIN !!!")
                        exit()
                    # eat the food, increase energy and spawn a new part where his old tail was (essentially growing)
                    self.python.eat_food(meal.energy, old_tail_x, old_tail_y)
                # the python has moved successfully!
                self.update_world((old_tail_x, old_tail_y))
            except (OutOfWorldError, CollisionError) as e:
                # The Python has died
                with error_logger() as el:
                    el.write(str(e))
                print(e)
                self.clean_up_dead_python(old_tail_x, old_tail_y)
                # spawn a new one
                self.spawn_python()
        except DirectionError as e:
            with error_logger() as el:
                el.write(str(e))
            print(e)

    def update_world(self, old_tail_coords: tuple = None):
        """
        After the Python's movement, update the cells in the world
        :param old_tail_coords: The coordinates of the python's tail before he moved, which should now be freed
        """
        if old_tail_coords is not None:
            tail_x, tail_y = old_tail_coords
            self.world[tail_x][tail_y] = Cell()

        for part in self.python.body:
            self.world[part.x][part.y] = Cell(part)

    def clean_up_dead_python(self, old_tail_x, old_tail_y):
        """
        The Python has dead and we have to clean up his body.
        We ignore the head because it has hit something or gone out of bounds
        """
        for part in self.python.body[1:]:
            self.world[part.x][part.y] = Cell()
        self.world[old_tail_x][old_tail_y] = Cell()

    def add_cell(self, cell_type: WorldObject, x, y):
        try:
            if not self.world[x][y].is_empty():
                raise ConstructionError('You cannot overwrite a cell that is not empty!')

            if isinstance(cell_type, Food):
                self.food_count += 1

            cell = Cell(cell_type)
            self.world[x][y] = cell
        except (ConstructionError, IndexError) as e:
            print(e.message)

    def _find_free_spot(self):
        """
        Traverse the world and return coordinates with valid spawns for the python
        Valid coordinates are 5 consecutive empty cells, since we spawn the head of the python and it's body
        to the left
        """
        free_spots: [(int, int)] = []
        for row_dx in range(self.size):
            idx = 0
            max_idx = len(self.world[row_dx]) - 5
            while idx < max_idx:
                cell: Cell = self.world[row_dx][idx]
                if cell.is_empty():
                    # Possible space for the head, look for the next 4 spaces
                    has_space = True

                    for i in range(idx + 1, idx + 5):
                        possible_cell = self.world[row_dx][i]
                        if not possible_cell.is_empty():
                            has_space = False
                            # We know there is no way to create a snake up to i, so update the index
                            idx = i + 1
                            break

                    if not has_space:
                        continue

                    # We have a place for the snake, so add it to the free_spots
                    free_spots.append((row_dx, idx))

                    # now continue searching
                    # knowing we need one more free cell to have idx+1 be a valid spot for the head
                    for i in range(idx + 5, max_idx):
                        cell: Cell = self.world[row_dx][i]
                        if not cell.is_empty():
                            idx = i  # next iteration will increment this and we will continue searching
                            break
                        idx += 1
                        free_spots.append((row_dx, idx))

                idx += 1

        return free_spots
