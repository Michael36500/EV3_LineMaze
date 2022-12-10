#!/usr/bin/env pybricks-micropython
import pybricks.tools as pt
from pybricks.ev3devices import ColorSensor, Motor, TouchSensor  # type: ignore
from pybricks.hubs import EV3Brick
from pybricks.parameters import Color, Direction, Port
from pybricks.robotics import DriveBase
import random

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
    print()

def make_decision(kriz):
    moznosti = {"U": ["U"], "L":["L"], "R":["R"], "J":["S", "L"], "K":["S","R"], "T":["R","L"], "+":["R","L","S"]}
    vyber = moznosti[kriz]



    if len(vyber) == 1: rand = vyber[0]
    else: rand = vyber[random.randint(0, len(vyber) - 1)]

    print(vyber, kriz)
    if rand == "R":
        make_right()
    if rand == "L":
        make_left()
    if rand == "S":
        make_strght()
    if rand == "U":
        make_Uturn()


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
            pebug()
            make_decision("L")
            rd_all()
        elif bila(lft_fwd) == True and bila(mid_fwd) == False and bila(rgh_fwd) == True:
            print("J")
            pebug()
            make_decision("J")
            rd_all()
        else:
            print("FUCK FFT!!!")

    elif bila(lft) == True and bila(mid) == False and bila(rgh) == False:
        rd_fwd()
        somenum = 0
        if bila(lft_fwd) == True and bila(mid_fwd) == True and bila(rgh_fwd) == True:
            print("R")
            pebug()
            make_decision("R")
            rd_all()
        elif bila(lft_fwd) == True and bila(mid_fwd) == False and bila(rgh_fwd) == True:
            print("K")
            pebug()
            make_decision("K")
            rd_all()
        else:
            print("FUCK TFF!!!")

    elif bila(lft) == False and bila(mid) == False and bila(rgh) == False:
        rd_fwd()
        somenum = 0
        if bila(lft_fwd) == True and bila(mid_fwd) == True and bila(rgh_fwd) == True:
            print("T")
            pebug()
            make_decision("T")
            rd_all()
        elif bila(lft_fwd) == True and bila(mid_fwd) == False and bila(rgh_fwd) == True:
            print("+")
            pebug()
            make_decision("+")
            rd_all()
        elif bila(lft_fwd) == False and bila(mid_fwd) == False and bila(rgh_fwd) == False:
            print("FINISH")
            return "out"

    elif bila(lft) == True and bila(mid) == True and bila(rgh) == True:
        rd_fwd()
        if bila(lft_fwd) == True and bila(mid_fwd) == True and bila(rgh_fwd) == True:
            print("U")
            pebug()
            make_decision("U")
            rd_all()
        else:
            print("FUCK TTT!!!")

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
    if navi > targ:
        ev3.light.on(Color.RED)
    if navi < targ:
        ev3.light.on(Color.ORANGE)
    navi = navig.reflection()
ev3.light.on(Color.GREEN)
robot.reset()
pt.wait(500)




rd_all()
rd_fwd()

while True:
    rd_all()
    line()
    if check() == "out":
        break

