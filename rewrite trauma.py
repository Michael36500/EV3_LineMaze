#!/usr/bin/env pybricks-micropython
import pybricks.tools as pt
from pybricks.ev3devices import ColorSensor, Motor, TouchSensor  # type: ignore
from pybricks.hubs import EV3Brick
from pybricks.parameters import Color, Direction, Port
from pybricks.robotics import DriveBase

# kostka
ev3 = EV3Brick()    

# motory
levy_motor = Motor(Port.C, positive_direction=Direction.COUNTERCLOCKWISE, gears=[12,20])
pravy_motor = Motor(Port.D, positive_direction=Direction.COUNTERCLOCKWISE, gears=[12,20])

# senzory
color_levy = ColorSensor(Port.S1)
color_uprostred = ColorSensor(Port.S2)
color_vpravo = ColorSensor(Port.S3)

color_navigacni = ColorSensor(Port.S4)

# drivebase
robot = DriveBase(levy_motor, pravy_motor, 57, 226)

def sleduj_caru():
    global cilova_hodnota_sledovani_cary, konstanta_p, zakladni_rychlost_pro_PID, cl_navigacni
    # P formula
    cl_navigacni = color_navigacni.reflection()
    error_vuci_chtenemu = cl_navigacni - cilova_hodnota_sledovani_cary
    jak_moc_se_otocit = konstanta_p * error_vuci_chtenemu
    # vykonej
    robot.drive(zakladni_rychlost_pro_PID, jak_moc_se_otocit)  # type: ignore
def jsem_v_cili():
    # ev3.speaker.set_volume(100)
    ev3.speaker.play_file("rickroll.mp3")
    pt.wait(10)

def otoc_uturn():
    print("Uturn")
    ## vylaď
    robot.turn(182)
def otoc_doprava():
    print("right")
    ## vylaď
    robot.straight(20)
    robot.turn(92)
def otoc_doleva():
    print("left")
    ## vylaď
    robot.straight(20)
    robot.turn(-92)
def otoc_dopredu():
    # pro přeskakování rovných křižovatek
    print("strght")
    robot.straight(30)

def precti_senzory_s_posunem():
    global cl_vlevo_vepredu, cl_vpravo_vepredu, cl_vprostred_vepredu
    print("čtu vepředu")
    ## vylaď
    robot.straight(30)

    cl_vlevo_vepredu = color_levy.reflection()
    cl_vprostred_vepredu = color_uprostred.reflection()
    cl_vpravo_vepredu = color_vpravo.reflection()
def je_to_bila(vstupni_hodnota):
    global threshold_pro_bilou, threshold_pro_cernou

    if vstupni_hodnota > threshold_pro_bilou: return True
    elif vstupni_hodnota < threshold_pro_cernou: return False
    else: return None
def precti_senzory_pod_sebou():
    global cl_vlevo
    global cl_vpravo
    global cl_uprostred

    cl_vlevo = color_levy.reflection()
    cl_uprostred = color_uprostred.reflection()
    cl_vpravo = color_vpravo.reflection()
def print_debugovaci_vecicky():
    global cl_vlevo, cl_vpravo, cl_uprostred, cl_navigacni    
    global cl_vlevo_vepredu, cl_vpravo_vepredu, cl_vprostred_vepredu
    global pozice_x_y, otoceni_vuci_startu

    if True:
        print(je_to_bila(cl_vlevo_vepredu), je_to_bila(cl_vprostred_vepredu), je_to_bila(cl_vpravo_vepredu), cl_vlevo_vepredu, cl_vprostred_vepredu, cl_vpravo_vepredu, "vepředu")
        print(je_to_bila(cl_vlevo), je_to_bila(cl_uprostred), je_to_bila(cl_vpravo), cl_vlevo, cl_uprostred, cl_vpravo, "u sebe")
        print(cl_navigacni, "navigační")
        print(pozice_x_y, "pozice", otoceni_vuci_startu, "wturn")
        print()

def make_decision(vstupni_krizovatka):
    global pozice_x_y, otoceni_vuci_startu
    global planek_pro_treumax

    # pokud je křižovatka uturn, tak:
    if vstupni_krizovatka == "▫":
        updatuj_pozici_a_rotaci()
        print("našel jsem uturn")
        # získá políčko
        aktualnI_zpracovavane_policko = planek_pro_treumax[int(pozice_x_y[0])][int(pozice_x_y[1])]
        # když je prázdné, tak  nastaví
        if aktualnI_zpracovavane_policko.je_prazdny():
            aktualnI_zpracovavane_policko.nastav_podle_krizovatky(vstupni_krizovatka)
        # nastaví i po příjezdu
        aktualnI_zpracovavane_policko.prijezd(otoceni_vuci_startu)
        # otočí se, a jede pryč
        otoc_uturn()
        # a ještě updatuje pozici a políčko při odjezdu
        updatuj_pozici_a_rotaci()
        aktualnI_zpracovavane_policko.odjezd(otoceni_vuci_startu)

    # pokud jsem v cílu
    elif vstupni_krizovatka == "■":
        print("finish")
        jsem_v_cili()
    else:
        updatuj_pozici_a_rotaci() 
        aktualnI_zpracovavane_policko = planek_pro_treumax[int(pozice_x_y[0])][int(pozice_x_y[1])]
        if aktualnI_zpracovavane_policko.je_prazdny():
            aktualnI_zpracovavane_policko.nastav_podle_krizovatky(vstupni_krizovatka)

        aktualnI_zpracovavane_policko.prijezd(otoceni_vuci_startu)

        x = aktualnI_zpracovavane_policko.get_smer()
        print(x)

        rozdil_chteneho_smeru_vuci_rotaci_irl = ((x - otoceni_vuci_startu) + 4) % 4
        print(rozdil_chteneho_smeru_vuci_rotaci_irl, "rozdil")
        if rozdil_chteneho_smeru_vuci_rotaci_irl == 0:
            otoc_dopredu()
        elif rozdil_chteneho_smeru_vuci_rotaci_irl == 1:
            otoc_doprava()
        elif rozdil_chteneho_smeru_vuci_rotaci_irl == 2:
            otoc_uturn()
        elif rozdil_chteneho_smeru_vuci_rotaci_irl == 3:
            otoc_doleva()
        else:
            print("užij si debugování")


        updatuj_pozici_a_rotaci()
        # zapsat směr odjezdu
        aktualnI_zpracovavane_policko.odjezd(otoceni_vuci_startu)

        # další křižovatka (neboli vyskočím do checku a pokračuji)
def poznej_na_jake_krizovatce_jsem(vstupni_pole, smer_otoceni_robota):
    slovnik_krizovatek = {
    "TFT TFF" : ["├", "┬", "┤", "┴"],
    "TTT TFF" : ["┌", "┐", "┘", "└"],
    "TTT TTT" : ["▫", "▫", "▫", "▫"],
    "TTT FFF" : ["┬", "┤", "┴", "├"],
    "FFF FFF" : ["■", "■", "■", "■"],
    "TFT FFF" : ["┼", "┼", "┼", "┼"],
    "TFT FFT" : ["┤", "┴", "├", "┬"],
    "TTT FFT" : ["┐", "┘", "└", "┌"]
    }
    
    klic_k_slovniku = ""
    for x in vstupni_pole:
        for y in x:
            if y == True: klic_k_slovniku += "T"
            if y == None: klic_k_slovniku += "F"
            if y ==False: klic_k_slovniku += "F"
        klic_k_slovniku += " "
    klic_k_slovniku = klic_k_slovniku[: -1]
    print(klic_k_slovniku)
    
    print(vstupni_pole,smer_otoceni_robota)
    return slovnik_krizovatek[klic_k_slovniku][int(smer_otoceni_robota)]


def check():
    global cl_vlevo, cl_vpravo, cl_uprostred
    global cl_vlevo_vepredu, cl_vpravo_vepredu, cl_vprostred_vepredu, cl_navigacni
    global co100_cislo_tisknu_pebug
    global pozice_x_y, otoceni_vuci_startu


    co100_cislo_tisknu_pebug += 1

    if co100_cislo_tisknu_pebug % 100 == 0:
        print_debugovaci_vecicky()
    if not(je_to_bila(cl_vlevo) != False and je_to_bila(cl_uprostred) != True and je_to_bila(cl_vpravo) != False):
        robot.stop()
        precti_senzory_pod_sebou()
        precti_senzory_s_posunem()
        print_debugovaci_vecicky()
        pole_s_hodnotami_pred_robotem = [
            [je_to_bila(cl_vlevo_vepredu), je_to_bila(cl_vprostred_vepredu), je_to_bila(cl_vpravo_vepredu)],
            [je_to_bila(cl_vlevo), je_to_bila(cl_uprostred), je_to_bila(cl_vpravo)]]

        kriz = poznej_na_jake_krizovatce_jsem(pole_s_hodnotami_pred_robotem, otoceni_vuci_startu)
        make_decision(kriz)



def updatuj_pozici_a_rotaci():
    global pozice_x_y, otoceni_vuci_startu

    policek_se_posunul = round(robot.distance() / 150, 0)
    otoceni_vuci_minulemu_startu = (round(robot.angle() / 90, 0) + otoceni_vuci_startu) % 4
    robot.reset()
    otoceni_vuci_startu = otoceni_vuci_minulemu_startu

    if otoceni_vuci_minulemu_startu == 0:
        pozice_x_y[0] -= policek_se_posunul  # type: ignore
    elif otoceni_vuci_minulemu_startu == 1:
        pozice_x_y[1] += policek_se_posunul  # type: ignore
    elif otoceni_vuci_minulemu_startu == 2:
        pozice_x_y[0] += policek_se_posunul  # type: ignore
    elif otoceni_vuci_minulemu_startu == 3:
        pozice_x_y[1] -= policek_se_posunul  # type: ignore
    else:
        print("MOTHERFUCKER!!!!")

    print(policek_se_posunul, "posun")
    print(otoceni_vuci_minulemu_startu, "otoceni")
    print(otoceni_vuci_startu, "wturn")

class policko():
    # None - nevíme, -1 - cesta není, 0 cesta je, neprošli, 1 - c je, jednou p, 2 - cesta je, prošli 2 krát
    def __init__(self):
        self.nahoru = None
        self.doprava = None
        self.doleva = None
        self.dolu = None

    def je_prazdny(self):
        if self.nahoru == None and self.doprava == None and self.dolu == None and self.doleva == None:
            return True
        else:
            return False
    
    def nastav_podle_krizovatky(self, krizov):
        global moznosti_krizovatky

        moznosti = moznosti_krizovatky.get(krizov) # type: ignore
        print(moznosti, krizov)

        self.nahoru = moznosti[0]     # type: ignore
        self.doprava = moznosti[1]    # type: ignore
        self.dolu = moznosti[2]     # type: ignore
        self.doleva = moznosti[3]       # type: ignore

        strung = str([self.nahoru, self.doprava, self.dolu, self.doleva]) # type: ignore
        print(strung)

    def prijezd(self, smer):
        if smer == 0: self.dolu += 1          # type: ignore
        if smer == 1: self.doleva += 1        # type: ignore  
        if smer == 2: self.nahoru += 1        # type: ignore
        if smer == 3: self.doprava += 1       # type: ignore
## odřřádkování
    def odjezd(self, smer):
        if smer == 0: self.nahoru += 1      # type: ignore
        if smer == 1: self.doprava += 1     # type: ignore  
        if smer == 2: self.dolu += 1        # type: ignore
        if smer == 3: self.doleva += 1      # type: ignore

    def print_all(self):
        strung = str([self.nahoru, self.doprava, self.dolu, self.doleva]) # type: ignore
        strung = strung.replace("None", ".")
        strung = strung.replace("[", "")
        strung = strung.replace("]", "")
        strung = strung.replace("-1", "X")
        strung = strung.replace(",", "")
        strung = strung.replace(" ", "")
        strung += " "
        return strung

    def get_smer(self):
        print("\n")
        lst = [self.nahoru, self.doprava, self.dolu, self.doleva]
        print(lst)
        for x in range(len(lst)):
            if lst[x] == -1:
                lst[x] = 3
        kam = lst.index(min(lst)) # type: ignore
        print(kam)
        print("\n")
        return kam
        
        
    def gnahoru(self):
        return self.nahoru
    def gdoprava(self):
        return self.doprava
    def gdoleva(self):
        return self.doleva
    def gdolu(self):
        return self.dolu
    

    def nnahoru(self, x):
        self.nahoru = x
    def ndoprava(self, x):
        self.doprava = x
    def ndolu(self, x):
        self.dolu = x
    def ndoleva(self, x):
        self.doleva = x



pozice_x_y = [16,16]
otoceni_vuci_startu = 0

cis = 0
najeto_na_kolech = []
najeto_na_kolech2 = []

konstanta_p = 2.5
zakladni_rychlost_pro_PID = 75

threshold_pro_bilou = 26
threshold_pro_cernou =  16
cilova_hodnota_sledovani_cary = 12

co100_cislo_tisknu_pebug = 0
cl_navigacni = color_navigacni.reflection()

moznosti_krizovatky = {
    "┌" : [-1, 0, 0,-1],
    "┐" : [-1,-1, 0, 0],
    "┘" : [ 0,-1,-1, 0],
    "└" : [ 0, 0,-1,-1],
    "├" : [ 0, 0, 0,-1],
    "┤" : [ 0,-1, 0, 0],
    "┬" : [-1, 0, 0, 0],
    "┴" : [ 0, 0,-1, 0],
    "┼" : [ 0, 0, 0, 0],
    "▫" : [ 0, 0, 0, 0]
}

print("making planek")
planek_pro_treumax = []
for _ in range(32):
    temp = []
    for _ in range(32):
        temp.append(policko())
    planek_pro_treumax.append(temp)

# precise position
ev3.light.off()
while cl_navigacni != cilova_hodnota_sledovani_cary:
    if cl_navigacni > cilova_hodnota_sledovani_cary:
        ev3.light.on(Color.RED)
    if cl_navigacni < cilova_hodnota_sledovani_cary:
        ev3.light.on(Color.ORANGE)
    cl_navigacni = color_navigacni.reflection()
ev3.light.on(Color.GREEN)
robot.reset()
pt.wait(500)



precti_senzory_pod_sebou()
precti_senzory_s_posunem()

while True:
    precti_senzory_pod_sebou()
    sleduj_caru()
    if check() == "out":
        break


