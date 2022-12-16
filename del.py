def load_and_print():
    file = open("mapa2.txt", "r", encoding="utf8")

    file = file.readlines()
    blud = []
    for x in file:
        x = x[:-1]
        temp = []
        for y in x:
            temp.append(y)
        blud.append(temp)
    # for x in blud:
    #     print(x)
    return blud
def posun_na_dalsi_kriz():
    global pozice, wturn
    global blud


    dx, dy = 0, 0
    if wturn == 0:
        if not blud[pozice[0] - rozdil[0]][pozice[1] - rozdil[1]] in "┘ └ ├ ┤ ┴ ┼ ▫":
            raise Exception("nemůžu nahoru, chyba")
        dx = -1

    elif wturn == 1:
        if not blud[pozice[0] - rozdil[0]][pozice[1] - rozdil[1]] in "└ ┌ ├ ┬ ┴ ┼ ▫":
            raise Exception("nemůžu doprava, chyba")
        dy = 1

    elif wturn == 2:
        if not blud[pozice[0] - rozdil[0]][pozice[1] - rozdil[1]] in "┐ ┌ ┤ ├ ┬ ┼ ▫":
            raise Exception("nemůžu dolů, chyba")
        dx = 1

    elif wturn == 3:
        if not blud[pozice[0] - rozdil[0]][pozice[1] - rozdil[1]] in "┘ ┐ ┤ ┬ ┴ ┼ ▫":
            raise Exception("nemůžu doleva, chyba")
        dy = -1

    while True:
        pozice[0] += dx
        pozice[1] += dy

        # print(pozice)

        if wturn == 0 or wturn == 2:
            if blud[pozice[0] - rozdil[0]][pozice[1] - rozdil[1]] != "│":
                break
        if wturn == 1 or wturn == 3:
            if blud[pozice[0] - rozdil[0]][pozice[1] - rozdil[1]] != "─":
                break
def check():
    global blud

    # !!!!!!!!!!!PŘIDAT ODROTOVÁNÍ

    krizovatka = blud[pozice[0] - rozdil[0]][pozice[1] - rozdil[1]]

    x =  make_decision(krizovatka)
    try:
        posun_na_dalsi_kriz()
    except:
        return x
    
def make_decision(kriz):
    global pozice, wturn
    global planek
    global debug

    if kriz == "▫":
        # make_Uturn()
        # updt_kola()
        wturn = (wturn + 2) % 4 # opačný směr
    elif kriz == "■":
        print("finish")
        return "out"
    else:
        # když jsem tam nebyl, tak si vložit políčko do planek
        policsto = planek[pozice[0]][pozice[1]]
        if policsto.je_prazdny():
            policsto.nastav_podle_krizovatky(kriz)

        # zapsat směr příjezdu (odkud jsem přijel)
        policsto.prijezd(wturn)

        # vyhodnotím směr odjezdu
            # zjistím kam
        for x in planek:
            for y in x:
                print(y.print_all(), end="")
            print()
            # updt wturn
        print()

        x = policsto.get_smer()
        wturn = x
        
        # zapsat směr odjezdu
            # updt_kola()
        policsto.odjezd(wturn)

        # další křižovatka (neboli vyskočím do checku a pokračuji)

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
    def get_smer(self):
        global wturn
        lst = [self.nahoru, self.doprava, self.dolu, self.doleva]
        for x in range(len(lst)):
            if lst[x] == -1:
                lst[x] = 3

        # print(lst)
        
            

        if str(lst).count("1") == 1:
            minim = 3
            for x in range(len(lst)):
                if lst[x] < minim: # type: ignore
                    minim = lst[x]
                    moznosti = []
                    moznosti.append(x)
            if len(moznosti) == 1:     # type: ignore
                return moznosti[0]   # type: ignore

            rnd = random.randint(0, len(moznosti)) - 1   # type: ignore
            return moznosti[rnd]   # type: ignore

        elif lst[wturn] != 2:
            kam = (wturn + 2) % 4
            return kam

        else:
            minim = 3
            for x in range(len(lst)):
                if lst[x] < minim: # type: ignore
                    minim = lst[x]
                    moznosti = []
                    moznosti.append(x)
            return moznosti[random.randint(0, len(moznosti)) - 1]  # type: ignore

import time
import random

escribo = open("out.txt", "a")
random.seed(34)

blud = load_and_print()

planek = []
for _ in range(15):
    temp = []
    for _ in range(15):
        temp.append(policko())
    planek.append(temp)

pozice = [7,8]
start = [5,0] # musím být na křižovatce
rozdil = [pozice[0] - start[0], pozice[1] - start[1]]

wturn = 0

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

# for x in planek:
    # print(x)

# memory = []




ext = True
while ext:
    # time.sleep(0.02)
    if check() == "out":
        ext = False

for x in planek:
    for y in x:
        escribo.write(y.print_all())
    escribo.write("\n")
escribo.write("\n\n\n")