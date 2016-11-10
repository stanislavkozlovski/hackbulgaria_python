"""
This module holds our classes for in-game creatures and the hero
"""
from .spells import Spell

class Entity:
    def __init__(self, name: str, title: str, health: int, mana: int, x_coord: int=0, y_coord: int=0):
        self.name = name
        self. title = title
        self.max_health = health
        self.max_mana = mana
        self._health = health
        self._mana = mana
        self.spells = []  # type: [Spell]
        self.x_coord = x_coord
        self.y_coord = y_coord

    def set_coordinates(self, x, y):
        self.x_coord = x
        self.y_coord = y

    def equip(self, weapon):
       self.weapon = weapon  # type:

    def learn(self, spell: Spell):
        self.spells.append(spell)

    def is_in_range(self, x, y, range: int):
        return abs(self.x_coord - x) <= range and abs(self.y_coord - y) <= range

    def get_attack_damage(self, by: str):
        """ get the damage we would deal in an attack by calculating
        if we'll attack by spell or weapon """
        if by == 'spell':
            if self.spells:
                # get the spell with the maximum damage that we have enough mana for
                available_spells = [spell for spell in self.spells if self._mana >= spell.mana_cost]
                if not available_spells:
                    return None

                spell = max(available_spells, key= lambda spell: spell.damage) # type: Spell
                if spell:
                    return spell
            else:
                print('{} does not know any spells.'.format(self.name))
                return None
        else:
            return self.weapon.damage

    def attack(self, victim):
        raise NotImplementedError


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

    @property
    def health(self) -> int:
        return self._health
    @property
    def mana(self) -> int:
        return self._mana

    def is_alive(self) -> bool:
        return self._health > 0

    def can_cast(self, spell: Spell) -> bool:
        return self._mana >= spell.mana_cost


class Hero(Entity):
    def __init__(self, name: str, title: str, health: int, mana: int, mana_regen_rate: int):
        super().__init__(name, title, health, mana)
        self.mana_renegeration_rate = mana_regen_rate

    def attack(self, victim: 'Enemy'):
        # see if we should attack by spell or weapon by comparing their damage
        spell = self.get_attack_damage(by='spell')
        if spell and spell.damage >= self.get_attack_damage(by='weapon'):
            # spell damage is higher, attack by spell
            self.cast_spell(spell)  # use the mana for the spell
            victim.take_damage(spell.damage)
            victim_health = victim.health
            attack_message = 'Hero casts a {spell_name}, hits Enemy for {dmg} dmg.'.format(
                spell_name=spell.name, dmg=spell.damage)
        else:
            # normal attack
            damage_blow = self.get_attack_damage(by='weapon')  # type: int
            victim.take_damage(damage_blow)
            victim_health = victim.health
            attack_message = 'Hero hits with {wep_name} for {dmg} dmg.'.format(
                wep_name=self.weapon.name, dmg=damage_blow)

        print('{attack_message} Enemy health is {victim_health}'.format(
            attack_message=attack_message, victim_health=victim_health if victim_health >= 0 else 0
        ))
        if victim_health <= 0:
            print('Enemy is dead!')
            exit()

    def initial_attack(self, victim: 'Enemy', initial_attack: Spell or int):
        if initial_attack:
            if isinstance(initial_attack.__class__, Spell.__class__):
                spell_dmg = self.cast_spell(initial_attack)  # casts the spell and uses the mana
                victim.take_damage(spell_dmg)
                attack_message = 'Hero casts a {spell_name}, hits Enemy for {dmg} dmg.'.format(
                    spell_name=initial_attack.name, dmg=spell_dmg)
            else:
                victim.take_damage(initial_attack)
                attack_message = 'Hero hits with {wep_name} for {dmg} dmg.'.format(
                    wep_name=self.weapon.name, dmg=initial_attack)

            victim_health = victim.health
            print('{attack_message} Enemy health is {victim_health}'.format(
                attack_message=attack_message, victim_health=victim_health if victim_health >= 0 else 0
            ))
            if victim_health <= 0:
                print('Enemy is dead!')
                exit()


class Enemy(Entity):
    def __init__(self, name: str, title: str, health: int, mana: int, damage: int, x_coord: int, y_coord: int):
        super().__init__(name, title, health, mana)
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.damage = damage

    def attack(self, victim: Hero):
        # see if we should attack by spell or weapon by comparing their damage
        spell = self.get_attack_damage(by='spell')
        if spell and spell.damage >= self.get_attack_damage(by='weapon'):
            # spell damage is higher, attack by spell
            self.cast_spell(spell)  # use the mana for the spell
            victim.take_damage(spell.damage)
            victim_health = victim.health
            attack_message = 'Enemy casts a {spell_name}, hits Hero for {dmg} dmg.'.format(
                spell_name=spell.name, dmg=spell.damage)
        else:
            # normal attack
            if victim.is_in_range(x=self.x_coord, y=self.y_coord, range=1):
                damage_blow = self.get_attack_damage(by='weapon')  # type: int
                victim.take_damage(damage_blow)
                victim_health = victim.health
                attack_message = 'Enemy hits with {wep_name} for {dmg} dmg.'.format(
                    wep_name=self.weapon.name, dmg=damage_blow)
            else:
                self.move_toward(victim)
                return

        print('{attack_message} Hero health is {victim_health}'.format(
            attack_message=attack_message, victim_health=victim_health if victim_health >= 0 else 0
        ))
        if victim_health <= 0:
            print('Enemy is dead!')
            exit()

    def move_toward(self, hero: Hero):
        # here the enemy moves toward the hero to fight him, if the hero
        # engaged him from range
        if self.x_coord != hero.x_coord:
            if self.x_coord > hero.x_coord:
                direction = 'up'
                self.x_coord -= 1
            else:
                direction = 'down'
                self.x_coord += 1
        else:
            # y_coords
            if self.y_coord > hero.y_coord:
                direction = 'to the left'
                self.y_coord -= 1
            else:
                direction = 'to the right'
                self.y_coord += 1

        print('Enemy moves one square {dir} in order to get to the hero. This is his move.'.format(
            dir=direction
        ))