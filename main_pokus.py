#!/usr/bin/env pybricks-micropython
import pybricks.tools as pt
from pybricks.ev3devices import ColorSensor, Motor, TouchSensor
from pybricks.hubs import EV3Brick
from pybricks.parameters import Color, Direction, Port

ev3 = EV3Brick()    

m_l = Motor(Port.C, positive_direction=Direction.COUNTERCLOCKWISE)
m_r = Motor(Port.D, positive_direction=Direction.COUNTERCLOCKWISE)

cl1 = ColorSensor(Port.S1)
cl2 = ColorSensor(Port.S2)
cl3 = ColorSensor(Port.S3)

navig = ColorSensor(Port.S4)


def line():
    global targ
    global p
    global base_speed
    global navi

    navi = navig.reflection()
    error = navi - targ
    turn = p * error

    rm = base_speed - turn
    lm = base_speed + turn

    m_r.dc(rm)
    m_l.dc(lm)

def stop():
    global thresh_dwn
    for a in range(99999*99999):
        c1 = cl1.reflection()
        c2 = cl2.reflection()
        c3 = cl3.reflection()
        if a % 100 == 0:
            print(c1, c2, c3)

        if bila(c1) == True and bila(c2) == False and bila(c3) == True:
            # pt.wait(50)
            m_l.dc(0)
            m_r.dc(0)
            pt.wait(50)
            break

def make_Uturn():
    speed = 300
    hwmuch = 600 * 2
    m_l.run_angle(speed,  hwmuch, wait=False)
    m_r.run_angle(speed, -hwmuch)
    c1 = cl1.reflection()
    c2 = cl2.reflection()
    c3 = cl3.reflection()
    navi = navig.reflection()
    print(c1, c2, c3, navi)

def make_right():
    speed = 300
    posun = 190
    m_l.run_angle(speed, posun, wait=False)
    m_r.run_angle(speed, posun)

    speed = 300
    hwmuch = 610
    m_l.run_angle(speed,  hwmuch, wait=False)
    m_r.run_angle(speed, -hwmuch)

def make_left():
    speed = 300
    posun = 170
    m_l.run_angle(speed, posun, wait=False)
    m_r.run_angle(speed, posun)

    speed = 300
    hwmuch = -610
    m_l.run_angle(speed,  hwmuch, wait=False)
    m_r.run_angle(speed, -hwmuch)
        

def make_strght():
    # for skipping crossing
    speed = 300
    hwmuch = 210

    m_l.run_angle(speed, hwmuch, wait=False)
    m_r.run_angle(speed, hwmuch)

def updt_memory():
    global memory
    try:
        if memory[-2] == "U" and len(memory) >= 3:
            scnd = memory.pop()
            memory.pop()
            frst = memory.pop()
            if frst == "L" and scnd == "L":
                memory.append("S")
            if frst == "S" and scnd == "L":
                memory.append("R")
            if frst == "L" and scnd == "S":
                memory.append("R")
    except:
        pass


def rd_fwd():
    global lft_fwd
    global rgh_fwd
    global mid_fwd

    speed = 300
    hwmuch = 200

    m_r.run_angle(speed, hwmuch, wait=False)
    m_l.run_angle(speed, hwmuch)

    lft_fwd = cl1.reflection()
    mid_fwd = cl2.reflection()
    rgh_fwd = cl3.reflection()

    m_r.run_angle(speed, -hwmuch, wait=False)
    m_l.run_angle(speed, -hwmuch)
def bila(inp):
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! nastavené na bílou čáru, černé
    global thresh_up
    global thresh_dwn

    if inp > thresh_up:
        return True
    elif inp < thresh_dwn:
        return False
    else:
        return None
def rd_all():
    global lft
    global rgh
    global mid

    lft = cl1.reflection()
    mid = cl2.reflection()
    rgh = cl3.reflection()
def check():
    global lft
    global rgh
    global mid
    
    global lft_fwd
    global rgh_fwd
    global mid_fwd

    global somenum

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
            updt_memory()
            rd_all()
        if bila(lft_fwd) == True and bila(mid_fwd) == False and bila(rgh_fwd) == True:
            pebug()
            print("J")
            memory.append("L")
            make_left()
            updt_memory()
            rd_all()

    if bila(lft) == True and bila(mid) == False and bila(rgh) == False:
        pebug()
        rd_fwd()
        somenum = 0
        if bila(lft_fwd) == True and bila(mid_fwd) == True and bila(rgh_fwd) == True:
            pebug()
            print("R")
            # memory.append("L")
            make_right()
            updt_memory()
            rd_all()
        if bila(lft_fwd) == True and bila(mid_fwd) == False and bila(rgh_fwd) == True:
            pebug()
            print("K")
            memory.append("S")
            make_strght()
            updt_memory()
            rd_all()

    if bila(lft) == False and bila(mid) == False and bila(rgh) == False:
        pebug()
        rd_fwd()
        somenum = 0
        if bila(lft_fwd) == True and bila(mid_fwd) == True and bila(rgh_fwd) == True:
            pebug()
            print("T")
            memory.append("L")
            make_left()
            updt_memory()
            rd_all()
        if bila(lft_fwd) == True and bila(mid_fwd) == False and bila(rgh_fwd) == True:
            pebug()
            print("+")
            memory.append("L")
            make_left()
            updt_memory()
            rd_all()
        if bila(lft_fwd) == False and bila(mid_fwd) == False and bila(rgh_fwd) == False:
            pebug()
            print("FINISH")
            # memory.append("F")
            return "out"

    if bila(lft)== True and bila(mid) == True and bila(rgh) == True:
        pebug()
        rd_fwd()
        if bila(lft_fwd)== True and bila(mid_fwd) == True and bila(rgh_fwd) == True:
            pebug()
            print("U")
            memory.append("U")
            make_Uturn()
            updt_memory()
            rd_all()

def pebug():
    global lft
    global rgh
    global mid

    global navi
    
    global lft_fwd
    global rgh_fwd
    global mid_fwd

    global somenum

    print(bila(lft_fwd), bila(mid_fwd), bila(rgh_fwd), lft_fwd, mid_fwd, rgh_fwd)
    print(bila(lft), bila(mid), bila(rgh), lft, mid, rgh)
    print(navi)
    print(memory)
    print()

# BROKEN    
# def calibrate():
#     #!!!!!!!!!!!přesně položeno
#     global thresh_up
#     global thresh_dwn
#     global targ

#     thresh_up = cl2.reflection() - 5
#     thresh_dwn = (cl1.reflection() + cl3.reflection()) // 2 + 8
#     targ = navig.reflection()

#     print("thresh_up =", thresh_up)
#     print("thresh_dwn =", thresh_dwn)
#     print("targ =", targ)
def read_sensors():
    print(cl1.reflection())
    print(cl2.reflection())
    print(cl3.reflection())
    print(navig.reflection())
# calibrate()

p = 2
base_speed = 40

# thresh_up = 17
# thresh_dwn = 11
# targ = 8
# thresh_up = 19
# thresh_dwn = 6
# targ = 8
# thresh_up = 18
# thresh_dwn = 14
# targ = 8
# thresh_up = 40
# thresh_dwn = 67
# targ = 51
# thresh_up = 32
# thresh_dwn = 11
# targ = 16
thresh_up = 25
thresh_dwn = 14
targ = 15

# change = 0.6


memory = []
somenum = 0


rd_all()
rd_fwd()
navi = 7

# for _ in range(250):
#     rd_all()
#     line()

# print("found")

while True:
    rd_all()
    line()
    if check() == "out":
        break

# while True:
#     line()