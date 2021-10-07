from random import randint
import keyboard
ROOMSIZE = 12 # (x,y)
WALL = "#"
EMPTY = " "
PLAYER = "@"


#returnerar ett dictionary som sparar data kring rummet. Bland annat tiles, koordinater och om dörrar finns eller inte.
def generate_room(coords):
    tiles = []
    for horizLine in range(ROOMSIZE):
        vertLine = []
        if horizLine == 0 or horizLine == ROOMSIZE-1:
            for _ in range(ROOMSIZE):
                vertLine.append(WALL)
            tiles.append(vertLine)
            
        else:
            vertLine.append(WALL)
            for _ in range(ROOMSIZE-2):
                vertLine.append(EMPTY)
            vertLine.append(WALL)
            tiles.append(vertLine)
    room = {"tiles": tiles, "coordinates": coords,
            "T": False, "R": False, "B": False, "L": False}
    return room


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
    floor = [generate_room((0,0))]
    possibilities = [] #lista som lagrar alla möjliga koordinater där nästa rum kan placeras 
    for coords in possible_placements((0,0)):
        possibilities.append(coords)
    nRooms = 2**(level-1) + 5 #Antalet rum bestäms av parametern level
    for _ in range(nRooms):
        rng = randint(0, len(possibilities)-1)
        newRoomCoords = possibilities[rng]
        print(f"Rum {_} koordinater: ", newRoomCoords) #rad för debug
        floor.append(generate_room(newRoomCoords))
        for coords in possible_placements(newRoomCoords):
            if coords not in possibilities:
                possibilities.append(coords)
        possibilities.pop(possibilities.index(newRoomCoords))
    return floor

    
#Här under finns en del funktioner som interagerar med tiles i rum

#Funktion som placerar en entitet vid bestämda koordinater i tupelfrom "(x,y)" i ett bestämt rum
def place_entity(entity, room, tilecoords):
    x = tilecoords[0]
    y = tilecoords[1]
    tiles = room['tiles']
    yaxis = tiles[x]
    print(y)
    yaxis[y] = entity
def delete_entity(room, coords):
    tiles = room['tiles']
    x = coords[0]
    y = coords[1]
    yaxis = tiles[x]
    yaxis[y] = EMPTY

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
def find_entity(entitytype, room):
    tiles = room['tiles']
    x = 0
    for yaxis in tiles:
        if entitytype in yaxis:
            return (x, yaxis.index(entitytype))
        else:
            x += 1
        
            
    
    
    

#Returnerar ett rum med bestämda koordinater från ett bestämt floor 
def find_room_by_coord(floor, roomcoords):
    for room in floor:
        if room['coordinates']==roomcoords:
            return room['tiles']



floor = generate_floor(1)
def playerTurn(room):
    currentRoom = render_room(room)
    while True:
        playerCoords = find_entity(PLAYER, room)
        #För nuvarande så är movement inte fixat. Dessutom flyttar den sig åt höger istället för upp just nu. 
        if keyboard.is_pressed('w'):
            moveto = (playerCoords[0], (playerCoords[1] +1))
            move_entity(room, playerCoords, moveto)
            break
    render_room(room)
            
generate_floor(1)
place_entity(PLAYER, floor[0], (5,5))
playerTurn(floor[0])
