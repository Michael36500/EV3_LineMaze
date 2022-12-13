#!/usr/bin/env pybricks-micropython
import pybricks.tools as pt
from pybricks.ev3devices import ColorSensor, Motor, TouchSensor  # type: ignore
from pybricks.hubs import EV3Brick
from pybricks.parameters import Color, Direction, Port
from pybricks.robotics import DriveBase

# kostka
ev3 = EV3Brick() 

def jsem_v_cili():
    ev3.speaker.set_volume(80)
    ev3.speaker.play_file("/home/robot/EV3_LineMaze2/rickroll.wav")
    pt.wait(10)

jsem_v_cili()