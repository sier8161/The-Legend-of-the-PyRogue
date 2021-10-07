from random import randint

ROOMSIZE = 12 # (x,y)
WALL = "#"
EMPTY = " "
PLAYER = "@"


#returnerar ett dictionary som sparar data kring rummet. Bland annat tiles, koordinater och om dörrar finns eller inte
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


#printar rummet (främst för debug)
def render_room(room):
    tiles = room['tiles']
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
        

generate_floor(1)