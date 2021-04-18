from GameBoard import *


class SeaBattle:
    def __init__(self):
        self.human_board = HumanBoard()
        self.comp_board = CompBoard()
        pass

    def start(self):
        print("Let's greatest Sea Battle begin!!!")
        print("Ваше игровое поле слева, поле компьютера -  справа.")
        print("Чтобы сделать выстрел, необходимо ввести координаты х и у поражаемой точки через пробел.")
        print("Каждая координата должна быть числом от 1 до 6.")
        print("Удачи!")
        print()

    def showBoards(self):
        for line_1, line_2 in zip(self.human_board, self.comp_board):
            print(f"{line_1}   |   {line_2}")
        print()

    def makeMove(self):
        ok = False
        while (not ok):
            try:
                xy = list(map(int, input("Введите х и у координаты точки выстрела через пробел: ").split(" ")))
                xy = list(filter(lambda z: 1 <= z <= 6, xy))
                if (len(xy) < 2):
                    raise IndexError
                result = self.comp_board.shot(xy)
                print(result[1])
                if result[0]:
                    self.showBoards()
                    if self.comp_board.areAllShipsKilled():
                        return
                    continue
            except ValueError:
                print("Каждая координата должна быть числом! Повторите выстрел.")
            except IndexError:
                print("Каждая координата должна быть числом от 1 до 6! Повторите выстрел.")
            except BoardError:
                print("Нельзя дважды стрелять в одну и ту же точку! Повторите выстрел...")
            else:
                ok = True
        ########
        while True:
            result = self.human_board.shot(None)
            print(result[1])
            if not result[0]:
                break

    def isEnd(self):
        if self.human_board.areAllShipsKilled():
            self.showBoards()
            print("Вы проиграли !!!")
            return True
        if self.comp_board.areAllShipsKilled():
            self.showBoards()
            print("Я проиграл ...")
            return True
        return False

    def play(self):
        self.showBoards()
        self.makeMove()
        return not self.isEnd()
