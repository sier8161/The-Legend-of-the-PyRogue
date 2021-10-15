from random import randint
import keyboard
import os

clear_console = lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear') #för körning i kommandotolk

SIDELENGTH = 15 # Kvadratiskt rum med sidlängd SIDELENGTH
MIDDLE = int(SIDELENGTH/2)
GRAPHICS={  'PLAYER':'@',
            'PLAYER_DAMAGED':'a',
            'TL_WALL':'╔', #TL står för top-left
            'TR_WALL':'╗', #TR står för top-right
            'BL_WALL':'╚', #BL står för bottom-left
            'BR_WALL':'╝', #BR står för bottom-right
            'V_WALL':'║',  #V står för vertical
            'H_WALL':'═',  #H står för horizontal
            'TEMP_WALL':'#',#Temporär tile för att rendera alla väggar
            'DOOR': 'd',
            'EMPTY':' ',
            'NEXT_FLOOR':'x',
            'ENEMY_1':'1',
            'ENEMY_2':'2',
            'ENEMY_3':'3',
            'ENEMY_SLEEPING':'Z',
            'SHIELD':'H',
            'PIROGUE':'B'}
floor = []
level = 1
entities = {'PLAYER': {'pos':(MIDDLE, MIDDLE),
                      'room':0, #index i listan floor som innehåller rum
                      'life':2, #2: sköld, 1: ingen sköld, 0:död
                      'evasion': 0
                       }
            #lägg till monster här
            }

monsterCount = 0 #
# generate_monster är en procedur som ändrar den globala dictionaryn entities för att lägga till ett monster.
# Parametrar in till denna funktion; diff:integer med svårighetsgrad på monstret, room: integer för index på
# rummet i floor-listan som den skall genereras i, och coords: tupel med integers för x och y-värden.
# sidoeffekter: ändrar den globala dictionaryn entities för att lägga till ett monster, och ändrar globala variabeln monsterCount
def generate_monster(diff,where,room):
    global monsterCount
    life = 0
    evasion = 0
    for _ in range(diff):
        life += 1 #temporära värden
        evasion += 2 #ändra dessa sedan när vi har funderat ut hur vi vill göra med liv och evasion
    entities[f'MONSTER_{str(monsterCount)}'] = {'pos':where,
                                                'room':room,
                                                'life':life,
                                                'evasion':evasion,
                                                }
    place_entity(f'MONSTER_{str(monsterCount)}', entities[f'MONSTER_{str(monsterCount)}']['room'])
    monsterCount += 1

def generate_room(coords): #returnerar ett dictionary som sparar data kring rummet. Bl.a tiles, koordinater och om dörrar finns eller inte.
    tiles = []
    for horizLine in range(SIDELENGTH):
        vertLine = []
        if horizLine == 0 or horizLine == SIDELENGTH-1:
            for _ in range(SIDELENGTH):
                vertLine.append(GRAPHICS['TEMP_WALL'])
        else:
            vertLine.append(GRAPHICS['TEMP_WALL'])
            for _ in range(SIDELENGTH-2):
                vertLine.append(GRAPHICS['EMPTY'])
            vertLine.append(GRAPHICS['TEMP_WALL'])
        tiles.append(vertLine)
    room = {"tiles": tiles, #tiles[y][x], koordinatsystem som i 3dje kvadranten
            "coordinates": coords,
            "doors": {"T": False, "B": False, "L": False, "R": False}} #dörrarna är (up down left right)
    return room

def needed_doors(room, possibilities): #Sidoeffekt: Ändrar nycklarnas booelska värden i doors-ordboken så att man vet vilka håll som rummen behöver ha dörrar till
    roomCoords = room['coordinates']
    x = roomCoords[0]
    y = roomCoords[1]
    neighbouringRooms = []
    for coords in possible_placements(roomCoords):
        neighbouringRooms.append(coords)
    for coords in neighbouringRooms:
        if not coords in possibilities:
            neighbouringRooms.remove(coords)
        if coords == (x-1,y):
            room['doors']['L'] = True
        elif coords == (x+1,y):
            room['doors']['R'] = True
        elif coords == (x,y-1):
            room['doors']['B'] = True
        elif coords == (x,y+1):
            room['doors']['T'] = True
            
def create_doors(room):
    tiles = room['tiles']
    if room['doors']['L'] == True:
        tiles[MIDDLE][0] = GRAPHICS['DOOR']
    if room['doors']['R'] == True:
        tiles[MIDDLE][SIDELENGTH-1] = GRAPHICS['DOOR']
    if room['doors']['T'] == True:
        tiles[0][MIDDLE] = GRAPHICS['DOOR']
    if room['doors']['B'] == True:
        tiles[SIDELENGTH-1][MIDDLE] = GRAPHICS['DOOR']
        
#printar rummet
def render_room(tiles):
    clear_console()
    for vertLine in tiles:
        for tile in vertLine:
            print(tile, end="")
        print("\n", end="")
        
#returnerar en lista av tuples där varje tuple är koordinater som ligger brevid ett bestämt rum
def possible_placements(roomCoords):
    x = roomCoords[0]
    y = roomCoords[1]
    listy = [((x+1), y), ((x-1), y), (x, (y-1)), (x, (y+1))]
    return listy    
    
#Returnerar en lista bestående av dictionaries som representerar alla rum
#problem med funktionen: det blir en enda stor klump av alla rum. Om man inte vill ha det så, hur gör man?
def generate_floor(level):
    #skapar första rummet vid 0,0
    global floor
    floor = [generate_room((0,0), )]
    existingRooms= [(0,0)]
    possibilities = [] #lista som lagrar alla möjliga koordinater där nästa rum kan placeras 
    for coords in possible_placements((0,0)):
        possibilities.append(coords)
    nRooms = 2**(level-1) + 5 #Antalet rum bestäms av parametern level
    for _ in range(nRooms):
        rng = randint(0, len(possibilities)-1)
        newRoomCoords = possibilities[rng]
        print(f"Rum {_+2} koordinater: ", newRoomCoords) #rad för debug
        floor.append(generate_room(newRoomCoords, ))
        for coords in possible_placements(newRoomCoords):
            if coords not in possibilities:
                possibilities.append(coords)
        possibilities.pop(possibilities.index(newRoomCoords))
    for room in floor:
        needed_doors(room, possibilities)
        create_doors(room)
    entities['PLAYER']['room'] = randint(0, nRooms) #slumpar vilket rum spelaren börjar i
    place_entity('PLAYER', entities['PLAYER']['pos'])


#Här under finns en del funktioner som interagerar med tiles i rum

#Funktion som placerar en entitet vid bestämda koordinater i tupelform "(x,y)" i ett bestämt rum
def place_entity(entity, where):
    tiles = floor[entities[entity]['room']]['tiles']
    x = where[0]
    y = where[1]
    yaxis = tiles[x]
    if entity == 'PLAYER':
        graphics = GRAPHICS[entity]
    else:
        diff = entity['life']
        graphics = GRAPHICS[f'ENEMY_{diff}']
    yaxis[y] = graphics
    
def delete_entity(entity):
    tiles = floor[entities[entity]['room']]['tiles']
    coords = entities[entity]['pos']
    x = coords[0]
    y = coords[1]
    yaxis = tiles[x]
    yaxis[y] = GRAPHICS['EMPTY']

def move_entity(entity, goalcoords):
    tiles = floor[entities[entity]['room']]['tiles'] #OBS! tog player som key till entities för att jag inte förväntar mig att någon ska använda funktionen i ett annat rum och ville göra det enkelt
    delete_entity(entity)
    place_entity(entity, goalcoords)

#returnerar vad för entitet som befinner sig på en bestömd ruta
def what_entity(room, where):
    tiles = room['tiles']
    x = where[0]
    y = where[1]
    yaxis = tiles[x]
    return yaxis[y]

#Returnerar koordinaterna för en (1) entiet av en viss typ i ett rum
def find_entity(entityType):
    y = 0
    for xAxis in tiles:
        if entityType in xAxis:
            return (y, xAxis.index(entityType))
        else:
            y += 1
        
#Returnerar ett rum med bestämda koordinater från ett bestämt floor 
def find_tiles_by_coord(roomCoords):
    for room in floor:
        if room['coordinates']==roomCoords:
            return room['tiles']

def entity_action(entity, moveTo): #Anropas när spelaren trycker på WASD eller när monster gör sitt drag. Om rutan är tom förflyttas man dit, om det finns en entitet där slår man den
    tiles = floor[entities[entity]['room']]['tiles']
    x = moveTo[0]
    y = moveTo[1]
    goalTile = floor[entities[entity]['room']]['tiles'][y][x]
    if goalTile == GRAPHICS['EMPTY']: #om rutan är tom förflyttas entiteten dit
        move_entity(entity, moveTo)
        entities[entity]['pos'] = moveTo
        
        return False #returnerar False som assignas till playerTurn för att visa att ett drag har genomförts och att spelarens runda är över
    elif goalTile == GRAPHICS['TEMP_WALL'] or goalTile == GRAPHICS['DOOR']:
        return True
    else: #om rutan inte är tom så
        if moveTo == entities['PLAYER']['pos'] and not entity == 'PLAYER':
            attack_entity(entity, entities['PLAYER']) #OBS! OBS! OBS! Anropar en icke-existerande funktion som jag tänker göra senare, attack_entity(attacker, target)
        if entity == 'PLAYER':
            for i in range(6):
                if moveTo == entities[f'{i}']['pos']:
                    attack_entity(entities['PLAYER'], entities[f'{i}'])
                    return False
   
            
def playerTurn():
    render_room(floor[entities['PLAYER']['room']]['tiles'])
    while True:
        playersTurn = True
        while playersTurn == True:
            if keyboard.is_pressed('w'): # move up
                playersTurn = entity_action('PLAYER',
                                            (entities['PLAYER']['pos'][0]-1, entities['PLAYER']['pos'][1]))

            if keyboard.is_pressed('a'): # move left
                playersTurn = entity_action('PLAYER',
                                            (entities['PLAYER']['pos'][0], entities['PLAYER']['pos'][1]-1))

            if keyboard.is_pressed('s'): # move down
                playersTurn = entity_action('PLAYER',
                                            (entities['PLAYER']['pos'][0]+1, entities['PLAYER']['pos'][1]))

            if keyboard.is_pressed('d'):# move right
                playersTurn = entity_action('PLAYER',
                                            (entities['PLAYER']['pos'][0], entities['PLAYER']['pos'][1]+1))
            if keyboard.is_pressed('q'): #attack
                pass
            if keyboard.is_pressed('e'): #wait
                pass
                playersTurn = False
        
        render_room(floor[entities['PLAYER']['room']]['tiles'])

def testing_create_doors(door):
    testroom = generate_room((0,0))
    render_room(testroom)
    testroom['doors'][door] = True
    create_doors(testroom)
    render_room(testroom)
    
def testing_movement():
    generate_floor(level)
    generate_monster(1,(4,4),floor[0])
    playerTurn()
    
testing_movement()
