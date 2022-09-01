#!/usr/bin/env pybricks-micropython
import pybricks.tools as pt
from pybricks.ev3devices import ColorSensor, Motor, TouchSensor
from pybricks.hubs import EV3Brick
from pybricks.parameters import Direction, Port, Color

ev3 = EV3Brick()    

m_l = Motor(Port.A)
m_r = Motor(Port.B)

cl1 = ColorSensor(Port.S1)
cl2 = ColorSensor(Port.S2)
cl3 = ColorSensor(Port.S3)



def line():
    global targ
    global p
    global base_speed

    mid = cl2.reflection()
    error = mid - targ
    turn = p * error

    rm = base_speed + turn
    lm = base_speed - turn

    print(lm, rm)

    m_r.dc(rm, wait = False)
    m_l.dc(lm)

targ = 6
p = 0.2
base_speed = 20

# while True:
#     line()
