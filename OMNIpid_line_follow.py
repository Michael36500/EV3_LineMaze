#!/usr/bin/env pybricks-micropython
# tohole musí být 1. rádek

# importy
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, ColorSensor, TouchSensor
from pybricks.parameters import Port
from pybricks.tools import wait, StopWatch
import sys


import functions as fn

# setup kostka, stopky
ev3 = EV3Brick()

# setup motory 
m_lu = Motor(Port.A)
m_ru = Motor(Port.C)
m_rd = Motor(Port.B)
m_ld = Motor(Port.D)


# vstupuju  čísla, a točím motory
def run_m (lu, ru, rd, ld):
    global m_lu
    global m_ru
    global m_rd
    global m_ld

    lu = round(lu)
    ru = round(ru)
    rd = round(rd)
    ld = round(ld)    
    
    rd *= -1
    ld *= -1

    m_lu.dc(lu)
    m_ru.dc(ru)
    m_rd.dc(rd)
    m_ld.dc(ld)

# funkce z vstupu se pohne nahoru/dolů/otočí se
def UDLR(ud, lr, rot):
    lu = ud + lr + rot
    ru = ud - lr - rot
    rd = ud + lr - rot
    ld = ud - lr + rot

    run_m(lu, ru, rd, ld)

cols = ColorSensor(Port.S1)

up = 17
down = 6

targ = (up + down) // 2
print(targ)

previous_er = 0
integ = 0
base_speed = 25

while True:
    refl = cols.reflection()

    p = 8
    i = 0.008
    d = 0.01

    error = refl - targ
    integ = integ + error
    deriv = error - previous_er

    turn = p * error + i * integ + d * deriv
    rm = base_speed + turn
    lm = base_speed - turn

    run_m(lm, rm, rm, lm)



    previous_er = error