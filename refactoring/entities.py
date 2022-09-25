from random import randint
#Global variables
difficulty = 1

prompts = []

GRAPHICS = {
    'Player':{
        '2':'@',
        '1':'a',
        '0':'∩',
        'ERROR': '?'
    },
    'Monster':{
        '3':'3',
        '2':'2',
        '1':'1',
        'ERROR': '?'
    }
}
class EmptyTile():
    graphics = ' '

class Item():
    def __init__(self, pos, room, name):
        self.pos = pos
        self.room = room
        self.name = name


class Pyrogue(Item):
    graphics = 'B'

class Entity():
    
    def __init__(self, pos, room, life):
        self.pos = pos
        self.room = room
        self.life = life
        self.evasion = 5 * difficulty 
        self.graphics = GRAPHICS[self.__class__.__name__]
        self.set_graphic_corresponding_life()

    def set_graphic_corresponding_life(self):
        life_str = str(self.life)
        self.graphic = self.graphics[life_str]

    def move(self, where):
        pass
    
    def death_prompt(self):
        n = self.name
        prompts.append(n + " died!")

    def successful_attack_prompt(self, defender):
        n = self.name
        prompts.append(n + " successfully hit " + defender.name + " dealing damage!")
    
    def missed_attack_prompt(self, defender):
        n = self.name
        prompts.append(n + " tries to attack " + defender.name + " but misses!")
        
    def kill(self):
        self.death_prompt()
        self.room.remove_from_tile(self)
        del self

    def take_damage(self, amount):
        self.life = self.life - amount
        if self.life <= 0:
            self.kill()

    def attack(self, defender):
        hit_roll = randint(0,100)
        hit_successful = (hit_roll - defender.evasion) >= 15 * difficulty
        if hit_successful:
            self.successful_attack_prompt(defender)
            defender.take_damage(1)
            defender.set_graphic_corresponding_life()
        else:
            self.missed_attack_prompt(defender)


class Player(Entity):
    name = 'Player'

    
    


    
class Monster(Entity):
    name = 'Monster'


