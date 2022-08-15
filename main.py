#!/usr/bin/env pybricks-micropython
from operator import truediv
from re import X
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import ColorSensor, TouchSensor, Motor
from pybricks.parameters import Port, Direction
import pybricks.tools as pt

ev3 = EV3Brick()

m_l = Motor(Port.B)
m_r = Motor(Port.C)
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
    m_s.run_target(rd_spd, -15)
    return cols.reflection()

def rd_lft():
    global rd_spd
    m_s.run_target(rd_spd, trn)
    return cols.reflection()

def rd_rght():
    global rd_spd
    m_s.run_target(rd_spd, -trn)
    return cols.reflection()

def make_Uturn():
    speed = 200
    hwmuch = 700
    m_l.run_angle(speed, hwmuch, wait=False)
    m_r.run_angle(speed, -hwmuch)

    m_l.run_angle(speed, 100, wait=False)
    m_r.run_angle(speed, 100)

def make_right():
    speed = 200
    hwmuch = 350
    m_l.run_angle(speed, -hwmuch, wait=False)
    m_r.run_angle(speed, hwmuch)

    m_l.run_angle(speed, 100, wait=False)
    m_r.run_angle(speed, 100)

def make_left():
    speed = 200
    hwmuch = 350
    m_l.run_angle(speed, hwmuch, wait=False)
    m_r.run_angle(speed, -hwmuch)

    m_l.run_angle(speed, 100, wait=False)
    m_r.run_angle(speed, 100)

def line():
    global targ
    global p
    global base_speed

    mid = rd_mid_flw()
    error = mid - targ
    turn = p * error

    rm = base_speed + turn
    lm = base_speed - turn

    m_r.dc(rm)
    m_l.dc(lm)

def check():
    global thresh

    global lft
    global rgh
    global mid
    
    mid = rd_mid()

    print(lft, rgh)

    if bila(lft) == True and bila(mid) == True and bila(rgh) == True:
        print("U turn")
        make_Uturn()

    if bila(lft) == True and bila(mid) == False and bila(rgh) == False:
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
p = 0.5
base_speed = 15
targ = 8
trn = 50

thresh_up = 20
thresh_dwn = 10

# lft = rd_lft()
# mid = rd_mid()
# rgh = rd_rght()

while True:
    lft = rd_lft()
    line()
    check()

    rgh = rd_rght()
    line()
    check()

    