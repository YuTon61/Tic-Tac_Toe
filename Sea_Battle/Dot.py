class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.cleared = True
        self.struck = False
        self.shipped = False
        self.contoured = False
        self.hitted = False
        self.dont_hit = False

    def __str__(self):
        if self.hitted: return "*"
        if self.struck: return "!"
        if self.shipped: return "O"
        #if self.dont_hit: return "."
        if self.cleared: return " "
        return "?"

