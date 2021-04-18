from abc import ABCMeta, abstractmethod
from Comp import Comp
from Dot import Dot
from Ship import Ship
import random


class BoardError(Exception): pass


class Board(metaclass=ABCMeta):
    __size = 6

    def __init__(self):
        self.dots = []
        self.ships = []
        self.iniShips()
        self.line_counter = 0

    def clearDots(self):
        self.dots.clear()
        for y in range(self.__size):
            for x in range(self.__size):
                self.dots.append(Dot(x, y))

    def iniShips(self):
        while True:
            ok = False
            self.clearDots()
            self.ships.clear()
            for i in range(7):
                ship = Ship(i)
                if not self.insertShip(ship):
                    break
                self.ships.append(ship)
            else:
                ok = True
            if ok:
                break

    def insertShip(self, ship):
        count = 0
        while True:
            count += 1
            if count > 100:
                return False
            # координаты начала, v == 1 вертикально, u == 1 вверх if v == 1 else вправо
            x = random.randint(0, self.__size - 1)
            y = random.randint(0, self.__size - 1)
            v = random.randint(0, 1)
            u = random.randint(0, 1)
            # генерим координаты по x, y, v, u для всех точек корабля в зависимости от его размера
            position = []
            for i in range(ship.size):
                xy = [x if v else x + (i if u else -i), y if not v else y + (i  if u else -i)]
                position.append(xy)
                del xy
            # вышли ли координаты за границы поля или зяняты другим кораблём или его контуром?
            ok = True
            for xy in position:
                if not self.check(xy):
                    ok = False
            if not ok:
                continue
            # ставим корабль на поле
            for x, y in position:
                self.dots[x + y * self.__size].cleared = False
                self.dots[x + y * self.__size].shipped = True
            self.contour(position)  # отмечаем контур корабля
            # запоминаем в корабле его координаты
            ship.position(position)
            # корабль успешно поставлен на поле
            break
        return True

    def __iter__(self):
        self.line_counter = 0
        return self

    def __next__(self):
        self.line_counter += 1
        if self.line_counter == 15:
            raise StopIteration
        elif self.line_counter == 1:
            return " |1|2|3|4|5|6|"
        elif self.line_counter == 14:
            return "--------------"
        elif self.line_counter % 2 == 0:
            return "-+-+-+-+-+-+-|"
        else:
            line_num = self.line_counter // 2
            board_line = []
            for i in range(14):
                if i % 2 != 0: board_line.append("|")
                elif i == 0: board_line.append(str(line_num))
                else:
                    board_line.append(str(self.dots[(line_num - 1) * self.__size + i // 2 - 1]))
            self.changeLine(board_line)
            return "".join(board_line)

    def check(self, xy):
        if xy[0] < 0 or xy[0] >= self.__size:
            return False
        if xy[1] < 0 or xy[1] >= self.__size:
            return False
        idx = xy[0] + xy[1] * self.__size
        if self.dots[idx].shipped or self.dots[idx].contoured:
            return False
        return True

    def contour(self, position):
        for x, y in position:
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    _x = x + dx
                    _y = y + dy
                    if 0 <= _x < self.__size and 0 <= _y < self.__size:
                        idx = _x + _y * self.__size
                        if not self.dots[idx].shipped:
                            self.dots[idx].contoured = True

    def areAllShipsKilled(self):
        return all([ship.killed for ship in self.ships])

    def isShipKilled(self, xy):
        for ship in self.ships:
            if ship.isHitted(xy):
                return ship.killed

    @abstractmethod
    def changeLine(self, line):
        pass

    @abstractmethod
    def shot(self, xy):
        pass


class CompBoard(Board):
    #def __init__(self):
    #    pass

    def changeLine(self, line):
        for idx in range(len(line)):
            if line[idx] == "O":
                line[idx] = " "

    def shot(self, xy):
        mess = "Вы стреляли {0}. ".format(xy)
        xy[0] -= 1
        xy[1] -= 1
        idx = xy[0] + xy[1]  * super()._Board__size
        if self.dots[idx].struck:
            raise BoardError
        self.dots[idx].struck = True
        if self.dots[idx].shipped:
            self.dots[idx].hitted = True
            if self.isShipKilled(xy):
                return [True, mess + "Убит!"]
            else:
                return [True, mess + "Ранен!"]
        return [False, mess + "Мимо!"]


class HumanBoard(CompBoard):
    def __init__(self):
        super().__init__()
        self.comp = Comp()

    def changeLine(self, line):
        pass

    def shot(self, no_xy):
        xy = self.comp.nextShot(self.dots, super()._Board__size)
        if xy is None:
            return [False, "!!!!!!!"]
        ##########################
        _xy = list(xy)  # super().shot(xy) поменяет координаты! предохранимся
        result = super().shot(xy)
        self.comp.addShortResult(_xy, result[1], self.dots, super()._Board__size)
        return [result[0], result[1].replace("Вы стреляли", "Компьютер стрелял")]



