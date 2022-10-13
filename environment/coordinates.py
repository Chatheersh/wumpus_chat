class Coordinate:
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y
    
    def is_equal(self, c):
        return self.x == c.x and self.y == c.y