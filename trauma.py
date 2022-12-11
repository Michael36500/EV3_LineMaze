def get_smer():
    lst = [-1,0,1,2]
    for x in range(len(lst)):
        if lst[x] == -1:
            lst[x] = 3
    kam = lst.index(min(lst))
    return kam

print(get_smer())
