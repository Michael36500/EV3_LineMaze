#!/usr/bin/env pybricks-micropython
import pybricks.tools as pt
from pybricks.ev3devices import ColorSensor, Motor, TouchSensor  # type: ignore
from pybricks.hubs import EV3Brick
from pybricks.parameters import Color, Direction, Port
from pybricks.robotics import DriveBase

ev3 = EV3Brick()    

m_l = Motor(Port.C, positive_direction=Direction.COUNTERCLOCKWISE, gears=[12,20])
m_r = Motor(Port.D, positive_direction=Direction.COUNTERCLOCKWISE, gears=[12,20])

cl1 = ColorSensor(Port.S1)
cl2 = ColorSensor(Port.S2)
cl3 = ColorSensor(Port.S3)

navig = ColorSensor(Port.S4)

robot = DriveBase(m_l, m_r, 57, 226)

# robot.settings(256, 1024, 128, 512)
# robot.settings(256, 1024, 128, 512)

def line():
    global targ
    global p
    global base_speed
    global navi

    navi = navig.reflection()
    error = navi - targ
    turn = p * error

    robot.drive(base_speed, turn)  # type: ignore

def make_Uturn():
    # for x in range (3):
    robot.turn(182)
    # robot.straight(20)

def make_right():
    ## vylaď
    robot.straight(20)
    robot.turn(92)

def make_left():
    ## vylaď
    robot.straight(20)
    robot.turn(-92)

def make_strght():
    # for skipping crossing
    # robot.straight(30)
    pass

def rd_fwd():
    global lft_fwd
    global rgh_fwd
    global mid_fwd
    ## vylaď
    robot.straight(30)

    lft_fwd = cl1.reflection()
    mid_fwd = cl2.reflection()
    rgh_fwd = cl3.reflection()

def bila(inp):
    global thresh_up
    global thresh_dwn

    if inp > thresh_up: return True
    elif inp < thresh_dwn: return False
    else: return None

def rd_all():
    global lft
    global rgh
    global mid

    lft = cl1.reflection()
    mid = cl2.reflection()
    rgh = cl3.reflection()

def pebug():
    global lft, rgh, mid
    global navi    
    global lft_fwd, rgh_fwd, mid_fwd
    global pozice, wturn

    print(bila(lft_fwd), bila(mid_fwd), bila(rgh_fwd), lft_fwd, mid_fwd, rgh_fwd)
    print(bila(lft), bila(mid), bila(rgh), lft, mid, rgh)
    print(navi)
    print(memory)
    print(pozice, "pozice", wturn, "wturn")
    print()


def make_decision(kriz):
    global pozice, wturn
    global memory

    moznosti = {"U": ["U"], "L":["L"], "R":["R"], "J":["S", "L"], "K":["S","R"], "T":["R","L"], "+":["R","L","S"]}
    # kompletní update políčka
    if kriz == "R":
        memory[pozice[0]][pozice[1]].




    




def check():
    global lft
    global rgh
    global mid
    
    global lft_fwd
    global rgh_fwd
    global mid_fwd
    global navi

    global somenum
    rd_all()

    mid = cl2.reflection()

    somenum += 1
    krizovatka = None

    if somenum % 100 == 0:
        pebug()

    if bila(lft) == False and bila(mid) == False and bila(rgh) == True:
        rd_fwd()
        somenum = 0
        if bila(lft_fwd) == True and bila(mid_fwd) == True and bila(rgh_fwd) == True:
            krizovatka = "L"
        elif bila(lft_fwd) == True and bila(mid_fwd) == False and bila(rgh_fwd) == True:
            krizovatka = "J"
        else:
            print("FUCK FFT!!!")

          

    elif bila(lft) == True and bila(mid) == False and bila(rgh) == False:
        rd_fwd()
        somenum = 0
        if bila(lft_fwd) == True and bila(mid_fwd) == True and bila(rgh_fwd) == True:
            krizovatka = "R"
        elif bila(lft_fwd) == True and bila(mid_fwd) == False and bila(rgh_fwd) == True:
            krizovatka = "K"
        else:
            print("FUCK TFF!!!")

    elif bila(lft) == False and bila(mid) == False and bila(rgh) == False:
        rd_fwd()
        somenum = 0
        if bila(lft_fwd) == True and bila(mid_fwd) == True and bila(rgh_fwd) == True:
            krizovatka = "T"
        elif bila(lft_fwd) == True and bila(mid_fwd) == False and bila(rgh_fwd) == True:
            krizovatka = "+"
        elif bila(lft_fwd) == False and bila(mid_fwd) == False and bila(rgh_fwd) == False:
            print("FINISH")
            return "out"

    elif bila(lft) == True and bila(mid) == True and bila(rgh) == True:
        rd_fwd()
        if bila(lft_fwd) == True and bila(mid_fwd) == True and bila(rgh_fwd) == True:
            krizovatka = "U"
        else:
            print("FUCK TTT!!!")
            # make_strght()
    elif bila(lft) == True and bila(mid) == False and bila(rgh) == True:
        rd_all()
        updt_kola()
        # sledování čáry
        pass
    else:
        print("NĚCO JE TOTÁLNĚ ŠPATNĚ")


    if krizovatka != None:
        make_decision(krizovatka)
    


def updt_kola():
    global pozice, wturn

    posun = round(robot.distance() / 150, 0)
    otoceni = (round(robot.angle() / 90, 0) + wturn) % 4
    wturn = otoceni

    if otoceni == 0:
        pozice[1] -= posun  # type: ignore
    elif otoceni == 1:
        pozice[0] += posun  # type: ignore
    elif otoceni == 2:
        pozice[1] += posun  # type: ignore
    elif otoceni == 3:
        pozice[0] -= posun  # type: ignore
    else:
        print("MOTHERFUCKER!!!!")


    print(posun, "posun")
    print(otoceni, "otoceni")

    robot.reset()

class policko():
    # None - nevíme, -1 - cesta není, 0 cesta je, neprošli, 1 - c je, jednou p, 2 - cesta je, prošli 2 krát
    def __init__(self):
        self.nahoru = None
        self.doprava = None
        self.doleva = None
        self.dolu = None

    def gnahoru(self):
        return self.nahoru
    def gdoprava(self):
        return self.doprava
    def gdoleva(self):
        return self.doleva
    def gdolu(self):
        return self.dolu
    
    def update_by_list(self, lst, posun):
        for x in range(4):
            y = (x + posun) % 4
            if y == 0:
                # self.nnahoru()


    def nnahoru(self, x):
        self.nahoru = x
    def ndoprava(self, x):
        self.doprava = x
    def ndolu(self, x):
        self.dolu = x
    def ndoleva(self, x):
        self.doleva = x



pozice = [25, 25]
wturn = 0


planek = []
for _ in range(50):
    temp = []
    for _ in range(50):
        tmp = []
        for _ in range(4):
            tmp.append(policko())
        temp.append(tmp)
    planek.append(temp)


cis = 0
najeto_na_kolech = []
najeto_na_kolech2 = []

p = 2.5
base_speed = 75

thresh_up = 26
thresh_dwn =  16
targ = 12

memory = []
somenum = 0
navi = navig.reflection()

# precise position
ev3.light.off()
while navi != targ:
    navi = navig.reflection()
ev3.light.on(Color.GREEN)
pt.wait(500)



rd_all()
rd_fwd()

while True:
    rd_all()
    line()
    if check() == "out":
        break




strung = ""

for x in memory:
    strung += x

print(strung)

strung_start = None


while strung_start != strung:
    strung_start = strung
    strung = strung.replace("LUL", "S")
    strung = strung.replace("LUS", "R")
    strung = strung.replace("SUL", "R")
    strung = strung.replace("RUL", "U")
    strung = strung.replace("SUS", "U")
    strung = strung.replace("UU", "")

print(strung)
