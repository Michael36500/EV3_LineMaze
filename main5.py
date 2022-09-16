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
    # print(navi)
    error = navi - targ
    turn = p * error

    rm = base_speed + turn
    lm = base_speed - turn

    m_r.dc(rm)
    m_l.dc(lm)
# def go_15():
#     speed = 200
#     bckwrd = 170

#     m_r.run_angle(speed, bckwrd, wait=False)
#     m_l.run_angle(speed, bckwrd)
def make_Uturn():
    speed = 400
    # hwmuch = 1288 // 3 * 2
    hwmuch = 1950 // 3 * 2
    bckwrd = 100
    zmena = - 0.07
    # zmena = 0
    m_r.run_angle(speed,  hwmuch * (1 - zmena), wait=False)
    m_l.run_angle(speed, -hwmuch * (1 + zmena))
    # m_r.run_angle(speed,  hwmuch, wait=False)
    # m_l.run_angle(speed, -hwmuch)

    # # m_r.dc( speed // 10)
    # # m_l.dc(-speed // 10)

    # # while True:
    # #     nav = cl1.reflection()
    # #     # print(nav)
    # #     if nav > targ:
    # #         break    

    # m_r.run_angle(speed, -bckwrd, wait=False)
    # m_l.run_angle(speed, -bckwrd)


def make_right():
    global change
    speed = 300
    # hwmuch = 590 // 3 * 2
    bckwrd = 280
    zmena = change + 0.14

    hwmuch = 1950 // 3 * 2 // 2

    m_r.run_angle(speed, -hwmuch * (1 - zmena), wait=False)
    m_l.run_angle(speed,  hwmuch * (1 + zmena))

    # m_r.run_angle(speed, -hwmuch * (1 - change), wait=False)
    # m_l.run_angle(speed,  hwmuch * (1 + change))

    # m_r.dc(-speed // 10 * (1 - zmena))
    # m_l.dc( speed // 10 * (1 + zmena))
    # while True:
    #     nav = navig.reflection()
    #     print(nav)
    #     if nav > targ + 2:
    #         break

    m_r.run_angle(speed, -bckwrd, wait=False)
    m_l.run_angle(speed, -bckwrd)


def make_left():
    global change
    speed = 300
    hwmuch = 590 // 3 * 2
    bckwrd = 280
    m_l.run_angle(speed, -hwmuch * (1 - change), wait=False)
    m_r.run_angle(speed,  hwmuch * (1 + change))
    

    m_r.dc( speed // 10)
    m_l.dc(-speed // 10)
    while True:
        nav = navig.reflection()
        # print(nav)
        if nav < targ + 2:
            break


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

    if inp < thresh_up:
        return True
    elif inp > thresh_dwn:
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

    
def calibrate():
    #!!!!!!!!!!!přesně položeno
    global thresh_up
    global thresh_dwn
    global targ

    thresh_up = cl2.reflection() - 5
    thresh_dwn = (cl1.reflection() + cl3.reflection()) // 2 + 10
    targ = navig.reflection()

    print("thresh_up =", thresh_up)
    print("thresh_dwn =", thresh_dwn)
    print("targ =", targ)

# calibrate()

p = 5
base_speed = 40
thresh_up = 17
thresh_dwn = 11
targ = 8
# thresh_up = 19
# thresh_dwn = 6
# targ = 8
change = 0.6


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
