#!/usr/bin/env pybricks-micropython
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


def make_Uturn():
    speed = 400
    hwmuch = 710
    m_l.run_angle(speed, hwmuch, wait=False)
    m_r.run_angle(speed, -hwmuch)
for _ in range(10):
    make_Uturn()