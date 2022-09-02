#!/usr/bin/env pybricks-micropython
from re import X
import pybricks.tools as pt
from pybricks.ev3devices import ColorSensor, Motor, TouchSensor
from pybricks.hubs import EV3Brick
from pybricks.parameters import Direction, Port, Color

ev3 = EV3Brick()    

m_l = Motor(Port.C, positive_direction=Direction.COUNTERCLOCKWISE)
m_r = Motor(Port.D, positive_direction=Direction.COUNTERCLOCKWISE)

cl1 = ColorSensor(Port.S1)
cl2 = ColorSensor(Port.S2)
cl3 = ColorSensor(Port.S3)



def line():
    global targ
    global p
    global base_speed

    lft = cl1.reflection()
    error = lft - targ
    turn = p * error

    rm = base_speed + turn
    lm = base_speed - turn

    m_r.dc(rm)
    m_l.dc(lm)
def go_15():
    speed = 200
    bckwrd = 170

    m_r.run_angle(speed, bckwrd, wait=False)
    m_l.run_angle(speed, bckwrd)
def make_Uturn():
    speed = 200
    hwmuch = 460
    bckwrd = 100

    m_r.run_angle(speed, -hwmuch, wait=False)
    m_l.run_angle(speed,  hwmuch)

    m_r.run_angle(speed, -bckwrd, wait=False)
    m_l.run_angle(speed, -bckwrd)
def make_right():
    speed = 200
    hwmuch = 220
    bckwrd = 100
    change = 0.6

    m_r.run_angle(speed, -hwmuch * (1 - change), wait=False)
    m_l.run_angle(speed,  hwmuch * (1 + change))

    m_r.run_angle(speed, -bckwrd, wait=False)
    m_l.run_angle(speed, -bckwrd)
def make_left():
    speed = 200
    hwmuch = 220
    bckwrd = 100
    change = 0.6

    m_l.run_angle(speed, -hwmuch * (1 - change), wait=False)
    m_r.run_angle(speed,  hwmuch * (1 + change))

    m_r.run_angle(speed, -bckwrd, wait=False)
    m_l.run_angle(speed, -bckwrd)
def make_strght():
    # for skipping crossing
    speed = 200
    hwmuch = 75

    m_l.run_angle(speed, hwmuch, wait=False)
    m_r.run_angle(speed, hwmuch)
def updt_memory():
    global memory
    try:
        if memory[-2] == "U":
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

    speed = 100
    hwmuch = 75

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
        print(bila(lft_fwd), bila(mid_fwd), bila(rgh_fwd), lft_fwd, mid_fwd, rgh_fwd)
        print(bila(lft), bila(mid), bila(rgh), lft, mid, rgh)
        print(memory)
        print()

    if bila(lft) == False and bila(mid) == False and bila(rgh) == True:
        rd_fwd()
        somenum = 0
        if bila(lft_fwd) == True and bila(mid_fwd) == True and bila(rgh_fwd) == True:
            print("L")
            # memory.append("L")
            make_left()
            updt_memory()
            rd_all()
        if bila(lft_fwd) == True and bila(mid_fwd) == False and bila(rgh_fwd) == True:
            print("J")
            memory.append("L")
            make_left()
            updt_memory()
            rd_all()

    if bila(lft) == True and bila(mid) == False and bila(rgh) == False:
        rd_fwd()
        somenum = 0
        if bila(lft_fwd) == True and bila(mid_fwd) == True and bila(rgh_fwd) == True:
            print("R")
            # memory.append("L")
            make_right()
            updt_memory()
            rd_all()
        if bila(lft_fwd) == True and bila(mid_fwd) == False and bila(rgh_fwd) == True:
            print("K")
            memory.append("S")
            make_strght()
            updt_memory()
            rd_all()

    if bila(lft) == False and bila(mid) == False and bila(rgh) == False:
        rd_fwd()
        somenum = 0
        if bila(lft_fwd) == True and bila(mid_fwd) == True and bila(rgh_fwd) == True:
            print("T")
            memory.append("L")
            make_left()
            updt_memory()
            rd_all()
        if bila(lft_fwd) == True and bila(mid_fwd) == False and bila(rgh_fwd) == True:
            print("+")
            memory.append("L")
            make_left()
            updt_memory()
            rd_all()
        if bila(lft_fwd) == False and bila(mid_fwd) == False and bila(rgh_fwd) == False:
            print("FINISH")
            # memory.append("F")
            return "out"

    if bila(lft)== True and bila(mid) == True and bila(rgh) == True:
        rd_fwd()
        if bila(lft_fwd)== True and bila(mid_fwd) == True and bila(rgh_fwd) == True:
            print("U")
            memory.append("U")
            make_Uturn()
            updt_memory()
            rd_all()



p = 1
base_speed = 30 
thresh_up = 16
thresh_dwn = 8
targ = 7

memory = []
somenum = 0

rd_all()
rd_fwd()

while True:
    rd_all()
    line()
    if check() == "out":
        break

# while True:
#     line()