memory = "SLULUSLLUSLULLUSULLL"

strung = ""

for x in memory:
    strung += x

print(strung)

strung_start = None

while strung_start != strung:
    strung_start = strung
    strung = strung.replace("LUL", "S")
    strung = strung.replace("LUS", "R")
    strung = strung.replace("SUL", "R")
    strung = strung.replace("RUL", "U")
    strung = strung.replace("SUS", "U")

print(strung)