#Testfunktioner
def testing_create_doors(door):
    testroom = generate_room((0,0))
    render_room(testroom)
    testroom['doors'][door] = True
    create_doors(testroom)
    render_room(testroom)
    
def testing_movement():
    generate_floor()
    generate_monsters()
    playerTurn()

#Testar hur många matcher som vinns under de bästa förhållanden för spelarna, dvs hen hittar det monster med minst liv, dödar den och tar sig till nästa nivå omdelebart tills hen är död eller hittat pirogen.
def testing_difficulty():
    global level
    global floor
    global difficulty
    global pirogueDropped
    #global keyDropped
    wins = 0
    losses = 0
    totalGames = input("How many games do you want to emulate?")
    difficulty = int(input("What difficulty? (1-3)"))
    for _ in range(int(totalGames)):
        print(f"Game {_}")
        level = 0
        floor = []
        gameOver = False
        entities['PLAYER']['life'] = 2
        pirogueDropped = False
        keyDropped = False
        while entities['PLAYER']['life'] > 0 or gameOver == False:
            if entities['PLAYER']['life'] == 1 and difficulty != 3:
                entities['PLAYER']['life'] = 2
            level += 1
            generate_floor()
            generate_monsters()
            keyDropped = False
            print(f"Floor: {level}")
          
            
            while keyDropped == False:
                monster = ""
                monsterFound = False
                i = 0
                while monsterFound == False:
                    for e in entities:
                        print(e)
                        if entities[e]['life'] == 1+i and e != 'PLAYER':
                            monster = e
                    if monster != "":
                        monsterFound = True
                        print(f"Battle against {e}")
                    else:
                        i +=1
                    
                
                    
                while entities[monster]['life'] > 0 and entities['PLAYER']['life'] > 0:
                    if entities['PLAYER']['life'] > 0:
                        attack_entity('PLAYER', monster)
                    if entities[monster]['life'] > 0:
                        attack_entity(monster, 'PLAYER')
                print("Battle is over!")
                    
                if entities['PLAYER']['life'] == 0:
                    print("player died")
                    gameOver = True
                    losses +=1
                    keyDropped = True #nyckeln har inte droppat men behöver bryta loopen
                
                elif pirogueDropped == True:
                    print("player won")
                    wins += 1
                    gameOver = True
                    keyDropped = True
                    
                
                 
                elif keyDropped == True:
                    print("Key dropped!")
                
                
                
    print(f"Total games: {totalGames}")
    print(f"Wins: {wins}")
    print(f"Losses: {losses}")
    savedata = open("difficulty_test_data.txt", 'a')
    savedata.write(f"Total games: {totalGames}, Difficulty: {difficulty}, Wins: {wins}, Losses: {losses}\n")
    savedata.close