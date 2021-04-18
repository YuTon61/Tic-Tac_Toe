from Dot import Dot


class Comp:
    __shot_sequence = [
        [3, 3], [4, 4], [3, 5], [2, 4], [1, 3], [2, 2], [3, 1], [4, 2], [5, 3],
        [6, 4], [5, 5], [4, 6], [2, 6], [1, 5], [1, 1], [5, 1], [6, 2], [6, 6]
    ]

    def __init__(self):
        self.shot_num = 0
        self.hitted_dots = []
        self.hitted_x = 0
        self.hitted_y = 0

    def nextShot(self, dots, size):
        xy = self.searchNextShipDot(dots, size)
        if xy is not None:
            return xy
        while True:
            if self.shot_num < len(self.__shot_sequence):
                self.shot_num += 1
                xy = self.__shot_sequence[self.shot_num - 1]
                idx = xy[0] - 1 + (xy[1] - 1) * size
                if dots[idx].struck or dots[idx].hitted or dots[idx].dont_hit:
                    continue
                break
            else:
                xy = None
                break
        ########
        if xy is None:
            do_break = False
            for x in range(1, size + 1):
                for y in range(1, size + 1):
                    idx = x - 1 + (y - 1) * size
                    if not dots[idx].struck and not dots[idx].hitted and not dots[idx].dont_hit:
                        do_break = True
                        xy = [x, y]
                        break
                if do_break:
                    break
        return xy

    def addShortResult(self, xy, mess, dots, size):
        if mess.find("Ранен") != -1 or mess.find("Убит") != -1:
            self.hitted_dots.append(Dot(xy[0], xy[1]))
            self.hitted_x = xy[0]
            self.hitted_y = xy[1]
        if mess.find("Убит") != -1:
            self.makeContour(dots, size)
            self.hitted_dots.clear()

    def searchNextShipDot(self, dots, size):
        ######### раненых кораблей нет
        if len(self.hitted_dots) == 0:
            return None
        ######### две раны => не более 2-х вариантов следующего выстрела ###############################################
        if len(self.hitted_dots) == 2:
            ##### трёхпалубник расположен вертикально
            if self.hitted_dots[0].x == self.hitted_dots[1].x:
                x = self.hitted_dots[0].x
                y_min = min(self.hitted_dots[0].y, self.hitted_dots[1].y)
                y_max = max(self.hitted_dots[0].y, self.hitted_dots[1].y)
                #### сверху?
                if y_min > 1:
                    idx = x - 1 + (y_min - 2) * size
                    if not dots[idx].struck and not dots[idx].hitted and not dots[idx].dont_hit:
                        return [x, y_min - 1]
                #### снизу?
                if y_max < size:
                    idx = x - 1 + y_max * size
                    if not dots[idx].struck and not dots[idx].hitted and not dots[idx].dont_hit:
                        return [x, y_max + 1]
            ##### трёхпалубник расположен горизонтально
            if self.hitted_dots[0].y == self.hitted_dots[1].y:
                y = self.hitted_dots[0].y
                x_min = min(self.hitted_dots[0].x, self.hitted_dots[1].x)
                x_max = max(self.hitted_dots[0].x, self.hitted_dots[1].x)
                #### слева?
                if x_min > 1:
                    idx = x_min - 2 + (y - 1) * size
                    if not dots[idx].struck and not dots[idx].hitted and not dots[idx].dont_hit:
                        return [x_min - 1, y]
                #### справа?
                if x_max < size:
                    idx = x_max + (y - 1) * size
                    if not dots[idx].struck and not dots[idx].hitted and not dots[idx].dont_hit:
                        return [x_max + 1, y]
            print("Компьютер не понимает вертикально или горизонтально расположен трёхпалубник !!!!!!!!!!!!!!!!!!!")
            return None

        ######### одна рана => не более 4-х вариантов следующего выстрела ##############################################
        ######### пробуем x - 1, y
        if self.hitted_x > 1:
            idx = self.hitted_x - 2 + (self.hitted_y - 1) * size
            if not dots[idx].struck and not dots[idx].hitted and not dots[idx].dont_hit:
                return [self.hitted_x - 1, self.hitted_y]
        ######### пробуем x, y - 1
        if self.hitted_y > 1:
            idx = self.hitted_x - 1 + (self.hitted_y - 2) * size
            if not dots[idx].struck and not dots[idx].hitted and not dots[idx].dont_hit:
                return [self.hitted_x, self.hitted_y - 1]
        ######### пробуем x + 1, y
        if self.hitted_x < size:
            idx = self.hitted_x + (self.hitted_y - 1) * size
            if not dots[idx].struck and not dots[idx].hitted and not dots[idx].dont_hit:
               return [self.hitted_x + 1, self.hitted_y]
        ######### пробуем x, y + 1
        if self.hitted_y < size:
            idx = self.hitted_x - 1 + self.hitted_y * size
            if not dots[idx].struck and not dots[idx].hitted and not dots[idx].dont_hit:
               return [self.hitted_x, self.hitted_y + 1]

        ######## None
        print("Компьютер не знает где следующая точка корабля !!!!!!!!!!!!!!!!!!!")
        return None

    def makeContour(self, dots, size):
        for dot in self.hitted_dots:
            for x in range(-1, 2):
                _x = dot.x + x
                if _x < 1 or _x > size:
                    continue
                for y in range(-1, 2):
                    _y = dot.y + y
                    if _y < 1 or _y > size:
                        continue
                    idx = _x - 1 + (_y - 1) * size
                    dots[idx].dont_hit = True

