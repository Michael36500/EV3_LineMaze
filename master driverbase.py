#!/usr/bin/env pybricks-micropython
import pybricks.tools as pt
from pybricks.ev3devices import ColorSensor, Motor, TouchSensor
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

    robot.drive(base_speed, turn)

def make_Uturn():
    robot.turn(180)

def make_right():
    ## vylaď
    robot.straight(50)
    robot.turn(90)

def make_left():
    ## vylaď
    robot.straight(50)
    robot.turn(-90)

def make_strght():
    # for skipping crossing
    robot.straight(30)
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

    robot.straight(-30)

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

    print(bila(lft_fwd), bila(mid_fwd), bila(rgh_fwd), lft_fwd, mid_fwd, rgh_fwd)
    print(bila(lft), bila(mid), bila(rgh), lft, mid, rgh)
    print(navi)
    print(memory)
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
        pebug()
        rd_fwd()
        somenum = 0
        if bila(lft_fwd) == True and bila(mid_fwd) == True and bila(rgh_fwd) == True:
            pebug()
            print("L")
            # memory.append("L")
            make_left()
            rd_all()
        elif bila(lft_fwd) == True and bila(mid_fwd) == False and bila(rgh_fwd) == True:
            pebug()
            print("J")
            memory.append("L")
            make_left()
            rd_all()
        else:
            print("FUCK!!!")

          

    elif bila(lft) == True and bila(mid) == False and bila(rgh) == False:
        pebug()
        rd_fwd()
        somenum = 0
        if bila(lft_fwd) == True and bila(mid_fwd) == True and bila(rgh_fwd) == True:
            pebug()
            print("R")
            # memory.append("L")
            make_right()
            rd_all()
        elif bila(lft_fwd) == True and bila(mid_fwd) == False and bila(rgh_fwd) == True:
            pebug()
            print("K")
            memory.append("S")
            make_strght()
            rd_all()
        else:
            print("FUCK!!!")

    elif bila(lft) == False and bila(mid) == False and bila(rgh) == False:
        pebug()
        rd_fwd()
        somenum = 0
        if bila(lft_fwd) == True and bila(mid_fwd) == True and bila(rgh_fwd) == True:
            pebug()
            print("T")
            memory.append("L")
            make_left()
            rd_all()
        elif bila(lft_fwd) == True and bila(mid_fwd) == False and bila(rgh_fwd) == True:
            pebug()
            print("+")
            memory.append("L")
            make_left()
            rd_all()
        elif bila(lft_fwd) == False and bila(mid_fwd) == False and bila(rgh_fwd) == False:
            pebug()
            print("FINISH")
            # memory.append("F")
            return "out"

    elif bila(lft) == True and bila(mid) == True and bila(rgh) == True:
        pebug()
        rd_fwd()
        if bila(lft_fwd) == True and bila(mid_fwd) == True and bila(rgh_fwd) == True:
            pebug()
            print("U")
            memory.append("U")
            make_Uturn()
            rd_all()
        # elif bila(lft_fwd) == True and bila(mid_fwd) == True and bila(rgh_fwd) != True:
        #     print("fuck, going right")
        #     speed = 300
        #     hwmuch = -100
        #     m_l.run_angle(speed,  hwmuch, wait=False)
        #     m_r.run_angle(speed, -hwmuch)

        # elif bila(lft_fwd) != True and bila(mid_fwd) == True and bila(rgh_fwd) == True:
        #     print("fuck, going left")
        #     speed = 300
        #     hwmuch = 150
        #     m_l.run_angle(speed,  hwmuch, wait=False)
        #     m_r.run_angle(speed, -hwmuch)
        else:
            print("FUCK!!!")



p = 3
base_speed = 80   

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




str = ""

for x in memory:
    str += x

print(str)

str_start = None

while str_start != str:
    str_start = str
    str = str.replace("LUL", "S")
    str = str.replace("LUS", "R")
    str = str.replace("SUL", "R")
    str = str.replace("RUL", "U")
    str = str.replace("SUS", "U")

print(str)