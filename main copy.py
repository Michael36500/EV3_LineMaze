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


trn = 40

def rd_mid():
    m_s.run_target(500, 0)
    return cols.reflection()

def rd_lft():
    m_s.run_target(500, trn)
    return cols.reflection()

def rd_rght():
    m_s.run_target(500, -trn)
    return cols.reflection()

def line():
    global lft
    global mid
    global rgh
    global p
    if lft == rgh:
        rm = base_speed
        lm = base_speed

    if lft > rgh:
        rm = base_speed - (p * mid)
        lm = base_speed + (p * mid)

    if lft < rgh:
        rm = base_speed + (p * mid)
        lm = base_speed - (p * mid)

    m_l.dc(lm)
    m_r.dc(rm)
    # print(lm, rm)




p = 0.25
base_speed = 15

lft = rd_lft()
mid = rd_mid()
rgh = rd_rght()

while True:
    lft = rd_lft()
    line()
    mid = rd_mid()
    line()
    rgh = rd_rght()
    line()

    