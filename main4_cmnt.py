
def check():
    global lft
    global rgh
    global mid
    
    global lft_fwd
    global rgh_fwd
    global mid_fwd

    mid = rd_mid()

    print(bila(lft_fwd), bila(mid_fwd), bila(rgh_fwd), lft_fwd, mid_fwd, rgh_fwd)
    print(bila(lft), bila(mid), bila(rgh), lft, mid, rgh)
    print(memory)
    print()

    if bila(lft) == False and bila(mid) == False and bila(rgh) == True:
        read_fwd()
        if bila(lft_fwd) == True and bila(mid_fwd) == True and bila(rgh_fwd) == True:
            print("L")
            # memory.append("L")
            make_left()
            updt_memory()
            rd_all()
        if bila(lft_fwd) == True and bila(mid_fwd) == False and bila(rgh_fwd) == True:
            print("J")
            memory.append("L")
            make_left()
            updt_memory()
            rd_all()

    if bila(lft) == True and bila(mid) == False and bila(rgh) == False:
        read_fwd()
        if bila(lft_fwd) == True and bila(mid_fwd) == True and bila(rgh_fwd) == True:
            print("R")
            # memory.append("L")
            make_right()
            updt_memory()
            rd_all()
        if bila(lft_fwd) == True and bila(mid_fwd) == False and bila(rgh_fwd) == True:
            print("K")
            memory.append("S")
            make_strght()
            updt_memory()
            rd_all()

    if bila(lft) == False and bila(mid) == False and bila(rgh) == False:
        read_fwd()
        if bila(lft_fwd) == True and bila(mid_fwd) == True and bila(rgh_fwd) == True:
            print("T")
            memory.append("L")
            make_left()
            updt_memory()
            rd_all()
        if bila(lft_fwd) == True and bila(mid_fwd) == False and bila(rgh_fwd) == True:
            print("+")
            memory.append("L")
            make_left()
            updt_memory()
            rd_all()
        if bila(lft_fwd) == False and bila(mid_fwd) == False and bila(rgh_fwd) == False:
            print("FINISH")
            # memory.append("F")
            return "out"

    if bila(lft)== True and bila(mid) == True and bila(rgh) == True:
        read_fwd()
        if bila(lft_fwd)== True and bila(mid_fwd) == True and bila(rgh_fwd) == True:
            print("U")
            memory.append("U")
            make_Uturn()
            updt_memory()
            rd_all()


def bila(inp):
    global thresh_up
    global thresh_dwn

    if inp > thresh_up:
        return True
    elif inp < thresh_dwn:
        return False
    else:
        return None
p = 0.2
base_angle = 10
targ = 8
trn = 40

thresh_up = 14
thresh_dwn = 11

memory = []

lft = rd_lft()
mid = rd_mid()
rgh = rd_rgh()


read_fwd()

while True:
    lft = rd_lft()
    # line()
    # if check() == "out":
    #     break

    rgh = rd_rgh()
    line()
    if check() == "out":
        break

# waiting to start second pass through maze
while True:
    if toch.pressed() == True:
        pt.wait(100)
        break


# add execute found path
ev3.light.on(Color.RED)
lft = rd_lft()
mid = rd_mid()
rgh = rd_rgh()


read_fwd()

def check_solved():
    global lft
    global rgh
    global mid
    
    global lft_fwd
    global rgh_fwd
    global mid_fwd

    global indx
    
    mid = rd_mid()

    print(bila(lft_fwd), bila(mid_fwd), bila(rgh_fwd), lft_fwd, mid_fwd, rgh_fwd)
    print(bila(lft), bila(mid), bila(rgh), lft, mid, rgh)
    print(memory)
    print()


    if bila(lft) == False and bila(mid) == False and bila(rgh) == True:
        read_fwd()
        if bila(lft_fwd) == True and bila(mid_fwd) == True and bila(rgh_fwd) == True:
            print("L")
            make_left()
            rd_all()
        if bila(lft_fwd) == True and bila(mid_fwd) == False and bila(rgh_fwd) == True:
            print("J")
            make_turn()
            rd_all()

    if bila(lft) == True and bila(mid) == False and bila(rgh) == False:
        read_fwd()
        if bila(lft_fwd) == True and bila(mid_fwd) == True and bila(rgh_fwd) == True:
            print("R")
            make_right()
            rd_all()
        if bila(lft_fwd) == True and bila(mid_fwd) == False and bila(rgh_fwd) == True:
            print("K")
            make_turn()
            rd_all()

    if bila(lft) == False and bila(mid) == False and bila(rgh) == False:
        read_fwd()
        if bila(lft_fwd) == True and bila(mid_fwd) == True and bila(rgh_fwd) == True:
            print("T")
            make_turn()
            rd_all()
        if bila(lft_fwd) == True and bila(mid_fwd) == False and bila(rgh_fwd) == True:
            print("+")
            make_turn()
            rd_all()
        if bila(lft_fwd) == False and bila(mid_fwd) == False and bila(rgh_fwd) == False:
            print("FINISH")
            return "out"

def make_turn():
    global indx
    global memory

    try:
        if memory[indx] == "L":
            print("L")
            make_left()
        elif memory[indx] == "S":
            make_strght()
            print("S")
        elif memory[indx] == "R":
            make_right()
            print("R")
        indx += 1
    except:
        pass


indx = 0

while True:
    lft = rd_lft()
    line()
    if check_solved() == "out":
        break

    rgh = rd_rgh()
    line()
    if check_solved() == "out":
        break

