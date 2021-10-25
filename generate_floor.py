#coding=utf-8
from random import randint
from random import shuffle
import keyboard
import os
from animations import SPLASHFRAMES, MENUFRAMES
from time import sleep

clear_console = lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear') #för körning i kommandotolk

SIDELENGTH = 15 # Kvadratiskt rum med sidlängd SIDELENGTH
MIDDLE = int(SIDELENGTH/2)
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

def initGlobalVariables():
    global game_over, keyDropped, keyFound, pirogueDropped, pirogueEaten, prompt
    global floor, level, monstersAlive, maxMonstersAlive, difficulty, entities, monstersKilled
    game_over = False
    keyDropped = False
    keyFound = False
    pirogueDropped = False
    pirogueEaten = False
    prompt = ""
    floor = []
    level = 0
    monstersAlive = 0
    maxMonstersAlive = 0
    monstersKilled = 0
    difficulty = 2
    
    entities = {'PLAYER':{'pos':(MIDDLE, MIDDLE),
                    'room':0,  #OBS! Nyckel 'room' som en entitet har är ett index för listan floor där indexet motsvarar ett dictionary som är rummet i fråga
                    'life':2, #2: sköld, 1: ingen sköld, 0:död
                    'evasion': 20, #sätts efter mainMenu() till (4-difficulty)*20 (beginner = 60, normal = 40, ILTD = 20)
                    'name':'Player'
                    }
                #MONSTER_1 , MONSTER_2, osv till MONSTER_{monstersAlive} kommer finnas i denna lista efter att de genererats
                }

# generate_monster är en procedur som ändrar den globala dictionaryn entities för att lägga till ett monster.
# Parametrar in till denna funktion; diff:integer med svårighetsgrad på monstret, room: integer för index på
# rummet i floor-listan som den skall genereras i, och coords: tupel med integers för x och y-värden.
# sidoeffekter: ändrar den globala dictionaryn entities för att lägga till ett monster, och ändrar globala variabeln monstersAlive
def generate_monster(diff,where,room): #OBS! Nyckel 'room' som entities har är ett index för listan floor där indexet motsvarar ett dictionary som är ett rum
    global monstersAlive
    monstersAlive += 1 #iom att vi ökar monstercount innan monstret skapas så kommer första monstret få 'entiteten' MONSTER_1
    life = 0
    evasion = 0
    for _ in range(diff):
        life += 1 #temporära värden
        evasion += 10 #ändra dessa sedan när vi har funderat ut hur vi vill göra med liv och evasion
    entities[f'MONSTER_{str(monstersAlive)}'] = {'pos':where,
                                                'room':room,
                                                'life':life,
                                                'evasion':evasion,
                                                'name': 'Monster'
                                                }
    place_entity(f'MONSTER_{str(monstersAlive)}', entities[f'MONSTER_{str(monstersAlive)}']['pos'])

#procedur som anropar generate_monster flertalet gånger för att skapa en mängd 'quantity' monster på slumpmässiga platser med slumpmässiga stats.
#OBS! EJ KLAR då den skall vikta antal fiender mot svårighetsgrad osv för att balansera spelet, vi får titta på det senare.
def generate_monsters():
    global maxMonstersAlive
    maxMonstersAlive = 3+(difficulty*level)
    diffSum = level*difficulty*2
    # diffSum beginner: lvl 1 2 3 4 5 6 7 8 9 10 = 2  4  6  8 10 12 14 16 18 20
    # diffSum default:  lvl 1 2 3 4 5 6 7 8 9 10 = 4  8 12 16 20 24 28 32 36 40
    # diffSum ILTD:     lvl 1 2 3 4 5 6 7 8 9 10 = 6 12 18 24 30 36 42 48 54 60
    # en 2a 'kostar' 1 från diffsum, en 3a kostar 2.
    for _ in range(maxMonstersAlive):
        # monster beginner: lvl 1 2 3 4 5 6 7 8 9 10 = 3+1  3+2  3+3  3+4  3+5  3+6  3+7  3+8  3+9  3+10 
        # monster default:  lvl 1 2 3 4 5 6 7 8 9 10 = 3+2  3+4  3+6  3+8  3+10 3+12 3+14 3+16 3+18 3+20
        # monster ILTD:     lvl 1 2 3 4 5 6 7 8 9 10 = 3+3  3+6  3+9  3+12 3+15 3+18 3+21 3+24 3+27 3+30
        rDiff = randint(1, 3)
        rX,rY,rRoom = (0,0,0)
        while floor[rRoom]['tiles'][rX][rY] != GRAPHICS['EMPTY']:
            rX = randint(2, SIDELENGTH-3)
            rY = randint(2, SIDELENGTH-3)
            rRoom = randint(0,(len(floor)-1))
        diffSum -= (rDiff-1)
        if diffSum <= 0:
            rDiff = 1
        generate_monster(rDiff,(rX,rY),rRoom)

#Denna funktion returnerar ett dictionary som representerar ett rum datamässigt. 
#Argument: coords: Avgör vilka koordinater som rummet har i nivån (floor).
#Anropas i funktionen generate_floor.
def generate_room(coords): #returnerar ett dictionary som sparar data kring rummet. Bl.a tiles, koordinater och om dörrar finns eller inte.
    tiles = []
    for vertLine in range(SIDELENGTH):
        horizLine = []
        if vertLine == 0:
            horizLine.append(GRAPHICS['TL_WALL'])
        if vertLine == SIDELENGTH-1:
            horizLine.append(GRAPHICS['BL_WALL'])
        if vertLine == 0 or vertLine == SIDELENGTH-1:
            for _ in range(SIDELENGTH-2):
                horizLine.append(GRAPHICS['H_WALL'])
            if vertLine == 0:
                horizLine.append(GRAPHICS['TR_WALL'])
            if vertLine == SIDELENGTH-1:
                horizLine.append(GRAPHICS['BR_WALL'])
        
        else:
            horizLine.append(GRAPHICS['V_WALL'])
            for _ in range(SIDELENGTH-2):
                horizLine.append(GRAPHICS['EMPTY'])
            horizLine.append(GRAPHICS['V_WALL'])
        tiles.append(horizLine)
    room = {"tiles": tiles, #tiles[y][x], koordinatsystem som i 3dje kvadranten
            "coordinates": coords,
            "doors": {"T": False, "B": False, "L": False, "R": False}} #dörrarna är (up down left right)
    return room

#Funktion som avgör vilka dörrar som kommer behövas skapas efter att alla rum i nivån är sammansatta.
#Sidoeffekten är att ett bestämt rums (dvs ett dictionary) booleska värden för om dörrar ska finnas ändras.
#Argument: room: ett dictionary (som representerar ett rum) som man vill använda funktionen på.
#Possibilities: en lista bestående av alla möjliga nya placeringar som skapats från generate_floor och används för att veta vilka dörrar som inte ska finnas. 
def needed_doors(room):
    roomCoords = room['coordinates']
    x, y = roomCoords
    for existingRoom in floor:
        coords = existingRoom['coordinates']
        if coords == (x-1,y):
            room['doors']['L'] = True
        elif coords == (x+1,y):
            room['doors']['R'] = True
        elif coords == (x,y-1):
            room['doors']['B'] = True
        elif coords == (x,y+1):
            room['doors']['T'] = True

#Sidoeffekt: ändrar argumentet "room"s (en dictionary) tiles så att de dörrar som ska finnas finns.
def create_doors(room):
    tiles = room['tiles']
    if room['doors']['L'] == True:
        tiles[MIDDLE-1][0] = GRAPHICS['BR_WALL']
        tiles[MIDDLE][0] = GRAPHICS['V_DOOR']
        tiles[MIDDLE+1][0] = GRAPHICS['TR_WALL']
    if room['doors']['R'] == True:
        tiles[MIDDLE-1][SIDELENGTH-1] = GRAPHICS['BL_WALL']
        tiles[MIDDLE][SIDELENGTH-1] = GRAPHICS['V_DOOR']
        tiles[MIDDLE+1][SIDELENGTH-1] = GRAPHICS['TL_WALL']
    if room['doors']['T'] == True:
        tiles[0][MIDDLE-1] = GRAPHICS['BR_WALL']
        tiles[0][MIDDLE] = GRAPHICS['H_DOOR']
        tiles[0][MIDDLE+1] = GRAPHICS['BL_WALL']
    if room['doors']['B'] == True:
        tiles[SIDELENGTH-1][MIDDLE-1] = GRAPHICS['TR_WALL']
        tiles[SIDELENGTH-1][MIDDLE] = GRAPHICS['H_DOOR']
        tiles[SIDELENGTH-1][MIDDLE+1] = GRAPHICS['TL_WALL']
        
#Sidoeffekt: tar bort allt som tidigare printats och printar rummet
def render_room(tiles):
    global prompt
    clear_console()
    for vertLine in tiles:
        for tile in vertLine:
            print(tile, end="")
        print("\n", end="")
    #print(floor[entities['PLAYER']['room']]['coordinates'])
    if keyFound:
        key = '╖'
    else:
        key = ''    
    print(f"Floor: {level} {key}")
    print(f'Kills: {monstersKilled}')
    
    print(prompt)
    if prompt != "":
        if os.name == 'nt':
            os.system('pause')
        else:
            os.system('read -s -n 1 -p "Press any key to continue..."')
        
            
    prompt = ""
#returnerar en lista av tuples där varje tuple är koordinater som ligger brevid ett bestämt rum
def possible_placements(roomCoords):
    y, x = roomCoords
    possibilities = [((y+1), x), ((y-1), x), (y, (x-1)), (y, (x+1))]
    return possibilities
    
def nearby_rooms(roomCoords, n): #returnerar en lista med alla rum som ligger max n steg från ett givet rums koordinater, anropas i generate_floor
    x,y = roomCoords
    nearbyRooms = [roomCoords]
    for i in range(1, n+1):
        for corners in [(n,n) , (n,-n), (-n,n), (-n,-n)]: #lägger till hörnen
            nearbyRooms.append((corners[0] + x, corners[1] + y))
        for coord in range(-(n-1), n):
             for coords in [(n, coord), (-n, coord), (coord, n), (coord, -n)]: #lägger till sidorna
                nearbyRooms.append((coords[0] + x, coords[1] + y))
    return nearbyRooms
    
#Skapar en lista (globalt) som representerar en floor datamässigt.
def generate_floor():
    global floor #skapar första rummet vid 0,0
    floor = [generate_room((0,0))]
    existingRoomCoords= [(0,0)]
    possibilities = possible_placements((0,0)) #lista som lagrar alla möjliga koordinater där nästa rum kan placeras 
    nRooms = difficulty*(level-1) + 5 #Antalet rum bestäms av level och difficulty
    # lvl 1 2 3 4 5 6 7 8 9 10 = 5  6  7  8  9  10 11 12 13 14 rum beginner
    # lvl 1 2 3 4 5 6 7 8 9 10 = 5  7  9  11 13 15 17 19 21 23 rum default
    # lvl 1 2 3 4 5 6 7 8 9 10 = 5  8  11 14 17 20 23 26 29 32 rum ILTD
    for _ in range(nRooms):
        rng = randint(0, len(possibilities)-1)
        newRoomCoords = possibilities[rng]
        existingRoomCoords.append(possibilities.pop(rng))
        #print(f"Rum {_+2} koordinater: ", newRoomCoords) #rad för debug (kan också användas vid presentationen)
        floor.append(generate_room(newRoomCoords))
        for coords in possible_placements(newRoomCoords):
            if not coords in possibilities:
                    if not coords in existingRoomCoords:
                        possibilities.append(coords)
    for room in floor:
        needed_doors(room)
        create_doors(room)
    entities['PLAYER']['room'] = randint(0, nRooms) #slumpar vilket rum spelaren börjar i
    
    #Denna del av koden skapar en tile i ett rum som tar en till nästa floor och som är placerad successivt längre bort från spelaren desto fler floors den klarar
    validRoomCoords =[]  
    i = 0      
    while validRoomCoords == []: #Om inga rum är kvar på listan, anropa nearby_rooms igen med level-n
        allRoomCoords = []
        for room in floor:   #Lägger till alla rums koordinater i en lista
            allRoomCoords.append(room['coordinates'])
        
        excludedRooms = []
        for n in range(1, level+1-i):
            for coords in  nearby_rooms(floor[entities['PLAYER']['room']]['coordinates'], n):
                excludedRooms.append(coords) #nearby_rooms returnerar en lista med alla rum som är max n steg (inklusive diagonalt) från ursprungsrummet
               
        for roomCoords in excludedRooms: #Tar bort alla rum som är exkluderade från listan med alla rums koordinater
            if roomCoords in allRoomCoords:
                allRoomCoords.remove(roomCoords)
        
        for roomCoords in allRoomCoords: #Lägger till de resterande rummen som blev kvar i listan med giltiga rum
            validRoomCoords.append(roomCoords)
        
        i += 1
    
    #Slumpar en av koordinaterna av de möjliga som finns till rummet där man tar sig till nästa floor 
    nextFloorRoomCoords = validRoomCoords[randint(0, len(validRoomCoords)-1)]
    
    for room in floor:
        if room['coordinates'] == nextFloorRoomCoords:
            nextFloorRoom = room
    nextFloorRoom['tiles'][MIDDLE][MIDDLE] = GRAPHICS['NEXT_FLOOR']
    
    place_entity('PLAYER', entities['PLAYER']['pos'])

#Här under finns en del funktioner som interagerar med tiles i rum

#Funktion som placerar en entitet vid bestämda koordinater. (GRAFIK)
#Argumentet entity är vilken entitet och where är koordinaterna i (x,y) form
def place_entity(entity, where):
    tiles = floor[entities[entity]['room']]['tiles']
    graphics = GRAPHICS['PLAYER_DEAD']
    if entity == 'PLAYER':
        if entities['PLAYER']['life'] == 2:
            graphics = GRAPHICS['PLAYER']
        elif entities['PLAYER']['life'] == 1:
            graphics = GRAPHICS['PLAYER_DAMAGED']
        elif entities['PLAYER']['life'] == 0:
            global game_over
            graphics = GRAPHICS['PLAYER_DEAD']
            game_over = True
    else:
        monsterLife = entities[entity]['life']
        if monsterLife > 0:
            graphics = GRAPHICS[f'ENEMY_{monsterLife}']
        else:
            global monstersAlive, monstersKilled
            monstersAlive -= 1
            monstersKilled += 1
            graphics = droppedItems()
            del entities[entity]
        
    x, y = where #då 'where' är en tupel blir detta en split av tupeln, enligt x, y = (x,y)
    
    tiles[y][x] = graphics
    

#Tar bort en entitet. Tar entity som argument vilket är den entitet som ska tas bort (ÄNDRAR ENDAST GRAFISK REPRESENTATION)
def delete_entity(entity):
    tiles = floor[entities[entity]['room']]['tiles']
    coords = entities[entity]['pos']
    x, y = coords #då 'coords' är en tupel blir detta en split av tupeln, enligt x, y = (x,y)
    yaxis = tiles[y]
    yaxis[x] = GRAPHICS['EMPTY']
    
def update_entity(entity,where):
    delete_entity(entity)
    place_entity(entity, where)

#Flyttar en entitet till bestämda koordinater. Tar argumenten entity vilket är vilken entitet och where som är koordinaterna för vart den ska flyttas
def move_entity(entity, where):
    tiles = floor[entities[entity]['room']]['tiles'] #OBS! tog player som key till move_entity('entity',_) för att jag inte förväntar mig att någon ska använda funktionen i ett annat rum och ville göra det enkelt
    delete_entity(entity)
    place_entity(entity, where)
    entities[entity]['pos'] = where

#returnerar vad för entitet som befinner sig på en bestömd ruta. Tar argumenten room som är rummet som man vill leta efter en entitet i
#och where som är vilka koordinater i tiles där man vill veta vilken entitet som befinner sig där
def what_entity(room, where):
    for entity in entities:
        if entities[entity]['room'] == room:
            if entities[entity]['pos'] == where:
                return entity
  
#Returnerar koordinaterna för en (1) entitet av en viss typ i ett rum 
def where_entity(room,entity):
    if entity in entities:
        if entities[entity]['room'] == room:
            where = entities[entity]['pos']
            return where
            
#Förflyttar spelaren från ett rum till ett annat. Tar argumenten room som är det rum man önskar att flytta till och where som är de koordinater man önskar att flytta till i det nya rummet
def move_between_rooms(room, where):
    delete_entity('PLAYER')
    entities['PLAYER']['room'] = floor.index(room)
    place_entity('PLAYER', where)
    entities['PLAYER']['pos'] = where
    
def next_floor():
    global level
    global monstersAlive
    level += 1
    monstersAlive = 0
    generate_floor()
    generate_monsters()
    playerTurn()

def droppedItems():
    global pirogueDropped,keyDropped
    diceRoll = randint(0,100)
    if not keyDropped and diceRoll >=((100/maxMonstersAlive)*monstersAlive)-10*(4-difficulty):
        #chans för key att droppa är nu baserad på antalet monster man dödat av totalen och ökar
        
        keyDropped = True
        return GRAPHICS['KEY'] 
    elif level >= 5 and diceRoll >= 100+(difficulty*10)-(level*7):
        #chans för pirog att droppa för lvl 5 6 7 8 9 10 = 25 32 39 46 53 60 (beginner),
        #chans för pirog att droppa för lvl 5 6 7 8 9 10 = 15 22 29 36 43 50 (default),
        #chans för pirog att droppa för lvl 5 6 7 8 9 10 = 5  12 19 26 33 40 (ILTD),
        pirogueDropped = True
        return GRAPHICS['PIROGUE']
    elif diceRoll >= (25*difficulty)+(level*4):
        #chans för potion att droppa för lvl 1 2 3 4 5 6 7 8 9 10 = 71 67 63 59 55 51 47 43 39 35 (beginner),
        #chans för potion att droppa för lvl 1 2 3 4 5 6 7 8 9 10 = 46 42 38 34 30 26 22 18 14 10 (default),
        #chans för potion att droppa för lvl 1 2 3 4 5 6 7 8 9 10 = 21 17 13 9  5  1  0  0  0  0  (ILTD),
        return GRAPHICS['POTION']
    else:
        return GRAPHICS['EMPTY']

#Anropas när spelaren trycker på WASD eller när monster gör sitt drag. Beroende på vad som finns på rutan så händer olika saker,
#t.ex. om rutan är tom förflyttas entiteten dit, om det finns en entitet där slår man den
def entity_action(entity, where):
    global keyDropped,keyFound,pirogueDropped,pirogueEaten
    
    tiles = floor[entities[entity]['room']]['tiles']
    x, y = where #då 'where' är en tupel blir detta en split av tupeln, enligt x, y = (x,y)
    goalTile = floor[entities[entity]['room']]['tiles'][y][x]
    if where == entities[entity]['pos']: #debugrad för att inte få en extra runda när man dött?
        return True
    elif goalTile == GRAPHICS['EMPTY']: #om rutan är tom förflyttas entiteten dit
        move_entity(entity, where)
        return False #returnerar False som assignas till playerTurn för att visa att ett drag har genomförts och att spelarens runda är över
    elif goalTile == GRAPHICS['V_DOOR'] or goalTile == GRAPHICS['H_DOOR']:
        change_room(where)
        return True
    elif where == entities['PLAYER']['pos'] and entities['PLAYER']['life'] > 0:
        attack_entity(entity, 'PLAYER')
        return False
    elif entity == 'PLAYER' and goalTile == GRAPHICS['KEY']:
        keyFound = True
        if entities[entity]['life'] < 2 and difficulty < 3: #om difficulty inte är ILTD så får man liv av nyckeln
            entities[entity]['life'] += 1
            update_entity(entity,entities[entity]['pos'])
        move_entity(entity, where)
        return False
    elif entity == 'PLAYER' and goalTile == GRAPHICS['POTION']:
        if entities[entity]['life'] < 2:
            entities[entity]['life'] += 1
            update_entity(entity,entities[entity]['pos'])
        move_entity(entity, where)
        return False
    elif entity == 'PLAYER' and goalTile == GRAPHICS['PIROGUE']:
        pirogueEaten = True
        move_entity(entity, where)
        return True
    elif goalTile == GRAPHICS['ENEMY_1'] or goalTile == GRAPHICS['ENEMY_2'] or goalTile == GRAPHICS['ENEMY_3']:
        attack_entity('PLAYER', what_entity(entities[entity]['room'], where))
        return False
    elif goalTile == GRAPHICS['NEXT_FLOOR']:
        if entity == 'PLAYER' and keyFound and not pirogueDropped:
            keyFound = False
            keyDropped = False
            move_entity(entity, where)
            next_floor()
            return False
        else:
            return False
    else:
        return False

def attack_entity(attacker,defender):
    global prompt
    rHit = randint(0,100)
    hitbool = False
    if rHit-int(entities[defender]['evasion']) >= 15*difficulty:
        entities[defender]['life'] -= 1
        hitbool = True
    combat_prompt(attacker, defender, hitbool)
    
    if entities[defender]['life'] >0:
        rCounterHit = randint(0,100)
        if rCounterHit-int(entities[attacker]['evasion']) >= 20*difficulty:
            entities[attacker]['life'] -= 1
            prompt += f"{entities[defender]['name']} successfully performs a counter-attack, hitting {entities[attacker]['name']}\n"
    update_entity(attacker, entities[attacker]['pos'])
    update_entity(defender, entities[defender]['pos'])
            
#Anropas när spelarens koordinater 'where' i entity_action är en dörr. Då avgör denna funktion vilket rum spelaren ska förflytta sig till.
#Tar argumentet coords vilket är koordinaterna 'where' som entity_action anropades med
def change_room(coords):
    index = 0
    roomX, roomY = floor[entities['PLAYER']['room']]['coordinates']

    if coords == (MIDDLE, 0): #flytta norrut
        for room in floor:
            if room['coordinates'] == (roomX, roomY+1):
                move_between_rooms(room, (MIDDLE, SIDELENGTH-2))
                
    elif coords == (SIDELENGTH-1, MIDDLE): #flytta öst
        for room in floor:
            if room['coordinates'] == (roomX+1, roomY):
                move_between_rooms(room, (1, MIDDLE))
            
    elif coords == (0, MIDDLE): #flytta väst
        for room in floor:
            if room['coordinates'] == (roomX-1, roomY):
                move_between_rooms(room, (SIDELENGTH-2, MIDDLE))
                
    elif coords == (MIDDLE, SIDELENGTH-1): #flytta söderut
        for room in floor:
            if room['coordinates'] == (roomX, roomY-1):
                move_between_rooms(room, (MIDDLE, 1))
        
#Anropas för att ge spelaren möjlighet att ge inputs för att göra sitt drag. 
def playerTurn():
    render_room(floor[entities['PLAYER']['room']]['tiles'])
    while game_over == False:
        playersTurn = True
        while playersTurn == True:
            if keyboard.is_pressed('w'): # move up
                playersTurn = entity_action('PLAYER',
                                            (entities['PLAYER']['pos'][0], entities['PLAYER']['pos'][1] - 1))
                
            if keyboard.is_pressed('a'): # move left
                playersTurn = entity_action('PLAYER',
                                            (entities['PLAYER']['pos'][0] - 1, entities['PLAYER']['pos'][1]))
                
            if keyboard.is_pressed('s'): # move down
                playersTurn = entity_action('PLAYER',
                                            (entities['PLAYER']['pos'][0], entities['PLAYER']['pos'][1] + 1))
                
            if keyboard.is_pressed('d'):# move right
                playersTurn = entity_action('PLAYER',
                                            (entities['PLAYER']['pos'][0] + 1, entities['PLAYER']['pos'][1]))
                
            if keyboard.is_pressed('e'): #wait
                playersTurn = False
                
            if pirogueEaten or game_over:
                break
            
        enemy_turn()
        render_room(floor[entities['PLAYER']['room']]['tiles']) # andra gången för att visa fiendens drag
        sleep(0.08)
        if game_over or pirogueEaten:
            break
        
    render_room(floor[entities['PLAYER']['room']]['tiles']) # när det blir gameover vill vi rensa prompten
    if not pirogueEaten:
        print("You died. Game over!\n")
    else:
        print("You found the pirogue!\nIt tasted like sweet victory.\n")
    print("Press e to go back to the main menu")
    keyboard.wait('e')

def enemy_turn():
    currentRoom = floor[entities['PLAYER']['room']]
    for e in list(entities)[1:]:
        if entities[e]['room'] == entities['PLAYER']['room'] and entities[e]['life'] > 0:
           entity_action(e, pathfinder(currentRoom['tiles'], e, entities['PLAYER']['pos']))
            

#egengjord pathfinder

#A* är overkill, kan inte avlusa det och eftersom entiteter inte kan röra sig diagonalt eller
#flera steg i taget så är det enklare att programmera en egen pathfinder
def pathfinder(tiles, entity, target):
    eX, eY = entities[entity]['pos']
    targetX, targetY = target
    direction = {'up': (eX, eY-1),
               'left': (eX-1, eY),
               'right': (eX+1, eY),
               'down': (eX, eY+1)}
    directions = []
    if targetX < eX:
        directions.append('left')
    if targetX > eX:
        directions.append('right')
    if targetY < eY:
        directions.append('up')
    if targetY > eY:
        directions.append('down')
        
    shuffle(directions) #Detta gör så att movement ser bättre ut
    for possible_direction in directions:
        pos = direction[possible_direction]
        if pos == target:
            return pos
        elif tiles[pos[1]][pos[0]] == GRAPHICS['EMPTY']:
            return pos
        else:
            rPick = randint(0,1)
            sideStep = (0,0) #för att undvika error om if-satserna under inte skulle gå igenom
            if targetX == eX:
                if rPick:
                    sideStep = direction['left']
                else:
                    sideStep = direction['right']
            if targetY == eY:
                if rPick:
                    sideStep = direction['up']
                else:
                    sideStep = direction['down']
            if tiles[sideStep[1]][sideStep[0]] == GRAPHICS['EMPTY']:
                return sideStep
            else:
                return (eX,eY)
            
            
def combat_prompt(attacker, defender, hitbool):
    global prompt
    if hitbool == False:
        rng = randint(0,2)
        if rng == 0:
            prompt += f"{entities[attacker]['name']} swings at {entities[defender]['name']} but it misses ...\n"
        elif rng == 1:
            prompt += f"{entities[attacker]['name']} attacks {entities[defender]['name']} but fails to do any damage...\n"
        elif rng == 2:
            prompt += f"{entities[attacker]['name']} tries to harm {entities[defender]['name']} but isn't successful...\n"
            
    if hitbool == True:
        rng = randint(0,2)
        if rng == 0:
            prompt += f"{entities[attacker]['name']} successfully hits {entities[defender]['name']} and deals damage!\n"
        elif rng == 1:
            prompt += f"{entities[attacker]['name']} attacks {entities[defender]['name']} and deals damage!\n"
        elif rng == 2:
            prompt += f"{entities[attacker]['name']} strikes {entities[defender]['name']}, successfully harming it!\n"
    
    deaths = []
    if entities[attacker]['life'] <= 0: # Har med detta eftersom någon kan dö av en counterattack
        deaths.append(attacker)
    if entities[defender]['life'] <= 0: # Har med detta eftersom någon kan dö av en counterattack
        deaths.append(defender)
        
    for dead_entity in deaths:
        rng = randint(0,2)
        if rng == 0:
            prompt += f"{entities[dead_entity]['name']} lets out one last sigh before biting the bullet\n"
        if rng == 1:
            prompt += f"{entities[dead_entity]['name']} closes its eyes for the last time and enters the eternal sleep\n"
        if rng == 2:
            prompt += f"{entities[dead_entity]['name']} lies down on the floor never to get up again\n"
        
def animatedSplashScreen():
    for frame in SPLASHFRAMES:
        clear_console()
        print(frame)
        sleep(1)
    print('Press e to start')
    keyboard.wait('e')
    
def clearPrint(menuState):
    clear_console()
    print(MENUFRAMES[menuState])
    
def mainMenu():
    global difficulty
    inMainMenu = True
    inDiffMenu = False
    menuState = 2
    clearPrint(menuState)
    while inMainMenu:
        sleep(0.1)
        if keyboard.is_pressed('w'):
            if menuState > 0:
                menuState -= 1
                clearPrint(menuState)
            else:
                menuState = 2
                clearPrint(menuState)
        if keyboard.is_pressed('s'):
            if menuState < 2:
                menuState += 1
                clearPrint(menuState)
            else:
                menuState = 0
                clearPrint(menuState)
        if keyboard.is_pressed('e'):
            if menuState == 1:
                inDiffMenu = True
                menuState = 2+difficulty
                clearPrint(menuState)
                while inDiffMenu:
                    sleep(0.1)
                    if keyboard.is_pressed('w'):
                        if menuState > 3:
                            menuState -= 1
                            clearPrint(menuState)
                        else:
                            menuState = 5
                            clearPrint(menuState)
                    if keyboard.is_pressed('s'):
                        if menuState < 5:
                            menuState += 1
                            clearPrint(menuState)
                        else:
                            menuState = 3
                            clearPrint(menuState)
                    if keyboard.is_pressed('e'):
                        if menuState == 3:   #Beginner
                            difficulty = 1
                        elif menuState == 4: #Default
                            difficulty = 2
                        else:                #I Like To Die
                            difficulty = 3
                        menuState = 1
                        inDiffMenu = False
                        clearPrint(menuState)
            elif menuState == 2:
                inHelp = True
                menuState = 6
                clearPrint(menuState)
                while inHelp:
                    sleep(0.1)
                    if keyboard.is_pressed('d'):
                        if menuState < 8:
                            menuState += 1
                            clearPrint(menuState)
                        else:
                            menuState = 6
                            clearPrint(menuState)
                            
                    if keyboard.is_pressed('a'):
                        if menuState > 6:
                            menuState -= 1
                            clearPrint(menuState)
                        else:
                            menuState = 8
                            clearPrint(menuState)
                            
                    if keyboard.is_pressed('e'):
                        menuState = 1
                        inHelp = False
                        clearPrint(menuState)
            else:
                inMainMenu = False
                
def main():
    while 1:
        initGlobalVariables()
        animatedSplashScreen()
        mainMenu()
        entities['PLAYER']['evasion']= 20*(4-difficulty)
        next_floor()     
main()
