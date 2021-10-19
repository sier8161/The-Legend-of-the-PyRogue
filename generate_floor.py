from random import randint
import keyboard
import os
from time import sleep
<<<<<<< Updated upstream

=======
>>>>>>> Stashed changes
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
            'H_DOOR': '─',
            'V_DOOR': '│',
            'EMPTY':' ',
            'NEXT_FLOOR':'x',
            'ENEMY_1':'1',
            'ENEMY_2':'2',
            'ENEMY_3':'3',
            'ENEMY_SLEEPING':'Z',
            'SHIELD':'H',
            'PIROGUE':'B'}

combatPromptAttack = ""
combatPromptCounter = ""
floor = []
level = 1
<<<<<<< Updated upstream
entities = {'PLAYER': {'pos':(MIDDLE, MIDDLE),
                      'room':0,  #OBS! Nyckel 'room' som en entitet har är ett index för listan floor där indexet motsvarar ett dictionary som är rummet i fråga
                      'life':2, #2: sköld, 1: ingen sköld, 0:död
                      'evasion': 1
                       'name': 'Player' #Implementera ett sätt för spelaren att få använda sitt namn?
=======
combatPromptAttack = ""
combatPromptCounter = ""
entities = {'PLAYER': {'pos':(MIDDLE, MIDDLE),
                      'room':0,  #OBS! Nyckel 'room' som en entitet har är ett index för listan floor där indexet motsvarar ett dictionary som är rummet i fråga
                      'life':2, #2: sköld, 1: ingen sköld, 0:död
                      'evasion': 1,
                      'name': 'Player'
>>>>>>> Stashed changes
                       }
            #lägg till monster här
            }

monsterCount = 0 #
# generate_monster är en procedur som ändrar den globala dictionaryn entities för att lägga till ett monster.
# Parametrar in till denna funktion; diff:integer med svårighetsgrad på monstret, room: integer för index på
# rummet i floor-listan som den skall genereras i, och coords: tupel med integers för x och y-värden.
# sidoeffekter: ändrar den globala dictionaryn entities för att lägga till ett monster, och ändrar globala variabeln monsterCount
def generate_monster(diff,where,room): #OBS! Nyckel 'room' som entities har är ett index för listan floor där indexet motsvarar ett dictionary som är ett rum
    global monsterCount
    monsterCount += 1 #iom att vi ökar monstercount innan monstret skapas så kommer första monstret få 'entiteten' MONSTER_1
    life = 0
    evasion = 0
    for _ in range(diff):
        life += 1 #temporära värden
        evasion += 2 #ändra dessa sedan när vi har funderat ut hur vi vill göra med liv och evasion
    entities[f'MONSTER_{str(monsterCount)}'] = {'pos':where,
                                                'room':room,
                                                'life':life,
                                                'evasion':evasion,
                                                'name': 'Monster'
                                                }
    place_entity(f'MONSTER_{str(monsterCount)}', entities[f'MONSTER_{str(monsterCount)}']['pos'])

#procedur som anropar generate_monster flertalet gånger för att skapa en mängd 'quantity' monster på slumpmässiga platser med slumpmässiga stats.
#OBS! EJ KLAR då den skall vikta antal fiender mot svårighetsgrad osv för att balansera spelet, vi får titta på det senare.
def generate_monsters(quantity):
    for _ in range(quantity):
        rDiff = randint(1, 3)
        rX = randint(2, SIDELENGTH-3)
        rY = randint(2, SIDELENGTH-3)
        rRoom = randint(0,(len(floor)-1))
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
def needed_doors(room, possibilities):
    roomCoords = room['coordinates']
    x = roomCoords[0]
    y = roomCoords[1]
    for coords in possible_placements(roomCoords):
        if coords in possibilities:
            print()
        elif coords == (x-1,y):
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
    global combatPromptAttack
    global combatPromptCounter
    clear_console()
    for vertLine in tiles:
        for tile in vertLine:
            print(tile, end="")
        print("\n", end="")
<<<<<<< Updated upstream
    print(floor[entities['PLAYER']['room']]['coordinates'])
=======
    print(combatPromptAttack)
    print(combatPromptCounter)
    print(str(floor[entities['PLAYER']['room']]['coordinates'])+" room n: "+str(entities['PLAYER']['room']))
    combatPromptAttack = ""
    combatPromptCounter = ""
>>>>>>> Stashed changes
        
#returnerar en lista av tuples där varje tuple är koordinater som ligger brevid ett bestämt rum
def possible_placements(roomCoords):
    x = roomCoords[0]
    y = roomCoords[1]
    listy = [((x+1), y), ((x-1), y), (x, (y-1)), (x, (y+1))]
    return listy    
    
#Skapar en lista (globalt) som representerar en floor datamässigt.
def generate_floor():
    #skapar första rummet vid 0,0
    global floor
    floor = [generate_room((0,0))]
    existingRoomCoords= [(0,0)]
    possibilities = possible_placements((0,0)) #lista som lagrar alla möjliga koordinater där nästa rum kan placeras 
    nRooms = 2**(level-1) + 5 #Antalet rum bestäms av parametern level
    for _ in range(nRooms):
        rng = randint(0, len(possibilities)-1)
        newRoomCoords = possibilities[rng]
        print(f"Rum {_+2} koordinater: ", newRoomCoords) #rad för debug
        floor.append(generate_room(newRoomCoords, ))
        for coords in possible_placements(newRoomCoords):
            if not coords in possibilities:
                    if not coords in existingRoomCoords:
                        possibilities.append(coords)
        existingRoomCoords.append(possibilities.pop(possibilities.index(newRoomCoords)))
    for room in floor:
        needed_doors(room, possibilities)
        create_doors(room)
    entities['PLAYER']['room'] = randint(0, nRooms) #slumpar vilket rum spelaren börjar i

    place_entity('PLAYER', entities['PLAYER']['pos'])

#Här under finns en del funktioner som interagerar med tiles i rum

#Funktion som placerar en entitet vid bestämda koordinater. Argumentet entity är vilken entitet och where är koordinaterna i (x,y) form
def place_entity(entity, where):
    tiles = floor[entities[entity]['room']]['tiles']
    
    if entity == 'PLAYER':
        graphics = GRAPHICS[entity]
    else:
        diff = entities[entity]['life']
        graphics = GRAPHICS[f'ENEMY_{diff}']
        
    x, y = where #då 'where' är en tupel blir detta en split av tupeln, enligt x, y = (x,y)
    yaxis = tiles[y]
    yaxis[x] = graphics
    

#Tar bort en entitet. Tar entity som argument vilket är den entitet som ska tas bort
def delete_entity(entity):
    tiles = floor[entities[entity]['room']]['tiles']
    coords = entities[entity]['pos']
    x, y = coords #då 'coords' är en tupel blir detta en split av tupeln, enligt x, y = (x,y)
    yaxis = tiles[y]
    yaxis[x] = GRAPHICS['EMPTY']

#Flyttar en entitet till bestämda koordinater. Tar argumenten entity vilket är vilken entitet och where som är koordinaterna för vart den ska flyttas
def move_entity(entity, where):
    tiles = floor[entities[entity]['room']]['tiles'] #OBS! tog player som key till entities för att jag inte förväntar mig att någon ska använda funktionen i ett annat rum och ville göra det enkelt
    delete_entity(entity)
    place_entity(entity, where)
    entities[entity]['pos'] = where

#returnerar vad för entitet som befinner sig på en bestömd ruta. Tar argumenten room som är rummet som man vill leta efter en entitet i
#och where som är vilka koordinater i tiles där man vill veta vilken entitet som befinner sig där
def what_entity(room, where):
    for e in entities:
        if entities[e]['room'] == room:
            if entities[e]['pos'] == where:
                return entities[e]
  
#Returnerar koordinaterna för en (1) entitet av en viss typ i ett rum 
def where_entity(room,entity):
    if entity in entities:
        if entities[entity]['room'] == room:
            return entities[entity]['pos']
            
#Förflyttar spelaren från ett rum till ett annat. Tar argumenten room som är det rum man önskar att flytta till och where som är de koordinater man önskar att flytta till i det nya rummet
def move_between_rooms(room, where):
    delete_entity('PLAYER')
    entities['PLAYER']['room'] = floor.index(room)
    place_entity('PLAYER', where)
    entities['PLAYER']['pos'] = where

#Anropas när spelaren trycker på WASD eller när monster gör sitt drag. Beroende på vad som finns på rutan så händer olika saker,
#t.ex. om rutan är tom förflyttas entiteten dit, om det finns en entitet där slår man den
def entity_action(entity, where): 
    tiles = floor[entities[entity]['room']]['tiles']
    x, y = where #då 'where' är en tupel blir detta en split av tupeln, enligt x, y = (x,y)
    goalTile = floor[entities[entity]['room']]['tiles'][y][x]
    if goalTile == GRAPHICS['EMPTY']: #om rutan är tom förflyttas entiteten dit
        move_entity(entity, where)
        return False #returnerar False som assignas till playerTurn för att visa att ett drag har genomförts och att spelarens runda är över
    elif goalTile == GRAPHICS['V_DOOR'] or goalTile == GRAPHICS['H_DOOR']:
        change_room(where)
        return False
    elif where == entities['PLAYER']['pos'] and not entity == 'PLAYER':
        attack_entity(entities[entity], entities['PLAYER']) #OBS! OBS! OBS! Anropar en icke-existerande funktion som jag tänker göra senare, attack_entity(attacker, target)
        return False
    elif goalTile == GRAPHICS['ENEMY_1'] or goalTile == GRAPHICS['ENEMY_2'] or goalTile == GRAPHICS['ENEMY_3']:
        attack_entity(entities['PLAYER'], what_entity(entities[entity]['room'], where))
        return False
    else:
        return True

def attack_entity(attacker,defender):
    global combatPromptAttack
    global combatPromptCounter
    rHit = randint(0,10)
<<<<<<< Updated upstream
    if int(rHit-defender['evasion']) >= 5:
        defender['life'] -= 1
        combatPromptAttack = f"{attacker['name']} attack and hit {defender['name']}"
    elif int(rHit-defender['evasion']) < 5:
        combatPromptAttack = ""
    
    if defender['life'] >0:
        rCounterHit = randint(0,9)
        if int(rCounterHit-attacker['evasion']) >= 5:
            attacker['life'] -= 1
=======
    hitormiss = "misses"
    if rHit-int(entities[defender]['evasion']) >= 5:
        entities[defender]['life'] -= 1
        hitormiss = "damages"
    combatPromptAttack = f"{entities[attacker]['name']} attacks and {hitormiss} {entities[defender]['name']}"
    
    if entities[defender]['life'] >0:
        rCounterHit = randint(0,9)
        if rCounterHit-int(entities[attacker]['evasion']) >= 5:
            entities[attacker]['life'] -= 1
            combatPromptCounter = f"{entities[defender]['name']} successfully performs a counter-attack, damaging {entities[attacker]['name']}"
    update_entity(attacker, entities[attacker]['pos'])
    update_entity(defender, entities[defender]['pos'])
            
>>>>>>> Stashed changes

#Anropas när spelarens koordinater 'where' i entity_action är en dörr. Då avgör denna funktion vilket rum spelaren ska förflytta sig till.
#Tar argumentet coords vilket är koordinaterna 'where' som entity_action anropades med
def change_room(coords):
    index = 0
    roomCoords = floor[entities['PLAYER']['room']]['coordinates']
    roomX = roomCoords[0]
    roomY = roomCoords[1]
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
                
    else:
        print("The door is broken!")
    
        
        
#Anropas för att ge spelaren möjlighet att ge inputs för att göra sitt drag. 
def playerTurn():
    render_room(floor[entities['PLAYER']['room']]['tiles'])
    while True:
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
                pass
                playersTurn = False
        
        render_room(floor[entities['PLAYER']['room']]['tiles'])
        combatPromptAttack = ""
        combatPromptCounter = ""
        sleep(0.1)
<<<<<<< Updated upstream
=======

>>>>>>> Stashed changes

#Testfunktioner
def testing_create_doors(door):
    testroom = generate_room((0,0))
    render_room(testroom)
    testroom['doors'][door] = True
    create_doors(testroom)
    render_room(testroom)
    
def testing_movement():
    generate_floor()
    generate_monsters(10)
    playerTurn()
    
testing_movement()