#@author : Rafsan Ratul (ratulrafsan@gmail.com)
#An attempt to make a simple rouguelike game in python without using any external library
import random
import keyboard

          # 0   1   2   3   4   5   6   7   8   9  10   11  12  13  14  15
room = {1:['#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#'], # ^
        2:['#','.','.','.','.','.','.','.','.','.','.','.','.','.','.','#'], # |
        3:['#','.','.','.','.','.','.','.','.','#','#','#','#','.','.','#'], # |
        4:['#','.','.','.','.','.','.','#','.','#','.','.','.','.','.','#'], # |
        5:['#','.','.','.','.','.','@','#','.','#','.','.','#','.','.','#'], # |
        6:['#','.','.','.','.','.','.','#','.','.','.','.','#','.','.','#'], # x
        7:['#','.','.','.','.','#','#','#','.','#','#','.','#','.','.','#'], # |
        8:['#','.','.','.','.','.','.','.','.','.','#','#','#','.','.','#'], # |
        9:['#','.','.','.','.','.','.','.','.','.','.','.','.','.','.','#'], # |
       10:['#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#']} # |
        # <------------------------------y--------------------------------->

stuff  = {'wall'  :  "#",
          'player':  "@",
          'empty' :  ".",
          'money' :  "$",
          'chest' :  "C"}
#potion = ['hp','xp','dmg']
#weapon = ['sword','nuclear bomb','TNT']

pos = [] # 0 is X,1 is Y


def gamemap():
    for i in range(1,len(room)+1):
        print ("".join(room[i]))

def player_pos():
    for i in range(1,len(room)+1):
        if stuff['player'] in room[i]:
            x_axis = i
            y_axis = room[i].index(stuff['player'])
            global pos
            del pos[:]
            pos.append(x_axis)
            pos.append(y_axis)

def updater():
    gamemap()
    player_pos()


def up(ditcioary,inst_replace,inst_player):
    (ditcioary[pos[0]]).pop(pos[1])
    (ditcioary[pos[0]]).insert(pos[1],inst_replace)
    (ditcioary[pos[0]-1]).pop(pos[1])
    (ditcioary[pos[0]-1]).insert(pos[1],inst_player)


def down(ditcioary,inst_replace,inst_player):
    (ditcioary[pos[0]]).pop(pos[1])
    (ditcioary[pos[0]]).insert(pos[1],inst_replace)
    (ditcioary[pos[0]+1]).pop(pos[1])
    (ditcioary[pos[0]+1]).insert(pos[1],inst_player)


def left(ditcioary,inst_replace,inst_player):
    (ditcioary[pos[0]]).pop(pos[1])
    (ditcioary[pos[0]]).insert(pos[1],inst_replace)
    (ditcioary[pos[0]]).pop(pos[1]-1)
    (ditcioary[pos[0]]).insert(pos[1]-1,inst_player)


def right(ditcioary,inst_replace,inst_player):
    (ditcioary[pos[0]]).pop(pos[1])
    (ditcioary[pos[0]]).insert(pos[1],inst_replace)
    (ditcioary[pos[0]]).pop(pos[1]+1)
    (ditcioary[pos[0]]).insert(pos[1]+1,inst_player)



updater()

while True:
    keyPressed = False
    if keyboard.is_pressed('w') and keyPressed == False:
        keyPressed = True
        if room[pos[0]-1][pos[1]] is not stuff['wall']:
            up(room, stuff['empty'], stuff['player'])
            updater()
            print (pos)
        else:
            print ("Bump! Wall : up")
    elif keyboard.is_pressed('s') and keyPressed == False:
        keyPressed = True
        if room[pos[0]+1][pos[1]] is not stuff['wall']:
            down(room,stuff['empty'],stuff['player'])
            updater()
            print (pos)
        else:
            print ("Bump! wall : down")
    elif keyboard.is_pressed('a') and keyPressed == False:
        keyPressed = True
        if room[pos[0]][pos[1]-1] is not stuff['wall']:
            left(room,stuff['empty'], stuff['player'])
            updater()
            print (pos)
        else:
            print("Bump! wall : left")
    elif keyboard.is_pressed('d') and keyPressed == False:
        keyPressed = True
        if room[pos[0]][pos[1]+1] is not stuff['wall']:
            right(room,stuff['empty'], stuff['player'])
            updater()
            print (pos)
        else:
            print("Bump! wall : right")
