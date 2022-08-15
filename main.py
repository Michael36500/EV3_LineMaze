#!/usr/bin/env pybricks-micropython
from operator import truediv
from re import X
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import ColorSensor, TouchSensor, Motor
from pybricks.parameters import Port, Direction
import pybricks.tools as pt

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

def rd_rght():
    global rd_spd
    m_s.run_target(rd_spd, trn)
    return cols.reflection()

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
    bckwrd = -250

    m_r.run_angle(speed, -hwmuch * 0.3, wait=False)
    m_l.run_angle(speed,  hwmuch * 1.7)

    m_r.run_angle(speed, bckwrd, wait=False)
    m_l.run_angle(speed, bckwrd)

def make_left():
    speed = 200
    hwmuch = 350
    bckwrd = -250

    m_l.run_angle(speed, -hwmuch * 0.3, wait=False)
    m_r.run_angle(speed,  hwmuch * 1.7)

    m_r.run_angle(speed, bckwrd, wait=False)
    m_l.run_angle(speed, bckwrd)
make_left()

def line():
    global targ
    global p
    global base_speed

    mid = rd_mid_flw()
    error = mid - targ
    turn = p * error

    rm = base_speed + turn
    lm = base_speed - turn

    m_r.dc(lm)
    m_l.dc(rm)

def check():
    global thresh

    # global lft
    # global rgh
    # global mid
    
    lft = rd_lft()
    mid = rd_mid()
    rgh = rd_rght()

    print(lft, mid, rgh)

    if bila(lft) == True and bila(mid) == True and bila(rgh) == True:
        print("U turn")
        make_Uturn()

    if bila(lft) == True and bila(mid) == False and bila(rgh) == False:
    # if lft > thresh_up and rgh < thresh_dwn:
        print("right")
        make_right()

    if bila(lft) == False and bila(mid) == False and bila(rgh) == True:
        print("left")
        make_left()

def bila(inp):
    global thresh_up
    global thresh_dwn

    if inp > thresh_up:
        return True
    elif inp < thresh_dwn:
        return False
    else:
        return None
p = 0.25
base_speed = 12
targ = 8
trn = 40

thresh_up = 17
thresh_dwn = 12

lft = rd_lft()
mid = rd_mid()
rgh = rd_rght()

while True:
    line()
    check()

    # line()
    # check()

    