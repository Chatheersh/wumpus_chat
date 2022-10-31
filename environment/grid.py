class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
        self.grid = []

        for y in range(height - 1, -1, -1):
            self.grid.append([])
            for x in range(width):
                self.grid[height - y - 1].append(0)

    def set_one(self, x, y):
        self.set_value(x, y, 1)

    def set_value(self, x, y, value):
        self.grid[self.height - y - 1][x] = value

    def get_value(self, x, y):
        return self.grid[self.height - y - 1][x]