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
    # robot.straight(20)
    print("Uturn")
    robot.turn(182)
def make_right():
    ## vylaď
    print("right")
    robot.straight(20)
    robot.turn(92)
def make_left():
    ## vylaď
    print("left")
    robot.straight(20)
    robot.turn(-92)
def make_strght():
    print("strght")
    # for skipping crossing
    robot.straight(30)

def rd_fwd():
    global lft_fwd
    global rgh_fwd
    global mid_fwd
    print("rd fwd")
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
    if True:
        print(bila(lft_fwd), bila(mid_fwd), bila(rgh_fwd), lft_fwd, mid_fwd, rgh_fwd)
        print(bila(lft), bila(mid), bila(rgh), lft, mid, rgh)
        print(navi)
        print(memory)
        print(pozice, "pozice", wturn, "wturn")
        print()
def make_decision(kriz):
    global pozice, wturn
    global planek
    global debug

    if kriz == "▫":
        updt_kola()
        print("našel jsem uturn")
        policsto = planek[int(pozice[0])][int(pozice[1])]
        if policsto.je_prazdny():
            policsto.nastav_podle_krizovatky(kriz)
        policsto.prijezd(wturn)
        
        make_Uturn()
        updt_kola()
        policsto.odjezd(wturn)
        # wturn = (wturn + 2) % 4 # opačný směr

    elif kriz == "■":
        print("finish")
        exit()
    else:
        # když jsem tam nebyl, tak si vložit políčko do planek
        updt_kola() 
        policsto = planek[int(pozice[0])][int(pozice[1])]
        if policsto.je_prazdny():
            policsto.nastav_podle_krizovatky(kriz)

        # zapsat směr příjezdu (odkud jsem přijel)
        policsto.prijezd(wturn)

        # vyhodnotím směr odjezdu
            # zjistím kam
        # strang = ""
        # for x in planek:
        #     for y in x:
        #         strang += y.print_all()
        #         strang += " "
        #     strang += "\n"
        # print(strang)
        # for x in planek:
        #     for y in x:
        #         print(y.print_all(), end="")
        #     print()
            # updt wturn
        print()
        
        x = policsto.get_smer()
        print(x)
        # x = int(input())
        # # print(y)
        # if y != "d":
        #     x = y

        rozdil = ((x - wturn) + 4) % 4
        print(rozdil, "rozdil")
        if rozdil == 0:
            make_strght()
        elif rozdil == 1:
            make_right()
        elif rozdil == 2:
            make_Uturn()
        elif rozdil == 3:
            make_left()
        else:
            print("užij si debugování")


        updt_kola()
        # zapsat směr odjezdu
        policsto.odjezd(wturn)

        # další křižovatka (neboli vyskočím do checku a pokračuji)
def na_jake_kriz(pole, smer):
    boss_dict = {
    "TFT TFF" : ["├", "┬", "┤", "┴"],
    "TTT TFF" : ["┌", "┐", "┘", "└"],
    "TTT TTT" : ["▫", "▫", "▫", "▫"],
    "TTT FFF" : ["┬", "┤", "┴", "├"],
    "FFF FFF" : ["■", "■", "■", "■"],
    "TFT FFF" : ["┼", "┼", "┼", "┼"],
    "TFT FFT" : ["┤", "┴", "├", "┬"],
    "TTT FFT" : ["┐", "┘", "└", "┌"]
    }
    
    strung = ""
    for x in pole:
        for y in x:
            if y == True: strung += "T"
            if y == None: strung += "F"
            if y ==False: strung += "F"
        strung += " "
    strung = strung[: -1]
    print(strung)
    
    print(pole,smer)
    # for x in strung:
    #     print(x, end=".")
    return boss_dict[strung][int(smer)]


def check():
    global lft, rgh, mid
    global lft_fwd, rgh_fwd, mid_fwd, navi
    global somenum
    global pozice, wturn


    somenum += 1

    if somenum % 100 == 0:
        pebug()
    if not(bila(lft) != False and bila(mid) != True and bila(rgh) != False):
        robot.stop()
        rd_all()
        rd_fwd()
        pebug()
        pole = [
            [bila(lft_fwd), bila(mid_fwd), bila(rgh_fwd)],
            [bila(lft), bila(mid), bila(rgh)]]
        # for x in pole:
        #     for y in pole:
        #         if 

        kriz = na_jake_kriz(pole, wturn)
        make_decision(kriz)



def updt_kola():
    global pozice, wturn

    posun = round(robot.distance() / 150, 0)
    otoceni = (round(robot.angle() / 90, 0) + wturn) % 4
    robot.reset()
    wturn = otoceni

    if otoceni == 0:
        pozice[0] -= posun  # type: ignore
    elif otoceni == 1:
        pozice[1] += posun  # type: ignore
    elif otoceni == 2:
        pozice[0] += posun  # type: ignore
    elif otoceni == 3:
        pozice[1] -= posun  # type: ignore
    else:
        print("MOTHERFUCKER!!!!")

    print(posun, "posun")
    print(otoceni, "otoceni")
    print(wturn, "wturn")

class policko():
    # None - nevíme, -1 - cesta není, 0 cesta je, neprošli, 1 - c je, jednou p, 2 - cesta je, prošli 2 krát
    def __init__(self):
        self.nahoru = None
        self.doprava = None
        self.doleva = None
        self.dolu = None

    def je_prazdny(self):
        if self.nahoru == None and self.doprava == None and self.dolu == None and self.doleva == None:
            return True
        else:
            return False
    
    def nastav_podle_krizovatky(self, krizov):
        global moznosti_krizovatky

        moznosti = moznosti_krizovatky.get(krizov) # type: ignore
        print(moznosti, krizov)

        self.nahoru = moznosti[0]     # type: ignore
        self.doprava = moznosti[1]    # type: ignore
        self.dolu = moznosti[2]     # type: ignore
        self.doleva = moznosti[3]       # type: ignore

        strung = str([self.nahoru, self.doprava, self.dolu, self.doleva]) # type: ignore
        print(strung)

    def prijezd(self, smer):
        if smer == 0: self.dolu += 1          # type: ignore
        if smer == 1: self.doleva += 1        # type: ignore  
        if smer == 2: self.nahoru += 1        # type: ignore
        if smer == 3: self.doprava += 1       # type: ignore
## odřřádkování
    def odjezd(self, smer):
        if smer == 0: self.nahoru += 1      # type: ignore
        if smer == 1: self.doprava += 1     # type: ignore  
        if smer == 2: self.dolu += 1        # type: ignore
        if smer == 3: self.doleva += 1      # type: ignore

    def print_all(self):
        strung = str([self.nahoru, self.doprava, self.dolu, self.doleva]) # type: ignore
        strung = strung.replace("None", ".")
        strung = strung.replace("[", "")
        strung = strung.replace("]", "")
        strung = strung.replace("-1", "X")
        strung = strung.replace(",", "")
        strung = strung.replace(" ", "")
        strung += " "
        return strung

    def get_smer(self):
        print("\n")
        lst = [self.nahoru, self.doprava, self.dolu, self.doleva]
        print(lst)
        for x in range(len(lst)):
            if lst[x] == -1:
                lst[x] = 3
        kam = lst.index(min(lst)) # type: ignore
        print(kam)
        print("\n")
        return kam
        
        
    def gnahoru(self):
        return self.nahoru
    def gdoprava(self):
        return self.doprava
    def gdoleva(self):
        return self.doleva
    def gdolu(self):
        return self.dolu
    

    def nnahoru(self, x):
        self.nahoru = x
    def ndoprava(self, x):
        self.doprava = x
    def ndolu(self, x):
        self.dolu = x
    def ndoleva(self, x):
        self.doleva = x



pozice = [7,7]
wturn = 0

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

moznosti_krizovatky = {
    "┌" : [-1, 0, 0,-1],
    "┐" : [-1,-1, 0, 0],
    "┘" : [ 0,-1,-1, 0],
    "└" : [ 0, 0,-1,-1],
    "├" : [ 0, 0, 0,-1],
    "┤" : [ 0,-1, 0, 0],
    "┬" : [-1, 0, 0, 0],
    "┴" : [ 0, 0,-1, 0],
    "┼" : [ 0, 0, 0, 0],
    "▫" : [ 0, 0, 0, 0]
}

print("making planek")
planek = []
for _ in range(15):
    temp = []
    for _ in range(15):
        temp.append(policko())
    planek.append(temp)

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


