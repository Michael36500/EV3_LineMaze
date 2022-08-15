#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import ColorSensor, TouchSensor, Motor
from pybricks.parameters import Port

ev3 = EV3Brick()

m_l = Motor(Port.B)
m_r = Motor(Port.C)

cols = ColorSensor(Port.S4)


up = 9
down = 3

targ = (up + down) // 2
print(targ)

previous_er = 0
integ = 0
base_speed = 15

while True:

    refl = cols.reflection()    
    print(refl)

    p = 8
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