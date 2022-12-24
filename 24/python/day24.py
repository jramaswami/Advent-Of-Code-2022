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


class GridA:
    "Grid to solve part A of puzzle."

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
        if r == 0 and c == 1:
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

    def move_blizzards(self):
        "Move all the blizzards"
        grid0 = [[[] for _ in row] for row in self.grid]
        for r, row in enumerate(self.grid):
            for c, cell in enumerate(row):
                for dr, dc in cell:
                    r0, c0 = self.wrap(r + dr, c + dc)
                    grid0[r0][c0].append((dr, dc))
        self.grid = grid0

    def move_mes(self):
        "Compute all my next possible positions."
        me0 = set()
        for r, c in self.me:
            for dr, dc in MY_MOVES:
                r0, c0 = r + dr, c + dc
                if self.inbounds(r0, c0) and len(self.grid[r0][c0]) == 0:
                    me0.add((r0, c0))
        self.me = me0

    def tick(self):
        "Simulate one round."
        self.move_blizzards()
        self.move_mes()

    def found_exit(self):
        "Return True if the exit has been found."
        return any(r == self.height - 1 and c == self.width - 2 for r, c in self.me)

    def solve(self):
        "Solve puzzle."
        soln = 0
        while not self.found_exit():
            self.tick()
            soln += 1
        return soln

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


class GridB(GridA):
    "Grid to solve part B of puzzle by keeping track of which trip I am on."

    FIRST_TRIP = 0
    TRIP_BACK = 1
    SECOND_TRIP = 2

    def __init__(self, grid):
        super().__init__(grid)
        self.mes_b = set()
        self.mes_b.add((0, 1, 0))
        self.current_trip = GridB.FIRST_TRIP

    def is_exit(self, r, c):
        "Return True if position is the exit."
        return r == self.height - 1 and c == self.width - 2

    def is_entrance(self, r, c):
        "Return True if position is the entrance."
        return r == 0 and c == 1

    def move_mes(self):
        "Compute all my next possible positions with trip."
        me0 = set()
        for r, c, trip in self.mes_b:
            for dr, dc in MY_MOVES:
                r0, c0 = r + dr, c + dc
                trip0 = trip
                if self.inbounds(r0, c0) and len(self.grid[r0][c0]) == 0:
                    if trip == GridB.FIRST_TRIP and self.is_exit(r0, c0):
                        trip0 = GridB.TRIP_BACK
                    elif trip == GridB.TRIP_BACK and self.is_entrance(r0, c0):
                        trip0 = GridB.SECOND_TRIP
                    self.current_trip = max(self.current_trip, trip0)
                    me0.add((r0, c0, trip0))
        self.mes_b = me0
        # self.mes_b = {t for t in me0 if t[2] == self.current_trip}

    def found_exit(self):
        "Return True if the exit has been found *on the second trip*."
        return any(
            t == GridB.SECOND_TRIP and self.is_exit(r, c)
            for r, c, t in self.mes_b
        )


#
# Testing
#


def test_get_grid():
    grid = GridA(read_input('../test.txt'))
    expected = read_input('../expected0.txt')
    assert grid.get_grid() == expected


def test_solve_a():
    grid = GridA(read_input('../test.txt'))
    expected = 18
    assert grid.solve() == expected


def test_solve_b():
    grid = GridB(read_input('../test.txt'))
    expected = 54
    assert grid.solve() == expected


#
# Main
#


def main():
    "Main program"
    import pyperclip
    input_grid = read_input('../input24.txt')
    grid = GridA(input_grid)
    soln_a = grid.solve()
    print(f"The solution to part A is {soln_a}.")
    assert soln_a == 299
    pyperclip.copy(str(soln_a))
    print(f"{soln_a} has been placed in the clipboard.")

    input_grid = read_input('../input24.txt')
    grid = GridB(input_grid)
    soln_b = grid.solve()
    print(f"The solution to part B is {soln_b}.")
    assert soln_b == 899
    pyperclip.copy(str(soln_b))
    print(f"{soln_b} has been placed in the clipboard.")


if __name__ == '__main__':
    main()
