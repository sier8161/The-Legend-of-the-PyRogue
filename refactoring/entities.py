from random import randint

difficulty = 1

prompts = []

GRAPHICS={  'PLAYER':'@',
            'PLAYER_DAMAGED':'a',
            'PLAYER_DEAD':'∩',
            'TL_WALL':'╔', #TL står för top-left
            'TR_WALL':'╗', #TR står för top-right
            'BL_WALL':'╚', #BL står för bottom-left
            'BR_WALL':'╝', #BR står för bottom-right
            'V_WALL':'║',  #V står för vertical
            'H_WALL':'═',  #H står för horizontal
            'H_DOOR': '─',
            'V_DOOR': '│',
            'EMPTY':' ',
            'NEXT_FLOOR':'^',
            'ENEMY_1':'1',
            'ENEMY_2':'2',
            'ENEMY_3':'3',
            'ENEMY_SLEEPING':'z',
            'POTION':'H',
            'PIROGUE':'B',
            'KEY':'╖',}

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
    name = ""
    def __init__(self, pos, room, life, evasion):
        self.pos = pos
        self.room = room
        self.life = life
        self.evasion = evasion
    
    def move(self, where):
        pass
    
    def death_prompt(self):
        n = self.name
        prompts.append(n + " died!")
        
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
            defender.take_damage(1)


class Player(Entity):
    name = 'Player'
    #def __init__(self):
    #    self.set_graphics_corresponding_life(self)
    
    possible_graphics = {
        'PLAYER':'@',
        'PLAYER_DAMAGED':'a',
        'PLAYER_DEAD':'∩',
        'ERROR': '?'
    } 

    def set_graphics_corresponding_life(self):
        l = self.life
        g = self.possible_graphics
        if l == 2:
            self.graphics = g['PLAYER']
        elif l == 1:
            self.graphics = g['PLAYER_DAMAGED']
        elif l == 0:
            self.graphics = g['PLAYER_DEAD']
        else:
            self.graphics = g['ERROR']
    
class Monster(Entity):
    name = 'Monster'
    #def __init__(self):
    #    self.set_graphics_corresponding_life(self)
    
    possible_graphics = {
        '3_HP':'3',
        '2_HP':'2',
        '1_HP':'1',
        'ERROR': '?'
    } 

    def set_graphics_corresponding_life(self):
        l = self.life
        g = self.possible_graphics
        if 0 <= l and l <= 3:
            self.graphics = g[l + '_HP']
        else:
            self.graphics = g['ERROR']
