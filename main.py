ROOMSIZE = 21 # (x,y)

H_WALL = "═" # Basic tile-grafik inläst som konstanter
V_WALL = "║"
TL_CORNER = "╔"
TR_CORNER = "╗"
BL_CORNER = "╚"
BR_CORNER = "╝"
EMPTY = " "

T_DOOR  = BR_CORNER+EMPTY+BL_CORNER
B_DOOR  = TR_CORNER+EMPTY+TL_CORNER
TB_NODOOR = H_WALL*3

def generate_room(doors):
    room = []
    for vertLine in range(ROOMSIZE):
        horizLine = []
        if vertLine == 0:
            horizLine+=TL_CORNER
            horizLine+=H_WALL*int(((ROOMSIZE-1)/2)-2)
            if doors['T']:
                horizLine+=T_DOOR
            else:
                horizLine+=TB_NODOOR
            horizLine+=H_WALL*int(((ROOMSIZE-1)/2)-2)
            horizLine+=TR_CORNER
        elif vertLine == ROOMSIZE-1:
            horizLine+=BL_CORNER
            horizLine+=H_WALL*int(((ROOMSIZE-1)/2)-2)
            if doors['B']:
                horizLine+=B_DOOR
            else:
                horizLine+=TB_NODOOR
            horizLine+=H_WALL*int(((ROOMSIZE-1)/2)-2)
            horizLine+=BR_CORNER
        elif vertLine == int(((ROOMSIZE-1)/2)-2):
            if doors['L']:
                horizLine+=BR_CORNER
            else:
                horizLine+=V_WALL
            horizLine+=EMPTY*(ROOMSIZE-2)
            if doors['R']:
                horizLine+=BL_CORNER
            else:
                horizLine+=V_WALL
        elif vertLine == int(((ROOMSIZE-1)/2)-1):
            if doors['L']:
                horizLine+=EMPTY
            else:
                horizLine+=V_WALL
            horizLine+=EMPTY*(ROOMSIZE-2)
            if doors['R']:
                horizLine+=EMPTY
            else:
                horizLine+=V_WALL
        elif vertLine == int(((ROOMSIZE-1)/2)):
            if doors['L']:
                horizLine+=TR_CORNER
            else:
                horizLine+=V_WALL
            horizLine+=EMPTY*(ROOMSIZE-2)
            if doors['R']:
                horizLine+=TL_CORNER
            else:
                horizLine+=V_WALL
        else:
            horizLine+=V_WALL
            horizLine+=EMPTY*(ROOMSIZE-2)
            horizLine+=V_WALL
        room.append(horizLine)
    return room

doors = {"T":False,"L":True,"R":False,"B":True}

test_room = generate_room(doors)
for hLine in test_room:
    currLine = ""
    for tile in hLine:
        currLine += tile
    print(f"{currLine}")
print("Hello World")