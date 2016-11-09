"""
Dungeons and Pythons

We are going to make a simple, 2D turn-based console game filled with dungeons and pythons!

We are going to have hero, enemies, weapons, treasures and magic!

So lets start with the basic stuff:

Our Hero

Make a Hero class which can be initialized by that (all constructor arguments are shown in the example):

h = Hero(name="Bron", title="Dragonslayer", health=100, mana=100, mana_regeneration_rate=2)
Our hero should have the following methods:

known_as() method

Add a known_as() method to our Hero, which returns a string, formatted in the following way: "{hero_name} the {hero_title}"

For example:

# >>> h.known_as()
Bron the DragonSlayer
get_health() and get_mana() and is_alive() and can_cast()

Every hero starts with the given health and mana points.

Those health and mana points are the maximum health and mana for the hero!

When a hero reaches 0 health he is considered death.
When a hero reaches 0 mana, he cannot cast any spells
Implement the following methods:

is_alive() which returns True, if our hero is still alive. Otherwise - False.
get_health() which returns the current health
get_mana() which returns the current mana
can_cast() which returns True, if our hero can cast the magic he has been given. Otherwise - False
take_damage(damage_points)

So, our hero can take damage which reduces his health.

Implement a method, called take_damage(damage_points) where damage can be either integer or floating point value.

This method should reduce the hero's health by damage

If we inflict more damage than we have health, health will always be equal to zero and we cannot get below that!

take_healing(healing_points)

Our hero can also be healed!

Implement a method, called take_healing(healing_points) which heals our hero.

Here are the requirements:

If our hero is dead, the method should return False. It's too late to heal our hero
We cannot heal our hero above the maximum health, which is given by health
If healing is successful (Our hero is not dead), the method should return True
take_mana(mana_points)

Our hero can also increase his mana in two ways:

Each time he makes a move, his mana is increased by mana_regeneration_rate amount.
He can drink a mana potion, which will increse his mana by the amount of mana points the potion have.
Hero's mana cannot go above the start mana given to him, neither he can go down below 0 mana.

equip(weapon) method

Our hero can equip one weapon and one spell in order to have damage.

Check the weapon example for more information.

learn(spell) method

The same as equip, but takes a Spell class.

Our hero can learn only 1 spell at a time.

If you learn a given spell, and after this learn another one, the hero can use only the latest.

attack() method

The method should return the demage done either from the weapon or from the spell (more on that, later)

If the hero has not been equiped with weapon or he has no spells, his attack points are 0.

The method can be called in two ways:

attack(by="weapon") - returns the damage of the weapon if equiped or 0 otherwise
attack(by="magic") - returns the damage of the spell, if quiped or 0 otherwise
The Enemies

Implement a class Enemy which is initialized like that:

enemy = Enemy(health=100, mana=100, damage=20)
The Enemy should have the following methods, just like our hero:

is_alive()
can_cast()
get_health()
get_mana()
take_healing()
take_mana()
attack()
take_damage(damage)

Enemies cannot regenerate mana!

Enemies have starting damage, which is different from a weapon or a spell. They can equip weapons or learn spells but it is not required for them to have any damage, as it is for our hero.
The weapons and spells

In order for our hero to have proper damage, he must be equiped with either a weapon or a spell.

One hero can carry at max 1 weapon and 1 spell.

Weapon class

Implement a simple class Weapon which behave like that:

h = Hero(name="Bron", title="Dragonslayer", health=100, mana=100, mana_regeneration_rate=2)
w = Weapon(name="The Axe of Destiny", damage=20)

h.equip(w)

h.attack(by="weapon") == 20
Spell class

This should be more complex. Implement a spell class, which behaves like that:

s = Spell(name="Fireball", damage=30, mana_cost=50, cast_range=2)
name and damage are self explanatory.

mana_cost means that the spell needs at least that much amount of mana in order to be casted. Raise an error if you cannot cast that spell.
cast_range is a bit more special and related to the Dungeon. You can cast that spell on an enemy, which is within the cast_range. If cast_range is 1, you can attack enemies, that are next to you. If cast range is greater than 1, you can attack enemies from distance, that is cast_range squares away. Casting range is only calculated in a straight line. You cannot curve spells
The Dungeons and treasures

We are going to need a dungeon, where our hero can fight his enemies and find powerful weapons and spells!

Our dungeon is going to be a 2D map that looks like that:

S.##.....T
#T##..###.
#.###E###E
#.E...###.
###T#####G
Where:

S means a starting point for our hero.
G means gateway - the end of the dungeon (and most propably the enter to another)
# is an obstacle
. is a walkable path.
T is a treasure that can be either mana, health, weapon or spell
E is an enemy that our hero can fight
We are going to load the layout of our map from a file. For example, the map above can be located in a filed called level1.txt

We create new dungeon like this:

# >>> from dungeon import Dungeon
# >>> map = Dungeon("level1.txt")
# >>> map.print_map()

S.##.....T
#T##..###.
#.###E###E
#.E...###.
###T#####G
Our Dungeon should have the following methods:

print_map()

This should print the map to the console. Check the example above.

spawn

We want to spawn our hero in the S location of the map.

Implement a method, called spawn(hero) where:

hero is a Hero instance
This one takes the first free spawning point in the map and populates it with H.

The first free spawning point is the one, that we get if we start from top-left and walk right.

If the spawning is successful - return True. Otherwise (If there are no more spawning points, return False)

If our hero dies, he can respawn at the next spawning point. If there are no free spawning points, game is over

So, if we have the map above, let's take the following example:

# >>> map.spawn(some_hero_instance)
# >>> map.print_map()
H.##.....T
#T##..###.
#.###E###E
#.E...###.
###T#####G
move_hero()

Now, implemented a method move_hero(direction) where:

direction is either "up", "down", "left" and "right"
This should move our hero in the desired direction.

Return True if he can move into that direction or Fasle otherwise.

For example:

# >>> map.move_hero("right")
True
# >>> map.print_map()
.H##.....T
#T##..###.
#.###E###E
#.E...###.
###T#####G
# >>> map.move_hero("up")
False
# >>> map.move_hero("down")
Found treasure!
# >>> map.print_map()
..##.....T
#H##..###.
#.###E###E
#.E...###.
###T#####G
Here are the cases:

If you move into an obstacle, return False and don't make the move.
If you move outside the map - return False and don't make the move.
If you move into an enemy, a Fight is automatically started. Otherwise, you have options, which we will describe in the Fight class
If you move into Treasure, roll a dice to decide what it can be - a mana or health potion, a weapon or a spell
Treasures

It is a good idea to have a finite list of treasures that can be found in a given dungeon.

One idea is to keep a list of treasure in the txt file, where the map is. Other idea is to have a separate file that keeps the loot for each map.

Our suggestion for you is to keep a track of all treasures in the Dungeon class and have a method pick_treasure() that returns an instance of randomly picked treasure.

Fights

The interesting part is here.

Our hero must fight his enemies in order to reach the exit of the dungeon.

Our Dungeon should have a hero_attack(by) method, which checks if our hero can attack either by weapon or by spell, again having a by keyword-argument, like the Weapon

A fight happens when:

Our hero walks into the same position as the enemy - then the fights start automatically
Our hero is within some range of the enemy and triggers hero_attack method call. Then we can attack our enemy, but our enemy must walk to our place in order to start attacking us. This is really helpful with spells!
Implement a Fight class that takes a hero and an emeny and simulates a fight between them.

The Fight is over when either our hero or the enemy is dead.

Here is a full example:

# >>> h = Hero(name="Bron", title="Dragonslayer", health=100, mana=100, mana_regeneration_rate=2)
# >>> w = Weapon(name="The Axe of Destiny", damage=20)
# >>> h.equip(w)
# >>> s = Spell(name="Fireball", damage=30, mana_cost=50, cast_range=2)
# >>> h.learn(s)
# >>> map = Dungeon("level1.txt")
# >>> map.spawn(h)
# >>> map.print_map()
H.##.....T
#T##..###.
#.###E###E
#.E...###.
###T#####G
# >>> map.move_hero("right")
True
# >>> map.move_hero("down")
Found health potion. Hero health is max.
# >>> map.print_map()
..##.....T
#H##..###.
#.###E###E
#.E...###.
###T#####G
# >>> map.hero_attack(by="spell")
Nothing in casting range 2
# >>> map.move_hero("down")
# >>> map.move_hero("down")
# >>> map.print_map()
..##.....T
#.##..###.
#.###E###E
#HE...###.
###T#####G
# >>> map.hero_attack(by="spell")
A fight is started between our Hero(health=100, mana=100) and Enemey(health=100, mana=100, damage=20)
Hero casts a Fireball, hits enemy for 20 dmg. Enemy health is 80
Enemy moves one square to the left in order to get to the hero. This is his move.
Hero casts a Fireball, hits enemy for 20 dmg. Enemy health is 60
Enemy hits hero for 20 dmg. Hero health is 80
Hero does not have mana for another Fireball.
Hero hits with Axe for 20 dmg. Enemy health is 40
Enemy hits hero for 20 dmg. Hero health is 60.
Hero hits with Axe for 20 dmg. Enemy health is 20
Enemy hits hero for 20 dmg. Hero health is 40.
Hero hits with Axe for 20 dmg. Emely health is 0
Enemy is dead!
Fight steps

The fight follows this algorithm:

Our hero always attacks first
We always use the attack that deals more damage
If our weapon and our spell deals the same amount of damage, use the spell first.
When you run out of mana, use the weapon (if any)
Think of how you can make the enemies cast spells?
Creativity and Improvisation

As you can see, this is a big and a fat problem. There are things that are not well defined.

This is up to you. Make an interesting game!
"""


class Weapon():
    def __init__(self, name: str, damage: int):
        self.name = name
        self.damage = damage

class Spell():
    def __init__(self, name: str, damage: int, mana_cost: int, cast_range: int):
        self.name = name
        self.damage = damage
        self.mana_cost = mana_cost
        self.cast_range = cast_range


class Entity:
    def __init__(self, name: str, title: str, health: int, mana: int):
        self.name = name
        self. title = title
        self.max_health = health
        self.max_mana = mana
        self._health = health
        self._mana = mana
        self.spells = []  # type: [Spell]
        self.x_coord = 0
        self.y_coord = 0

    def set_coordinates(self, x, y):
        self.x_coord = x
        self.y_coord = y

    def equip(self, weapon):
       self.weapon = weapon  # type:

    def learn(self, spell: Spell):
        self.spells.append(spell)

    def attack(self, by: str):
        if by == 'spell':
            if self.spells:
                # get the spell with the maximum damage that we have enough mana for
                available_spells = [spell for spell in self.spells if self._mana >= spell.mana_cost]
                if not available_spells:
                    return Spell(name='Empty spell', damage=-1, mana_cost=-1, cast_range=0)
                spell = max(available_spells, key= lambda spell: spell.damage) # type: Spell
                if spell:
                    self.cast_spell(spell)
                    return spell
                else:
                    return Spell(name='Empty spell', damage=-1, mana_cost=-1, cast_range=0)
            else:
                print('{} does not know any spells.'.format(self.name))
                return Spell(name='Empty spell', damage=-1, mana_cost=-1, cast_range=0)
        else:
            return self.weapon.damage

    def cast_spell(self, spell: Spell):
        self._mana -= spell.mana_cost
        return spell.damage

    def take_damage(self, damage_points: int):
        # If we inflict more damage than we have health, health will always be equal to zero and we cannot get below that!
        self._health = self._health - damage_points if (self._health - damage_points) > 0 else 0

    def take_healing(self, healing_points: int):
        if self._health == 0:
            return False # our hero is dead, it's too late :(

        self._health += healing_points
        if self._health > self.max_health:
            self._health = self.max_health

        return True

    def take_mana(self, mana_points: int):
        self._mana += mana_points
        if self._mana > self.max_mana:
            self._mana = self.max_mana

    def known_as(self) -> str:
        return "{hero_name} the {hero_title}".format(
            hero_name=self.name,
            hero_title=self.title
        )

    def get_health(self) -> int:
        return self._health

    def get_mana(self) -> int:
        return self._mana

    def is_alive(self) -> bool:
        return self._health > 0

    def can_cast(self, spell: Spell) -> bool:
        return self._mana >= spell.mana_cost


class Hero(Entity):
    def __init__(self, name: str, title: str, health: int, mana: int, mana_regen_rate: int):
        super().__init__(name, title, health, mana)
        self.mana_renegeration_rate = mana_regen_rate


class Enemy(Entity):
    def __init__(self, name: str, title: str, health: int, mana: int, damage: int):
        super().__init__(name, title, health, mana)
        self.damage = damage

    def attack(self, by: str):
        return self.damage


class Fight():
    def __init__(self, hero: Hero, enemy: Enemy, initial_attack):
        print('A fight is started between our Hero {} and Enemy {}'.format(
            hero.name, enemy.name
        ))
        # hero attacks first
        print(type(initial_attack))
        print(type(Spell('d', 2, 2, 2)))
        self.initial_attack = initial_attack
        print(isinstance(self.initial_attack, Spell))
        print(isinstance(initial_attack, Spell))
        if isinstance(initial_attack, Spell):
            enemy.take_damage(initial_attack.damage)
            enemy_health = enemy.get_health()
            if enemy_health > 0:
                print('Hero casts a {spell_name}, hits enemy for {dmg} dmg. Enemy health is {enemy_health}'.format(
                    spell_name=initial_attack.name, dmg=initial_attack.damage, enemy_health=enemy_health
                ))
            else:
                print('Enemy is dead!')
                exit()
        else:
            enemy.take_damage(initial_attack)
            enemy_health = enemy.get_health()
            if enemy_health > 0:
                print('Hero hits with {wep_name} for {dmg} dmg. Enemy health is {enemy_health}'.format(
                    wep_name=hero.weapon.name, dmg=initial_attack, enemy_health=enemy_health
                ))
            else:
                print('Enemy is dead!')
                exit()

        while True:
            if enemy.x_coord != hero.x_coord and enemy.y_coord != hero.y_coord:
                # move enemy
                self.move_enemy(hero, enemy)
            else:
                hero.take_damage(damage_points=enemy.attack(by='weapon'))
                hero_health = hero.get_health()
                if hero_health > 0:
                    print('Enemy hits hero for {dmg} dmg. Hero health is {hero_health}'.format(
                        dmg=enemy.attack(by='weapon'),
                        hero_health=hero_health
                    ))
                else:
                    print('Hero is dead!')
                    exit()

            # hero attack
            spell = hero.attack(by='spell')
            if spell.damage >= hero.attack(by='weapon'):
                enemy.take_damage(spell.damage)
                enemy_health = enemy.get_health()
                if enemy_health > 0:
                    print('Hero casts a {spell_name}, hits enemy for {dmg} dmg. Enemy health is {enemy_health}'.format(
                        spell_name=spell.name, dmg=spell.damage, enemy_health=enemy_health
                    ))
                else:
                    print('Enemy is dead!')
                    exit()
            else:
                # normal attack
                enemy.take_damage(hero.attack(by='weapon'))
                enemy_health = enemy.get_health()
                if enemy_health > 0:
                    print('Hero hits with {wep_name} for {dmg} dmg. Enemy health is {enemy_health}'.format(
                        wep_name=hero.weapon.name, dmg=hero.attack(by='weapon'), enemy_health=enemy_health
                    ))
                else:
                    print('Enemy is dead!')
                    exit()


    def move_enemy(self, hero: Hero, enemy: Enemy):
        direction = ''
        if enemy.x_coord != hero.x_coord:
            if enemy.x_coord > hero.x_coord:
                direction = 'up'
                enemy.x_coord -= 1
            else:
                direction = 'down'
                enemy.x_coord += 1
        else:
            # y_coords
            if enemy.y_coord > hero.y_coord:
                direction = 'left'
                enemy.y_coord -= 1
            else:
                direction = 'right'
                enemy.y_coord += 1
        print('Enemy moves one square to the {dir} in order to get to the hero. This is his move.'.format(
            dir=direction
        ))





def main():
    from week04.day_01.dungeon import Dungeon
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
    map.hero_attack(by="spell")

if __name__ == "__main__":
    main()