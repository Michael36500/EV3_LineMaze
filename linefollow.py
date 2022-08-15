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


while True:
    m_s.dc(-50)
    out_t = []
    out = []
    while True:
        out_t.append(cols.reflection())
        # print(m_s.angle())
        if m_s.angle() < -190:
            x = len(out_t) // 20
            for a in range(len(out_t)):
                if a % x == 0:
                    out.append(out_t[a])
            break
    out.reverse()
    turn = min(out)
    turn = out.index(turn)
    print(turn)

    # turn /= 20

    base_speed = 20
    rm = base_speed + turn
    lm = base_speed - turn

    m_l.dc(lm)
    m_r.dc(rm)



    m_s.dc(50)
    out_t = []
    out = []
    while True:
        out_t.append(cols.reflection())
        # print(m_s.angle())
        if toch.pressed() == True:
            m_s.reset_angle(0)
            x = len(out_t) // 20
            for a in range(len(out_t)):
                if a % x == 0:
                    out.append(out_t[a])
            break
    turn = min(out)
    turn = out.index(turn)
    print(turn)
    # turn /= 20

    base_speed = 20
    rm = base_speed + turn
    lm = base_speed - turn

    m_l.dc(lm)
    m_r.dc(rm)
