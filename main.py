#!/usr/bin/env pybricks-micropython
import pybricks.tools as pt
from pybricks.ev3devices import ColorSensor, Motor, TouchSensor
from pybricks.hubs import EV3Brick
from pybricks.parameters import Direction, Port

ev3 = EV3Brick()

m_r = Motor(Port.B)
m_l = Motor(Port.C)
m_s = Motor(Port.D, positive_direction=Direction.COUNTERCLOCKWISE)

cols = ColorSensor(Port.S4)
toch = TouchSensor(Port.S2)


def vynuluj():
    # global toch
    m_s.dc(50)

    while True:
        if toch.pressed() == True:
            pt.wait(100)
            m_s.reset_angle(0)
            break
vynuluj()

m_s.run_angle(300, -95)
m_s.reset_angle(0)


rd_spd = 1000
def rd_mid():
    global rd_spd
    m_s.run_target(rd_spd, 0)
    return cols.reflection()

def rd_mid_flw():
    global rd_spd
    m_s.run_target(rd_spd, -10)
    return cols.reflection()

def rd_lft():
    global rd_spd
    m_s.run_target(rd_spd, -trn)
    return cols.reflection()

def rd_rgh():
    global rd_spd
    m_s.run_target(rd_spd, trn)
    return cols.reflection()

def rd_all():
    global lft
    global rgh
    global mid

    lft = rd_lft()
    mid = rd_mid()
    rgh = rd_rgh()
def make_Uturn():
    speed = 200
    hwmuch = 720
    m_r.run_angle(speed, hwmuch, wait=False)
    m_l.run_angle(speed, -hwmuch)

    m_r.run_angle(speed, 100, wait=False)
    m_l.run_angle(speed, 100)


def make_right():
    speed = 200
    hwmuch = 350
    bckwrd = -220

    m_r.run_angle(speed, -hwmuch * 0.3, wait=False)
    m_l.run_angle(speed,  hwmuch * 1.7)

    m_r.run_angle(speed, bckwrd, wait=False)
    m_l.run_angle(speed, bckwrd)

def make_left():
    speed = 200
    hwmuch = 350
    bckwrd = -220

    m_l.run_angle(speed, -hwmuch * 0.3, wait=False)
    m_r.run_angle(speed,  hwmuch * 1.7)

    m_r.run_angle(speed, bckwrd, wait=False)
    m_l.run_angle(speed, bckwrd)

def make_strght():
    speed = 200
    hwmuch = 150    #vyladit !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    m_l.run_angle(speed, hwmuch, wait=False)
    m_r.run_angle(speed, hwmuch)

def line():
    global targ
    global p
    global base_speed

    mid = rd_mid_flw()
    error = mid - targ
    turn = p * error

    rm = base_speed + turn
    lm = base_speed - turn

    # print(lm, rm)

    m_r.dc(lm)
    m_l.dc(rm)

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

def check():
    global lft
    global rgh
    global mid
    
    global lft_fwd
    global rgh_fwd
    global mid_fwd

    mid = rd_mid()

    print(lft_fwd, mid_fwd, rgh_fwd)
    print(lft, mid, rgh)
    print(memory)
    print()

    if bila(lft) == False and bila(mid) == False and bila(rgh) == True:
        read_fwd()
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
        read_fwd()
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
        read_fwd()
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
        read_fwd()
        if bila(lft_fwd)== True and bila(mid_fwd) == True and bila(rgh_fwd) == True:
            print("U")
            memory.append("U")
            make_Uturn()
            updt_memory()
            rd_all()


def read_fwd():
    global lft_fwd
    global rgh_fwd
    global mid_fwd

    speed = 100
    hwmuch = 75

    m_r.run_angle(speed, hwmuch, wait=False)
    m_l.run_angle(speed, hwmuch)

    lft_fwd = rd_lft()
    mid_fwd = rd_mid()
    rgh_fwd = rd_rgh()

    m_r.run_angle(speed, -hwmuch, wait=False)
    m_l.run_angle(speed, -hwmuch)
    

def bila(inp):
    global thresh_up
    global thresh_dwn

    if inp > thresh_up:
        return True
    elif inp < thresh_dwn:
        return False
    else:
        return None
p = 0.2
base_speed = 10
targ = 8
trn = 40

thresh_up = 16
thresh_dwn = 12

memory = []

lft = rd_lft()
mid = rd_mid()
rgh = rd_rgh()


read_fwd()

while True:
    lft = rd_lft()
    line()
    if check() == "out":
        break

    rgh = rd_rgh()
    line()
    if check() == "out":
        break

# add execute found path