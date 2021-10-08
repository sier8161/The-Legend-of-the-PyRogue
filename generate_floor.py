from random import randint
#import keyboard
SIDELENGTH = 15 # Kvadratiskt rum med sidlängd SIDELENGTH
MIDDLE = int(SIDELENGTH/2)
GRAPHICS={  'PLAYER':'@',
            'TL_WALL':'╔', #TL står för top-left
            'TR_WALL':'╗', #TR står för top-right
            'BL_WALL':'╚', #BL står för bottom-left
            'BR_WALL':'╝', #BR står för bottom-right
            'V_WALL':'║',
            'H_WALL':'═',
            'TEMP_WALL':'#',
            'EMPTY':' ',
            'ENEMY_1':'1',
            'ENEMY_2':'2',
            'ENEMY_3':'3',
            'HP_POT':'H',
            'POWERUP':'P',}

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
    room = {"tiles": tiles, "coordinates": coords, "doors": {"T": False, "B": False, "L": False, "R": False}} #dörrarna är (up down left right)
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
        for i in range(3):
            tiles[int((SIDELENGTH-3)/2) + i][0] = GRAPHICS['EMPTY']
    if room['doors']['R'] == True:
        for i in range(3):
            tiles[int((SIDELENGTH-3)/2) + i][SIDELENGTH-1] = GRAPHICS['EMPTY']
    if room['doors']['T'] == True:
        for i in range(3):
            tiles[0][int((SIDELENGTH-3)/2) + i] = GRAPHICS['EMPTY']
    if room['doors']['B'] == True:
        for i in range(3):
            tiles[SIDELENGTH-1][int((SIDELENGTH-3)/2) + i] = GRAPHICS['EMPTY']
        

#printar rummet, returnerar även koordinaterna för rummet
def render_room(room):
    tiles = room['tiles']
    for vertLine in tiles:
        for tile in vertLine:
            print(tile, end="")
            
        print("\n", end="")
    return room['coordinates']
            
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
    possibilities = [] #lista som lagrar alla möjliga koordinater där nästa rum kan placeras 
    for coords in possible_placements((0,0)):
        possibilities.append(coords)
    nRooms = 2**(level-1) + 5 #Antalet rum bestäms av parametern level
    for _ in range(nRooms):
        rng = randint(0, len(possibilities)-1)
        newRoomCoords = possibilities[rng]
        print(f"Rum {_} koordinater: ", newRoomCoords) #rad för debug
        floor.append(generate_room(newRoomCoords, ))
        for coords in possible_placements(newRoomCoords):
            if coords not in possibilities:
                possibilities.append(coords)
        possibilities.pop(possibilities.index(newRoomCoords))
    for room in floor:
        needed_doors(room, possibilities)
        create_doors(room)
    
    return floor

#Här under finns en del funktioner som interagerar med tiles i rum

#Funktion som placerar en entitet vid bestämda koordinater i tupelform "(x,y)" i ett bestämt rum
def place_entity(entity, room, tilecoords):
    x = tilecoords[0]
    y = tilecoords[1]
    tiles = room['tiles']
    yaxis = tiles[x]
    yaxis[y] = entity
    
def delete_entity(room, coords):
    tiles = room['tiles']
    x = coords[0]
    y = coords[1]
    yaxis = tiles[x]
    yaxis[y] = GRAPHICS['EMPTY']

def move_entity(room, currentcoords, goalcoords):
    theEntity = what_entity(room, currentcoords)
    tiles = room['tiles']
    delete_entity(room, currentcoords)
    place_entity(theEntity, room, goalcoords)

#returnerar vad för entitet som befinner sig på nuvarande rutan
def what_entity(room, tilecoords):
    tiles = room['tiles']
    x = tilecoords[0]
    y = tilecoords[1]
    yaxis = tiles[x]
    return yaxis[y]

#OBS! Denna funktion är inte ännu anpassad för att hitta flera entiteter.
#Returnerar koordinaterna för en entiet av en viss typ i ett rum
def find_entity(entityType, room):
    tiles = room['tiles']
    y = 0
    for xAxis in tiles:
        if entityType in xAxis:
            return (y, xAxis.index(entityType))
        else:
            y += 1
        
#Returnerar ett rum med bestämda koordinater från ett bestämt floor 
def find_room_by_coord(floor, roomCoords):
    for room in floor:
        if room['coordinates']==roomCoords:
            return room['tiles']

def playerTurn(room):
    currentRoom = render_room(room)
    while True:
        playerCoords = find_entity(GRAPHICS['PLAYER'], room)
        #För nuvarande så är movement inte fixat.
        if keyboard.is_pressed('w'): # move up
            moveto = (playerCoords[0]-1, playerCoords[1])
            move_entity(room, playerCoords, moveto)
        if keyboard.is_pressed('a'): # move left
            moveto = (playerCoords[0], playerCoords[1]-1)
            move_entity(room, playerCoords, moveto)
        if keyboard.is_pressed('s'): # move down
            moveto = (playerCoords[0]+1, playerCoords[1])
            move_entity(room, playerCoords, moveto)
        if keyboard.is_pressed('d'):# move right
            moveto = (playerCoords[0], playerCoords[1]+1)
            move_entity(room, playerCoords, moveto)
        if keyboard.is_pressed('q'): #attack
            move_entity(room, playerCoords, moveto)
        if keyboard.is_pressed('e'): #wait
            None
    render_room(room)


def testing_create_doors(door):
    testroom = generate_room((0,0))
    render_room(testroom)
    testroom['doors'][door] = True
    create_doors(testroom)
    render_room(testroom)


generate_floor(1)
#place_entity(GRAPHICS['PLAYER'], floor[0], (MIDDLE,MIDDLE))
#playerTurn(floor[0])
