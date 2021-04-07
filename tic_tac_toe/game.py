from machine import *

def print_field():
    print("  0 1 2")
    for i in range(3):
        print("{0} {1} {2} {3}".format(i, field[i][0], field[i][1], field[i][2]))


def is_win(who):
    for i in range(3):
        if check_row(who, i) == 3:
            return True
    for i in range(3):
        if check_col(who, i) == 3:
            return True
    for i in range(2):
        if check_diag(who, i) == 3:
            return True
    return False

def is_dead_heat():
    for i in range(3):
        for j in range(3):
            if field[i][j] == empty:
                return False
    return True

def play():
    while (True):
        print("Ваш ход:")
        while (True):
            y = int(input("  введите номер строки (0...2): "))
            if 0 <= y <= 2: break
        while (True):
            x = int(input("  введите номер столбца (0...2): "))
            if 0 <= x <= 2: break
        if field[y][x] == empty:
            field[y][x] = player
        else:
            print("Поле ({0}, {1}) уже занято! Давайте ещё раз...".format(y, x))
            continue
        move(y, x)
        print_field()
        if is_win(player):
            print("Вы выиграли!")
            break
        if is_win(comp):
            print("Вы проиграли!")
            break
        if is_dead_heat():
            print("Ничья, однако...")
            break
    input("Нажмите Ввод для заверщения игры")
