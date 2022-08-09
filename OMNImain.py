#!/usr/bin/env pybricks-micropython
# !! please, all comments are in czech...
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import ColorSensor, TouchSensor, UltrasonicSensor, Motor
from pybricks.parameters import Port
from pybricks.tools import wait, StopWatch

import math

import functions as fn

# setup kostka, stopky
ev3 = EV3Brick()

# setup motory 
m_lu = Motor(Port.A)
m_ru = Motor(Port.C)
m_rd = Motor(Port.B)
m_ld = Motor(Port.D)

# setup senzory
touchl = TouchSensor(Port.S1)
ultrl = UltrasonicSensor(Port.S2)
ultrr = UltrasonicSensor(Port.S3) 
touchr = TouchSensor(Port.S4)


while True:
    fn.move(0, 40)


    if touchl.pressed() == True or touchr.pressed() == True:
        print("pressed")
        fn.move(180, 40)
        wait(500)
        if ultrl.distance() < ultrr.distance():
            # znamená jedu doprava
            print("doprava")
            fn.move(90, 40)
            while ultrr.distance() > 70:
                print(ultrr.distance())
                fn.move(90, 40)
        else:
            # znamená jedu doleva
            print("doleva")

            fn.move(270, 40)
            while ultrl.distance() > 70:
                print(ultrl.distance())
                fn.move(270, 40)








    # krok dopředu


    # test, jestli nenajde překážku
        # ne 
            # nic
        # ano 
            # krok dozadu
            # jestli lepší vlevo vpravo
                # vlevo
                    # start posun vlevo
                    # while vzdálenost < 10 cm
                        # péass
                # vpravo
                    # start posun vpravo
                    # while vzdálenost < 10 cm
                        # péass