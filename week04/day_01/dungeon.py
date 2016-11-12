import random
from operator import add

from .spells import Spell
from .entities import Hero, Enemy
from .items import Weapon


# our Dungeon class that holds the map of the dungeon
class Dungeon:
    # the values you need to add to your x,y coordinates when you want to move in a certain direction
    DIRECTION_VALUES = {'up': (-1, 0),
                      'down': (1, 0),
                      'left': (0, -1),
                      'right': (0, 1)}

    def __init__(self, path_to_level: str, hero: Hero):
        self.path_to_level = path_to_level
        self._map = self.load_map()
        self._treasures = self.load_treasures()
        self.hero = hero  # type:Hero

    def spawn(self, hero):
        for row_idx, row in enumerate(self._map):
            for col_idx, col in enumerate(row):
                if col == 'S':
                    # spawn the hero
                    self._map[row_idx][col_idx] = 'H'
                    self.hero.set_coordinates(row_idx, col_idx)
                    return True

        return False

    def hero_attack(self, by: str):
        initial_attack = None
        # check for meele range
        enemy_coords = self.enemy_in_range(range_=1)

        if by == 'spell':
            spell = self.hero.get_attack_damage(by='spell')
            if spell:
                # check for longer range for an enemy
                enemy_coords = self.enemy_in_range(spell.cast_range)
                if enemy_coords:
                    initial_attack = spell
                else:
                    print('Nothing in casting range {}'.format(spell.cast_range))
        elif enemy_coords:
            initial_attack = self.hero.get_attack_damage(by='weapon')

        if initial_attack is not None:
            from .dungeons_and_pythons import Fight
            enemy = Enemy("Badguy", "Mcgee", 100, 100, 20, x_coord=enemy_coords[0], y_coord=enemy_coords[1])
            enemy.learn(Spell('Frostbolt', damage=25, mana_cost=90, cast_range=3))
            w = Weapon(name="The Axe of Destiny", damage=20)
            enemy.equip(w)
            Fight(hero=self.hero, enemy=enemy, initial_attack=initial_attack)
            # if we get to this line, it means that the Hero has won the fight and
            # that the enemy is dead, therefore we should remove it from the map
            self.__remove_enemy(enemy)

    def move_hero(self, direction: str):
        # add the current coords to the values of the direction to get the new coordinates
        new_x_coord, new_y_coord = map(add, (self.hero.x_coord, self.hero.y_coord), self.DIRECTION_VALUES[direction])
        # check if out of bounds
        if (new_x_coord < 0 or new_x_coord >= len(self._map)
            or new_y_coord < 0 or new_y_coord >= len(self._map[new_x_coord])
            or self._map[new_x_coord][new_y_coord] == '#'):  # if an obstacle is in the way
            return False

        if self._map[new_x_coord][new_y_coord] == 'E':
            self.hero_attack(by='spell')
        elif self._map[new_x_coord][new_y_coord] == 'T':
            treasure = self.__get_treasure()
            print('Found treasure - {}!'.format(treasure))

        self.update_map(new_x_coord, new_y_coord)

        return True

    def __remove_enemy(self, enemy: Enemy):
        self._map[enemy.orig_x_coord][enemy.orig_y_coord] = '.'

    def __get_treasure(self):
        """ This function gets a random treasure from the loaded treasures for the specific map"""
        # roll dice and get treasure
        treasure_idx = random.randint(0, len(self._treasures) - 1)
        treasure = self._treasures[treasure_idx]
        self._treasures.remove(treasure)

        return treasure

    def update_map(self, x, y):
        """ This function updates the map whenever the character moves from one position to another"""
        self._map[self.hero.x_coord][self.hero.y_coord] = '.'
        self._map[x][y] = 'H'
        self.hero.set_coordinates(x, y)

    def enemy_in_range(self, range_: int):
        # check all the ways to find an enemy in the range given
        start_y_position = self.hero.y_coord - range_ if self.hero.y_coord - range_ >= 0 else 0
        end_y_position = self.hero.y_coord + range_ if len(self._map[self.hero.x_coord]) > self.hero.y_coord + range_  \
                                                    else len(self._map[self.hero.x_coord]) - 1

        start_x_position = self.hero.x_coord - range_ if self.hero.x_coord - range_ >= 0 else 0
        end_x_position = self.hero.x_coord + range_ if len(self._map) > self.hero.x_coord + range_ \
                                                    else len(self._map) - 1
        # range_ left from hero's Y position
        for new_y in range(start_y_position, self.hero.y_coord):
            if self._map[self.hero.x_coord][new_y] == 'E':
                return self.hero.x_coord, new_y
        # range_ right from hero's Y position
        for new_y in range(self.hero.y_coord, end_y_position+1):
            if self._map[self.hero.x_coord][new_y] == 'E':
                return self.hero.x_coord, new_y
        # range_ down from hero's X position
        for new_x in range(self.hero.x_coord, end_x_position+1):
            if self._map[new_x][self.hero.y_coord] == 'E':
                return new_x, self.hero.y_coord
        # range_ up from hero's X position
        for new_x in range(start_x_position, self.hero.x_coord):
            if self._map[new_x][self.hero.y_coord] == 'E':
                return new_x, self.hero.y_coord

        return False

    def load_map(self):
        with open(self.path_to_level, 'r', encoding='utf-8') as level_map:
            return list(map(lambda row: list(filter(lambda char: char != '\n', row)), level_map.readlines()))

    def load_treasures(self):
        with open(self.path_to_level[:self.path_to_level.index('.txt')] + '_treasures.txt', 'r', encoding='utf-8') as treasures:
            # return a list of all the treasures, removing the \n symbols
            return list(map(lambda treasure: ''.join(list(filter(lambda char: char != '\n', treasure))), treasures.readlines()))

    def print_map(self):
        print('\n'.join([''.join(row) for row in self._map]))