ROOMSIZE = (21,21) # (x,y)

H_WALL = "═" # Basic grafik inläst som konstanter
V_WALL = "║"
TL_CORNER = "╔"
TR_CORNER = "╗"
BL_CORNER = "╚"
BR_CORNER = "╝"

T_DOOR = BR_CORNER+" "+BL_CORNER
B_DOOR = TR_CORNER+" "+TL_CORNER
L_DOOR = BR_CORNER+"\n"+TR_CORNER
R_DOOR = BL_CORNER+"\n"+TL_CORNER

TB_NODOOR = H_WALL*3
LR_NODOOR = V_WALL*3

def generate_room(doors):
    room = []
    for vertLine in range(ROOMSIZE[1]):
        horizLine = []
        if vertLine == 0:
            horizLine.append(TL_CORNER)
            horizLine.append(H_WALL*int(((ROOMSIZE[0]-3)/2)-1))
            if doors['T']:
                horizLine.append(T_DOOR)
            else:
                horizLine.append(TB_NODOOR)
            horizLine.append(H_WALL*int(((ROOMSIZE[0]-3)/2)-1))
            horizLine.append(TR_CORNER)
        if vertLine == ROOMSIZE[1]-1:
            horizLine.append(BL_CORNER)
            horizLine.append(H_WALL*int(((ROOMSIZE[0]-3)/2)-1))
            if doors['B']:
                horizLine.append(B_DOOR)
            else:
                horizLine.append(TB_NODOOR)
            horizLine.append(H_WALL*int(((ROOMSIZE[0]-3)/2)-1))
            horizLine.append(BR_CORNER)
        room.append(horizLine)
    return room
doors = {"T":True,"L":True,"R":False,"B":False}

test = generate_room(doors)