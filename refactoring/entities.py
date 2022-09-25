class Entity():
    def __init__(self, pos, room, life, evasion, name, graphics):
        self.pos = pos
        self.room = room
        self.life = life
        self.evasion = evasion
        self.name = name
        self.graphics = GRAPHICS[graphics]

#class Player(Entity):

#class Monster(Entity):
