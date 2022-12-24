"""
Advent of Code 2022
Day 24: Blizzard Basin
jramaswami
"""


BLIZZARDS = {'^': (-1, 0), '>': (0, 1), 'v': (1, 0), '<': (0, -1)}
SIGNS = {(-1, 0): '^', (0, 1): '>', (1, 0): 'v',  (0, -1): '<'}
MY_MOVES = [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)]


def read_input(filename):
    with open(filename) as infile:
        return [[t for t in line.strip()] for line in infile]


class Grid:

    def __init__(self, grid):
        self.height = len(grid)
        self.width = len(grid[0])
        self.grid = [[[] for _ in row] for row in grid]
        for r, row in enumerate(grid):
            for c, val in enumerate(row):
                if val in BLIZZARDS:
                    self.grid[r][c].append(BLIZZARDS[val])
        self.me = set([(0, 1)])

    def inbounds(self, r, c):
        "Return True if r, c is inside the grid."
        # Entrance
        if r == 1 and c == 1:
            return True
        # Exit
        if r == self.height - 1 and c == self.width - 2:
            return True
        # Avoid walls.
        return (
            r >= 1 and r < self.height - 1 and
            c >= 1 and c < self.width - 1
        )

    def wrap(self, r, c):
        "Wrap position, if necessary."
        if r == 0:
            r = self.height - 2
        if r == self.height - 1:
            r = 1
        if c == 0:
            c = self.width - 2
        if c == self.width - 1:
            c = 1
        return r, c

    def tick(self):
        "Simulate one round."
        # Move blizzards.
        grid0 = [[[] for _ in row] for row in self.grid]
        for r, row in enumerate(self.grid):
            for c, cell in enumerate(row):
                for dr, dc in cell:
                    r0, c0 = self.wrap(r + dr, c + dc)
                    grid0[r0][c0].append((dr, dc))
        # Move me(s).
        me0 = set()
        for r, c in self.me:
            for dr, dc in MY_MOVES:
                r0, c0 = r + dr, c + dc
                if self.inbounds(r0, c0) and len(grid0[r0][c0]) == 0:
                    me0.add((r0, c0))
        self.me = me0
        self.grid = grid0

    def found_exit(self):
        "Return True if the exit has been found."
        return any(r == self.height - 1 and c == self.width - 2 for r, c in self.me)

    def solve_a(self):
        "Solve part A of puzzle."
        soln_a = 0
        while not self.found_exit():
            self.tick()
            soln_a += 1
        return soln_a

    def get_grid(self):
        "Return grid as represented on screen."
        grid = [['.' for _ in row] for row in self.grid]
        for r, row in enumerate(self.grid):
            for c, _ in enumerate(row):
                if r == 0 and c == 1:
                    grid[r][c] = '.'
                elif r == self.height-1 and c == self.width-2:
                    grid[r][c] = '.'
                elif r == 0 or r == self.height - 1:
                    grid[r][c] = '#'
                elif c == 0 or c == self.width - 1:
                    grid[r][c] = '#'
                elif len(self.grid[r][c]) == 1:
                    grid[r][c] = SIGNS[self.grid[r][c][0]]
                elif len(self.grid[r][c]) > 1:
                    grid[r][c] = str(len(self.grid[r][c]))
        for r, c in self.me:
            grid[r][c] = 'E'
        return grid

    def __str__(self):
        return "\n".join("".join(row) for row in self.get_grid())


#
# Testing
#


def test_get_grid():
    grid = Grid(read_input('../test.txt'))
    expected = read_input('../expected0.txt')
    assert grid.get_grid() == expected


def test_solve_a():
    grid = Grid(read_input('../test.txt'))
    expected = 18
    assert grid.solve_a() == expected


#
# Main
#


def main():
    "Main program"
    import pyperclip
    grid = Grid(read_input('../input24.txt'))
    soln_a = grid.solve_a()
    print(f"The solution to part A is {soln_a}.")
    assert soln_a == 299
    pyperclip.copy(str(soln_a))
    print(f"{soln_a} has been placed in the clipboard.")


if __name__ == '__main__':
    main()
