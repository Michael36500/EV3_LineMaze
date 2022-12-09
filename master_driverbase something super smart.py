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
    robot.turn(180)
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

    # robot.straight(-30)

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
    print(pozice, "pozice", wturn, "wturn")
    print()


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

    if somenum % 100 == 0:
        pebug()

    if bila(lft) == False and bila(mid) == False and bila(rgh) == True:
        rd_fwd()
        somenum = 0
        if bila(lft_fwd) == True and bila(mid_fwd) == True and bila(rgh_fwd) == True:
            print("L")
            updt_kola()
            make_left()
            rd_all()
        elif bila(lft_fwd) == True and bila(mid_fwd) == False and bila(rgh_fwd) == True:
            print("J")
            updt_kola()
            make_left()
            rd_all()
        else:
            print("FUCK FFT!!!")

    elif bila(lft) == True and bila(mid) == False and bila(rgh) == False:
        rd_fwd()
        somenum = 0
        if bila(lft_fwd) == True and bila(mid_fwd) == True and bila(rgh_fwd) == True:
            print("R")
            updt_kola()
            make_right()
            rd_all()
        elif bila(lft_fwd) == True and bila(mid_fwd) == False and bila(rgh_fwd) == True:
            print("K")
            updt_kola()
            make_strght()
            rd_all()
        else:
            print("FUCK TFF!!!")

    elif bila(lft) == False and bila(mid) == False and bila(rgh) == False:
        rd_fwd()
        somenum = 0
        if bila(lft_fwd) == True and bila(mid_fwd) == True and bila(rgh_fwd) == True:
            print("T")
            updt_kola()
            make_left()
            rd_all()
        elif bila(lft_fwd) == True and bila(mid_fwd) == False and bila(rgh_fwd) == True:
            print("+")
            updt_kola()
            make_left()
            rd_all()
        elif bila(lft_fwd) == False and bila(mid_fwd) == False and bila(rgh_fwd) == False:
            print("FINISH")
            return "out"

    elif bila(lft) == True and bila(mid) == True and bila(rgh) == True:
        rd_fwd()
        if bila(lft_fwd) == True and bila(mid_fwd) == True and bila(rgh_fwd) == True:
            print("U")
            updt_kola()
            make_Uturn()
            rd_all()
        else:
            print("FUCK TTT!!!")
            make_strght()

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

xpole, ypole = 7, 4
memory = [[] * xpole] * ypole


pozice = [6, 5]
wturn = 3

cis = 0
najeto_na_kolech = []
najeto_na_kolech2 = []

p = 2.5
base_speed = 75

thresh_up = 26
thresh_dwn =  16
targ = 12

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

