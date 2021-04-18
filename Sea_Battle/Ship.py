from Dot import Dot


class Ship:
    def __init__(self, ship_num):
        self.dots = [Dot(0, 0)]
        if ship_num == 1:
            self.dots.append(Dot(0, 0))
            self.dots.append(Dot(0, 0))
        elif 2 <= ship_num <= 3:
            self.dots.append(Dot(0, 0))

    @property
    def size(self):
        return len(self.dots)

    @property
    def killed(self):
        return all([dot.hitted for dot in self.dots])

    def isHitted(self, xy):
        for dot in self.dots:
            if dot.x == xy[0] and dot.y == xy[1]:
                dot.hitted = True
                return True
        return False

    def position(self, position):
        for xy, dot in zip(position, self.dots):
            dot.x = xy[0]
            dot.y = xy[1]
