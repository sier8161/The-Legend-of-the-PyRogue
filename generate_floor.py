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

entities = {'PLAYER': {'pos':(MIDDLE, MIDDLE),
                      'room':0, #index i listan floor som innehåller rum
                      'life':2, #2: sköld, 1: ingen sköld, 0:död
                      'evasion': 0
                       }
            #lägg till monster här
            }





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
    
    place_entity('PLAYER', floor, entities['PLAYER']['pos'])
    return floor


#Här under finns en del funktioner som interagerar med tiles i rum

#Funktion som placerar en entitet vid bestämda koordinater i tupelform "(x,y)" i ett bestämt rum
def place_entity(entity, floor, where):
    tiles = floor[entities[entity]['room']]['tiles']
    room = floor[entities[entity]['room']]
    x = where[0]
    y = where[1]
    yaxis = tiles[x]
    yaxis[y] = GRAPHICS[entity]
    
def delete_entity(floor, entity):
    tiles = floor[entities[entity]['room']]['tiles']
    coords = entities[entity]['pos']
    x = coords[0]
    y = coords[1]
    yaxis = tiles[x]
    yaxis[y] = GRAPHICS['EMPTY']

def move_entity(floor, entity, where):
    tiles = floor[entities[entity]['room']]['tiles'] #OBS! tog player som key till entities för att jag inte förväntar mig att någon ska använda funktionen i ett annat rum och ville göra det enkelt
    delete_entity(floor, entity)
    place_entity(entity, floor, where)

#returnerar vad för entitet som befinner sig på en bestömd ruta
#Att göra: Fixa så att funktionen returnerar entitetens key i entities (dvs entitetens dictionary) genom att se vilken av entiteternas 'pos' som matchar med de gvian koordinaterna
def what_entity(floor, where):
    for entity in entities:
        if entities[entity]['pos'] == where:
            return entities[entity]

#Returnerar koordinaterna för en (1) entiet av en viss typ i ett rum
def find_entity(entityType, floor):
    y = 0
    for xAxis in tiles:
        if entityType in xAxis:
            return (y, xAxis.index(entityType))
        else:
            y += 1
        
#Returnerar ett rum med bestämda koordinater från ett bestämt floor 
def find_tiles_by_coord(floor, roomCoords):
    for room in floor:
        if room['coordinates']==roomCoords:
            return room['tiles']

def entity_action(floor, entity, moveTo): #Anropas när spelaren trycker på WASD eller när monster gör sitt drag. Om rutan är tom förflyttas man dit, om det finns en entitet där slår man den
    tiles = floor[entities[entity]['room']]['tiles']
    x = moveTo[0]
    y = moveTo[1]
    goalTile = floor[entities[entity]['room']]['tiles'][y][x]
    if goalTile == GRAPHICS['EMPTY']: #om rutan är tom förflyttas entiteten dit
        move_entity(floor, entity, moveTo)
        entities[entity]['pos'] = moveTo
        
        return False #returnerar False som assignas till playerTurn för att visa att ett drag har genomförts och att spelarens runda är över
    elif goalTile == GRAPHICS['TEMP_WALL']:
        return True
    elif goalTile == GRAPHICS['DOOR']:
        entities['PLAYER']['room'] = change_room(floor, moveTo)
        return True
    else: #om rutan inte är tom så
        if moveTo == entities['PLAYER']['pos'] and not entity == 'PLAYER':
            attack_entity(entity, entities['PLAYER']) #OBS! OBS! OBS! Anropar en icke-existerande funktion som jag tänker göra senare, attack_entity(attacker, target)
        if entity == 'PLAYER':
            attack_entity(entities['PLAYER'], what_entity(floor, moveTo))
            return False
   
#returnerar indexet i floor för det nya rummet
def change_room(floor, coords):
    index = 0
    roomCoords = floor[entities['PLAYER']['room']]['coordinates']
    roomX = roomCoords[0]
    roomY = roomCoords[1]
    if coords == (MIDDLE, 0): #flytta norrut
        for room in floor:
            if room['coordinates'] == (roomX, roomY+1):
                index = floor.index(room)
    elif coords == (SIDELENGTH, MIDDLE): #flytta öst
        for room in floor:
            if room['coordinates'] == (roomX+1, roomY):
                index = floor.index(room)
    elif coords == (0, MIDDLE): #flytta väst
        for room in floor:
            if room['coordinates'] == (roomX-1, roomY):
                index = floor.index(room)
    elif coords == (MIDDLE, SIDELENGTH): #flytta söderut
        for room in floor:
            if room['coordinates'] == (roomX, roomY-1):
                index = floor.index(room)
    return index
    
        
def playerTurn(floor):
    render_room(floor[entities['PLAYER']['room']]['tiles'])
    while True:
        playersTurn = True
        while playersTurn == True:
            if keyboard.is_pressed('w'): # move up
                playersTurn = entity_action(floor, 'PLAYER',
                                            (entities['PLAYER']['pos'][0]-1, entities['PLAYER']['pos'][1]))

            if keyboard.is_pressed('a'): # move left
                playersTurn = entity_action(floor,'PLAYER',
                                            (entities['PLAYER']['pos'][0], entities['PLAYER']['pos'][1]-1))

            if keyboard.is_pressed('s'): # move down
                playersTurn = entity_action(floor,'PLAYER',
                                            (entities['PLAYER']['pos'][0]+1, entities['PLAYER']['pos'][1]))

            if keyboard.is_pressed('d'):# move right
                playersTurn = entity_action(floor,'PLAYER',
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
    floor = generate_floor(1)
    playerTurn(floor)
    
testing_movement()
