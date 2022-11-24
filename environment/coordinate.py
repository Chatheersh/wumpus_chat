class Coordinate:
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self) -> int:
        return hash(((self.x + self.y)*(self.x + self.y + 1)/2) + self.y)

    def __str__(self):
        return f"{self.x},{self.y}"