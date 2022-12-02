#!/usr/bin/env pybricks-micropython
# nutný 1. řádek

# importy pybrixů. u motoru to háže error, ale to je v poho
import pybricks.tools as pt
from pybricks.ev3devices import ColorSensor, Motor, TouchSensor
from pybricks.hubs import EV3Brick
from pybricks.parameters import Color, Direction, Port

ev3_brick = EV3Brick()    

left_motor = Motor(Port.C, positive_direction=Direction.COUNTERCLOCKWISE)
right_motor = Motor(Port.D, positive_direction=Direction.COUNTERCLOCKWISE)

color1 = ColorSensor(Port.S1)
color2 = ColorSensor(Port.S2)
color3 = ColorSensor(Port.S3)

navigace = ColorSensor(Port.S4)

def line():
    # global proměny
    global target_navig
    global p_konstanta
    global zakladni_rychlost
    global hodnota_navigace

    # načtu a spočítám hodnotu toho, jak mám zatočit
    hodnota_navigace = navigace.reflection()
    rozdil = hodnota_navigace - target_navig
    zatacka = p_konstanta * rozdil

    # provedu zatáčku
    right_motor.dc(zakladni_rychlost - zatacka)
    left_motor.dc(zakladni_rychlost + zatacka)

def zatoc_180():
    # předdefinovaná hodnota
    o_kolik = 1210

    # provedu
    left_motor.run_angle(300,  o_kolik, wait=False)
    right_motor.run_angle(300, -o_kolik)

def zatoc_doprava():
    # předdefinovaný posun dopředu(abych se otáčel podél svojí osy a vyšlo to)
    posun_dopředu = 190
    left_motor.run_angle(300, posun_dopředu, wait=False)
    right_motor.run_angle(300, posun_dopředu)


def zatoc_doleva():
    # předdefinový posun dopředu (...)
    o_kolik = 170

