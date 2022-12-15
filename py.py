strung = "SLUUSRLSRRLUSRULRLL"
for x in strung:
    strung += x
    strung_start = strung
    strung = strung.replace("LUL", "S")
    strung = strung.replace("LUS", "R")
    strung = strung.replace("SUL", "R")
    strung = strung.replace("RUL", "U")
    strung = strung.replace("UU", "")
print(strung)
