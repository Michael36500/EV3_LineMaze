#!/usr/bin/env pybricks-micropython
from operator import truediv
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

def naskenuj():
    m_s.run_angle(750, -180)
    out_t = []
    out = []

    m_s.dc(50)

    while True:
        out_t.append(cols.reflection())
        if toch.pressed() == True:
            # pt.wait(50)
            m_s.reset_angle(0)
            for a in range(len(out_t)):
                if a % 20 == 0:
                    out.append(out_t[a])
            return out


def flw_line ():
    m_s.run_angle(750, -75)
    up = 8  
    down = 2
    targ = (up + down) // 2

    previous_er = 0
    integ = 0
    base_speed = 25
    while True:
        refl = cols.reflection()
        print(refl, end=", ")

        p = 4
        i = 0.01
        d = 0.01

        error = refl - targ
        integ = integ + error
        deriv = error - previous_er

        turn = p * error + i * integ + d * deriv
        rm = base_speed + turn
        lm = base_speed - turn

        m_l.dc(lm)
        m_r.dc(rm)

        previous_er = error


        tols = 2
        if refl > up - tols or refl < down + tols:
            print("kříž ovat katce")
            break


flw_line()