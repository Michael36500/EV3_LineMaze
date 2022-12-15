def load_and_print():
    file = open("mapa.txt", "r", encoding="utf8")

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

blud = load_and_print()


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
        exit()
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

        if False:
            while True:
                inp = input()
                if str(inp) in "0123":
                    break
            wturn = int(inp)
        else:
            x = policsto.get_smer()
            debug.append(x)
            # print(debug)
            wturn = x
        
        # zapsat směr odjezdu
            # updt_kola()
        policsto.odjezd(wturn)

        # další křižovatka (neboli vyskočím do checku a pokračuji)








def check():
    global blud

    # !!!!!!!!!!!PŘIDAT ODROTOVÁNÍ

    krizovatka = blud[pozice[0] - rozdil[0]][pozice[1] - rozdil[1]]

    make_decision(krizovatka)
    
    posun_na_dalsi_kriz()

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
        lst = [self.nahoru, self.doprava, self.dolu, self.doleva]
        # print(lst)
        for x in range(len(lst)):
            if lst[x] == -1:
                lst[x] = 3
        kam = lst.index(min(lst)) # type: ignore
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



pozice = [4,3]
start = [4,3]
rozdil = [pozice[0] - start[0], pozice[1] - start[1]]
print(rozdil)
debug = []
wturn = 1

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

planek = []
for _ in range(16):
    temp = []
    for _ in range(16):
        temp.append(policko())
    planek.append(temp)
# for x in planek:
    # print(x)

# memory = []
import time
while True:
    time.sleep(0.)
    ## posun()
    if check() == "out":
        break
    # break
