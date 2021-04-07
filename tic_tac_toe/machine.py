player = 'X'
comp   = 'O'
empty  = '-'
field  = [[empty, empty, empty], [empty, empty, empty], [empty, empty, empty]]


def check_row(who, i):
    #print("check_row({0})".format(i))
    sum = 0
    for j in range(3):
        if field[i][j] == who:
            sum += 1
    return sum

def fill_row(i):
    #print("fill_row({0})".format(i))
    for j in range(3):
        if field[i][j] == empty:
            field[i][j] = comp
            return True
    return False

def check_col(who, i):
    #print("check_col({0})".format(i))
    sum = 0
    for j in range(3):
        if field[j][i] == who:
            sum += 1
    return sum

def fill_col(i):
    #print("fill_col({0})".format(i))
    for j in range(3):
        if field[j][i] == empty:
            field[j][i] = comp
            return True
    return False

def check_diag(who, i):
    #print("check_diag({0})".format(i))
    sum = 0
    if i == 0:
        for j in range(3):
            if field[j][j] == who:
                sum += 1
    else:
        for j in range(3):
            if field[2 - j][j] == who:
                sum += 1
    return sum

def fill_diag(i):
    #print("fill_diag({0})".format(i))
    if i == 0:
        for j in range(3):
            if field[j][j] == empty:
                field[j][j] = comp
                return True
    else:
        for j in range(3):
            if field[2 - j][j] == empty:
                field[2 - j][j] = comp
                return True
    return False


def check_next_move_win(who):
    for i in range(2):
        if check_diag(who, i) == 2:
            if fill_diag(i):
                return True
    for i in range(3):
        if check_row(who, i) == 2:
            if fill_row(i):
                return True
    for i in range(3):
        if check_col(who, i) == 2:
            if fill_col(i):
                return True
    return False

def move_into_corner():
    if field[0][0] == empty:
        field[0][0] = comp
        return
    if field[0][2] == empty:
        field[0][2] = comp
        return
    if field[2][0] == empty:
        field[2][0] = comp
        return
    if field[2][2] == empty:
        field[2][2] = comp
        return
    for i in range(3):
        for j in range(3):
            if field[i][j] == empty:
                field[i][j] = comp
                return

def move(y, x):
    if check_next_move_win(comp):
        return
    if check_next_move_win(player):
        return
    # -----------------
    move_into_corner()
    # -----------------
    return