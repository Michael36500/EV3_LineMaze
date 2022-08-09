#!/usr/bin/env pybricks-micropython
# tohole musí být 1. rádek

# importy
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, ColorSensor, TouchSensor
from pybricks.parameters import Port
from pybricks.tools import wait, StopWatch
import sys
# import img2num as imgnm



# setup kostka, stopky
ev3 = EV3Brick()

# setup touch senzory
touch_sensor = TouchSensor(Port.S4)
# touch_spust = TouchSensor(Port.S3)

# setup motory 
M_papir = Motor(Port.A)
M_vozik = Motor(Port.B)
M_pero = Motor(Port.C)

# setup is_up (pro řádek), cerna (is_up pro sloupce)
is_up = True
cerna = False
docasna = 0

# setup odsazení od okraje, zespodu
set_dal = 0
dal = set_dal
paper = 0

# setup velikost obrázku, potřeba vyladit k sobě
# zmena_p = 2.5
zmena_p = 3
zmena_carka = zmena_p   #?s
zmena_radek = zmena_p * 1.5

# setup toho, co chci tisknout
robot = robot.robot()

sirka = 266
    

# setup aktuální číslo řádku, celkem dopočítáno, pro procenta
cislo_radku = 0
pocet_radku = 0
for a in robot:
    if a == -1:
        pocet_radku = pocet_radku + 1
print(pocet_radku)


# chytrá funukce na zvednutí propisky (testuje, jestli není)
##################################################################
# how_much může dělat problémy
def push_up():
    global is_up
    #global M_pero
    if is_up == False:
        M_pero.run_target(200,20)
        is_up = True

        
# chytrá funukce na dolů propisky (testuje, jestli není)
def push_down(): 
    global is_up
    if is_up == True:
        M_pero.run_target(200, 0)
        is_up = False

# dojede na začátek 
def jdi_na():
    M_vozik.run(150)                # >>>>>>>>>>>>>>>>>>>>>>>>>> když jsem s, tak 400, jinak 200
    while True:
        if touch_sensor.pressed():
            M_vozik.brake()
            M_vozik.reset_angle(0)
            break 

# udělá nový řádek
def NRadek():
    global paper
    global dal
    global cislo_radku
    dal = set_dal
    push_up()
    #push_up()
    cislo_radku = cislo_radku + 1
    #M_pero.run_target(100, 0)
    # print ("\x1b[K",  2(cislo_radku/pocet_radku)*100,"%", cislo_radku, ". radek", stop_w.time()/60000, "ETA:", (1-(cislo_radku/pocet_radku)) * (stop_w.time() / 60000), end="\r" )
    procenta = round((cislo_radku/pocet_radku) * 100, 2)
    cas = round((stop_w.time()/60000), 5)
    print (cislo_radku,". radek", procenta,"%", cas, "min")

    zbyv_cas = (cas / cislo_radku) * (pocet_radku - cislo_radku)
    print("zbývající čas:", zbyv_cas, "min")
    print()

    jdi_na()
    paper = paper - (zmena_radek)
    M_papir.run_target(60, paper)

# posune vozikem o jednu jednotku
def carka(move, fast = False):
    global dal
    dal = dal - (zmena_carka * move)
    if fast == True:
        M_vozik.run_target(200, dal) # DOLADIT !!!!!!!
    elif fast == False:
        M_vozik.run_target(100, dal) # DOLADIT !!!!!!!
    else:
        print("Error, už zase? Jinak, máš problém s rychlopohybem, a tím, co do něj posíláš (fast)")
# main loop
def Print_Color(color):
    global cerna 
    for e in color:
        if e == -1:
            push_up()
            NRadek()
            cerna = False
            continue
        if e == sirka:
            push_up()
            NRadek()
            cerna = False
            continue
        
        if cerna == True:
            push_down()
        else:
            #cerna == False:
            push_up()
        if cerna == False and e > 10:
            carka(e, True)
        else:
            carka(e, False)
        cerna = not cerna

        
# udělá nový řádek
def NDRadek():
    global paper
    global zmena_radek
    # global dal
    # global cislo_radku
    dal = set_dal
    push_up()
    #push_up()
    # cislo_radku = cislo_radku + 1
    #M_pero.run_target(100, 0)
    # print("odseknuto", end = "\r")
    # jdi_na()
    paper = paper - (zmena_radek)
    M_papir.run_target(60, paper)


# paper = 0
push_up()
# aby se uvolnil M_paper
for a in range(10):
    NDRadek()
# cislo_radku = 0
# start všeho
stop_w = StopWatch()
cislo_radku = 0
paper = 0
M_papir.reset_angle(0)

M_pero.run_target(200, 20)
jdi_na()

# tisk
Print_Color(robot)
print("DONE")
push_up()


# po dokončení píp
tempo = 120
while True:
    ev3.speaker.beep(frequency=587.33, duration=1 * tempo)
    ev3.speaker.beep(frequency=587.33, duration=1 * tempo)
    ev3.speaker.beep(frequency=1174.66, duration=2 * tempo)
    ev3.speaker.beep(frequency=880, duration=2 * tempo)
    wait(1 * tempo)
    ev3.speaker.beep(frequency=830.61, duration=1 * tempo)
    wait(1 * tempo)
    ev3.speaker.beep(frequency=783.99, duration=1 * tempo)
    wait(1 * tempo)
    ev3.speaker.beep(frequency=698.46, duration=2 * tempo)
    ev3.speaker.beep(frequency=587.33, duration=1 * tempo)
    ev3.speaker.beep(frequency=698.46, duration=1 * tempo)
    ev3.speaker.beep(frequency=783.99, duration=1 * tempo)

    ev3.speaker.beep(frequency=523.25, duration=1 * tempo)
    ev3.speaker.beep(frequency=523.25, duration=1 * tempo)
    ev3.speaker.beep(frequency=1174.66, duration=2 * tempo)
    ev3.speaker.beep(frequency=880, duration=2 * tempo)
    wait(1 * tempo)
    ev3.speaker.beep(frequency=830.61, duration=1 * tempo)
    wait(1 * tempo)
    ev3.speaker.beep(frequency=783.99, duration=1 * tempo)
    wait(1 * tempo)
    ev3.speaker.beep(frequency=698.46, duration=2 * tempo)
    ev3.speaker.beep(frequency=587.33, duration=1 * tempo)
    ev3.speaker.beep(frequency=698.46, duration=1 * tempo)
    ev3.speaker.beep(frequency=783.99, duration=1 * tempo)

    ev3.speaker.beep(frequency=493.88, duration=1 * tempo)
    ev3.speaker.beep(frequency=493.88, duration=1 * tempo)
    ev3.speaker.beep(frequency=1174.66, duration=2 * tempo)
    ev3.speaker.beep(frequency=880, duration=2 * tempo)
    wait(1 * tempo)
    ev3.speaker.beep(frequency=830.61, duration=1 * tempo)
    wait(1 * tempo)
    ev3.speaker.beep(frequency=783.99, duration=1 * tempo)
    wait(1 * tempo)
    ev3.speaker.beep(frequency=698.46, duration=2 * tempo)
    ev3.speaker.beep(frequency=587.33, duration=1 * tempo)
    ev3.speaker.beep(frequency=698.46, duration=1 * tempo)
    ev3.speaker.beep(frequency=783.99, duration=1 * tempo)

    ev3.speaker.beep(frequency=466.16, duration=1 * tempo)
    ev3.speaker.beep(frequency=466.16, duration=1 * tempo)
    ev3.speaker.beep(frequency=1174.66, duration=2 * tempo)
    ev3.speaker.beep(frequency=880, duration=2 * tempo)
    wait(1 * tempo)
    ev3.speaker.beep(frequency=830.61, duration=1 * tempo)
    wait(1 * tempo)
    ev3.speaker.beep(frequency=783.99, duration=1 * tempo)
    wait(1 * tempo)
    ev3.speaker.beep(frequency=698.46, duration=2 * tempo)
    ev3.speaker.beep(frequency=587.33, duration=1 * tempo)
    ev3.speaker.beep(frequency=698.46, duration=1 * tempo)
    ev3.speaker.beep(frequency=783.99, duration=1 * tempo)