from environment.grid import Grid


class ProbGrid(Grid):
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
        self.grid = []

        for y in range(height - 1, -1, -1):
            self.grid.append([])
            for x in range(width):
                self.grid[height - y - 1].append(0.0)

    def set_one(self, x, y):
        self.set_value(x, y, 1.0)

    def print_grid(self):

        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x] < 10:
                    print(f"  {round(self.grid[y][x], 1)}", end='')
                else:
                    print(f" {round(self.grid[y][x], 1)}", end='')

            print('\n')