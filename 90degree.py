#!/usr/bin/env pybricks-micropython
import pybricks.tools as pt
from pybricks.ev3devices import ColorSensor, Motor, TouchSensor
from pybricks.hubs import EV3Brick
from pybricks.parameters import Color, Direction, Port

ev3 = EV3Brick()    

m_l = Motor(Port.C, positive_direction=Direction.COUNTERCLOCKWISE)
m_r = Motor(Port.D, positive_direction=Direction.COUNTERCLOCKWISE)

cl1 = ColorSensor(Port.S1)
cl2 = ColorSensor(Port.S2)
cl3 = ColorSensor(Port.S3)

navig = ColorSensor(Port.S4)

def left():
    speed = 1000
    hwmuch = -590
    m_l.run_angle(speed,  hwmuch, wait=False)
    m_r.run_angle(speed, -hwmuch)

def right():
    speed = 1000
    hwmuch = 590
    m_l.run_angle(speed,  hwmuch, wait=False)
    m_r.run_angle(speed, -hwmuch)

for _ in range(16):
    right()