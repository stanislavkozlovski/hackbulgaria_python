from week04.day_01.dungeon import Dungeon
from week04.day_01.entities import Hero, Enemy
from week04.day_01.spells import Spell
from week04.day_01.items import Weapon


class Fight():
    def __init__(self, hero: Hero, enemy: Enemy, initial_attack):
        print('A fight is started between our Hero {} and Enemy {}'.format(
            hero.name, enemy.name
        ))
        # hero attacks first by choice
        hero.initial_attack(enemy, initial_attack)

        while True:
            self.__enemy_turn(hero, enemy)

            # hero attack
            killing_blow = hero.attack(victim=enemy)

            if killing_blow:
                hero.leave_combat()
                break

    def __enemy_turn(self, hero: Hero, enemy: Enemy):
        # the enemy either moves to the hero or attacks him
        if enemy.x_coord != hero.x_coord and enemy.y_coord != hero.y_coord:
            # move enemy
            enemy.move_toward(hero)
        else:
            enemy.attack(victim=hero)


def sample_game_run():
    # TOOD: TESTS AND FURTHER REFINEMENT!
    h = Hero(name="Bron", title="Dragonslayer", health=100, mana=100, mana_regen_rate=2)
    w = Weapon(name="The Axe of Destiny", damage=20)
    h.equip(w)
    s = Spell(name="Fireball", damage=30, mana_cost=50, cast_range=2)
    h.learn(s)
    map = Dungeon("level1.txt", hero=h)
    map.spawn(h)
    map.print_map()
    map.move_hero("right")
    map.move_hero("down")
    map.print_map()
    map.hero_attack(by="spell")
    map.move_hero("down")
    map.move_hero("down")
    map.print_map()
    map.move_hero("right")
    map.move_hero("right")
    map.move_hero("down")
    map.print_map()
    map.move_hero("up")
    map.move_hero("right")
    map.move_hero("right")
    map.move_hero("right")
    map.print_map()
    map.hero_attack(by="spell")
    map.print_map()


def main():
    sample_game_run()


if __name__ == "__main__":
    main()