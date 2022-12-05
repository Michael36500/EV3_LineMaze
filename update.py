pole = ['S', 'L', 'U', 'L', 'L', 'U', 'S', 'U', 'L', 'S', 'L', 'L']
memory = []
str = ""

for x in pole:
    str += x
print(str)
str_start = None
while str_start != str:
    str_start = str
    str = str.replace("LUL", "S")
    str = str.replace("LUS", "R")
    str = str.replace("SUL", "R")
    str = str.replace("RUL", "U")
    str = str.replace("SUS", "U")


print(str)