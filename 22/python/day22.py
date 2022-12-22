"""
Advent of Code 2022
Day 22: Monkey Map
jramaswami
"""


import math
import collections


Posn = collections.namedtuple('Posn', ['row', 'col'])


def read_input(filename):
    """
    Read input from filename.
    Return (grid as list of list of strings, path)
    """
    grid = []
    with open(filename) as infile:
        lines = [line.strip('\n') for line in infile]
        return ([[c for c in t] for t in lines[:-2]], lines[-1])


class Grove:
    "Grove for part A where wrapping is a torus."

    OFFSETS = [Posn(0, 1), Posn(1, 0), Posn(0, -1), Posn(-1, 0)]
    MARK = '>v<^'
    EAST = 0
    SOUTH = 1
    WEST = 2
    NORTH = 3

    def __init__(self, grid, path):
        self.grid = grid
        # Find the widest grid row.
        width = max(len(t) for t in grid)
        # Find the min, max for each row and column to create a torus.
        self.row_min = [math.inf for _ in grid]
        self.row_max = [-math.inf for _ in grid]
        self.col_min = [math.inf for _ in range(width)]
        self.col_max = [-math.inf for _ in range(width)]
        for r, row in enumerate(self.grid):
            for c, val in enumerate(row):
                if not val.isspace():
                    self.row_min[r] = min(self.row_min[r], c)
                    self.row_max[r] = max(self.row_min[r], c)
                    self.col_min[c] = min(self.col_min[c], r)
                    self.col_max[c] = max(self.col_min[c], r)
        self.facing = Grove.NORTH
        # Parse path.
        window = collections.deque()
        self.path = []
        for c in path:
            if c.isnumeric():
                window.append(c)
            else:
                self.path.append(int("".join(window)))
                window.clear()
                self.path.append(c)
        if window:
            self.path.append(int("".join(window)))
        # Start at beginning ...
        self.facing = Grove.EAST
        self.posn = Posn(0, self.row_min[0])
        self.grid[self.posn.row][self.posn.col] = Grove.MARK[self.facing]

    def inbounds(self, posn):
        "Return True if posn is inside the grove."
        r, c = posn
        if r < 0 or r >= len(self.grid):
            return False
        if c < 0 or c >= len(self.grid[r]):
            return False
        if self.grid[r][c].isspace():
            return False
        return True

    def turn(self, direction):
        "Change facing based on direction of turn."
        if direction == 'L':
            self.facing -= 1
            if self.facing < Grove.EAST:
                self.facing = Grove.NORTH
        else:
            self.facing += 1
            if self.facing > Grove.NORTH:
                self.facing = Grove.EAST
        self.grid[self.posn.row][self.posn.col] = Grove.MARK[self.facing]

    def wrap(self):
        "Return the position when you wrap around to the other side."
        if self.facing == Grove.EAST:
            return Posn(self.posn.row, self.row_min[self.posn.row])
        elif self.facing == Grove.WEST:
            return Posn(self.posn.row, self.row_max[self.posn.row])
        elif self.facing == Grove.SOUTH:
            return Posn(self.col_min[self.posn.col], self.posn.col)
        elif self.facing == Grove.NORTH:
            return Posn(self.col_max[self.posn.col], self.posn.col)

    def move(self, steps):
        """
        Move the given number of steps, unless you run into a wall.
        Be sure to wrap around if you go out of bounds.
        """
        for _ in range(steps):
            moving = Grove.OFFSETS[self.facing]
            posn0 = Posn(self.posn.row + moving.row, self.posn.col + moving.col)
            if not self.inbounds(posn0):
                posn0 = self.wrap()
            if self.grid[posn0.row][posn0.col] == '#':
                return
            self.posn = posn0
            self.grid[self.posn.row][self.posn.col] = Grove.MARK[self.facing]

    def walk(self):
        "Walk the path ..."
        for i, p in enumerate(self.path):
            if i % 2 == 0:
                self.move(p)
            else:
                self.turn(p)

    def solve(self):
        "Solve puzzle."
        self.walk()
        return (
            ((self.posn.row + 1) * 1000) +
            ((self.posn.col + 1) * 4) +
            self.facing
        )

    def __str__(self):
        return "\n".join("".join(t) for t in self.grid)


class CubeGrove(Grove):
    "Grove for part B where wrapping is a cube."

    def __init__(self, grid, path, facesize, facemap, wrapfn):
        super().__init__(grid, path)
        self.faces = [[' ' for _ in row] for row in grid]
        self.faceoffsets = [Posn(0, 0) for _ in range(7)]
        # self.grids = [[[' ' for _ in range(facesize)] for _ in range(facesize)] for _ in range(7)]
        for i, facerow in enumerate(facemap):
            for j, faceid in enumerate(facerow):
                if faceid:
                    top = i * facesize
                    left = j * facesize
                    self.faceoffsets[faceid] = Posn(top, left)
                    for r in range(top, top+facesize):
                        for c in range(left, left+facesize):
                            if c >= len(self.faces[r]):
                                break
                            self.faces[r][c] = faceid
                            # self.grids[faceid][r-top][c-left] = grid[r][c]
        self.wrapfn = wrapfn

    def wrap(self):
        "Wrap using wrapping function passed in at initialization."
        self.grid[self.posn.row][self.posn.col] = '*'
        # Convert to face posn.
        faceid = self.faces[self.posn.row][self.posn.col]
        faceoff = self.faceoffsets[faceid]
        posn = Posn(self.posn.row - faceoff.row, self.posn.col - faceoff.col)
        faceid0, posn0, facing0 = self.wrapfn(faceid, posn, self.facing)
        self.grid[self.posn.row][self.posn.col] = Grove.MARK[self.facing]
        # Convert posn to actual posn
        faceoff = self.faceoffsets[faceid0]
        posn0 = Posn(posn0.row + faceoff.row, posn0.col + faceoff.col)
        return posn0, facing0

    def move(self, steps):
        """
        Move the given number of steps, unless you run into a wall.
        Be sure to wrap around if you go out of bounds.
        """
        for _ in range(steps):
            moving = Grove.OFFSETS[self.facing]
            posn0 = Posn(self.posn.row + moving.row, self.posn.col + moving.col)
            facing0 = self.facing
            if not self.inbounds(posn0):
                posn0, facing0 = self.wrap()
            if self.grid[posn0.row][posn0.col] == '#':
                return
            self.posn = posn0
            self.facing = facing0
            self.grid[self.posn.row][self.posn.col] = Grove.MARK[self.facing]


def wrapping_for_test_input(faceid, posn, facing):
    "Wrapping function for test input."
    if faceid == 2 and facing == Grove.EAST:
        return 3, Posn(0, 4 - 1 - posn.row), Grove.SOUTH
    if faceid == 6 and facing == Grove.SOUTH:
        return 5, Posn(4 - 1, 4 - 1 - posn.col), Grove.NORTH
    if faceid == 4 and facing == Grove.NORTH:
        return 1, Posn(posn.col, 0), Grove.EAST
    raise Exception("Cannot wrap")


def wrapping_for_actual_input(faceid, posn, facing):
    """
    Wrapping function for actual input.
    Spent quality time with a cube to write this.  :  )
    """
    # FACE ID == 1
    if faceid == 1:
        if facing == Grove.EAST:
            return 3, Posn(posn.row, 0), Grove.EAST
        if facing == Grove.SOUTH:
            return 2, Posn(0, posn.col), Grove.SOUTH
        if facing == Grove.WEST:
            return 4, Posn(50 - 1 - posn.row, 0), Grove.EAST
        if facing == Grove.NORTH:
            return 5, Posn(posn.col, 0), Grove.EAST

    # FACE ID == 2
    if faceid == 2:
        if facing == Grove.EAST:
            return 3, Posn(50-1, posn.row), Grove.NORTH
        if facing == Grove.SOUTH:
            return 6, Posn(0, posn.col), Grove.SOUTH
        if facing == Grove.WEST:
            return 4, Posn(0, posn.row), Grove.SOUTH
        if facing == Grove.NORTH:
            return 1, Posn(50-1, posn.col), Grove.NORTH

    # FACE ID == 3
    if faceid == 3:
        if facing == Grove.EAST:
            return 6, Posn(50-1-posn.row, 50-1), Grove.WEST
        if facing == Grove.SOUTH:
            return 2, Posn(posn.col, 50-1), Grove.WEST
        if facing == Grove.WEST:
            return 1, Posn(posn.row, 50-1), Grove.WEST
        if facing == Grove.NORTH:
            return 5, Posn(50-1, posn.col), Grove.NORTH

    # FACE ID == 4
    if faceid == 4:
        if facing == Grove.EAST:
            6, Posn(posn.row, 0), Grove.EAST
        if facing == Grove.SOUTH:
            5, Posn(0, posn.col), Grove.SOUTH
        if facing == Grove.WEST:
            return 1, Posn(50-1-posn.row, 0), Grove.EAST
        if facing == Grove.NORTH:
            return 2, Posn(posn.col, 0), Grove.EAST

    # FACE ID == 5
    if faceid == 5:
        if facing == Grove.EAST:
            return 6, Posn(50-1, posn.row) ,Grove.NORTH
        if facing == Grove.SOUTH:
            return 3, Posn(0, posn.col), Grove.SOUTH
        if facing == Grove.WEST:
            return 1, Posn(0, posn.row), Grove.SOUTH
        if facing == Grove.NORTH:
            4, Posn(50-1, posn.col), Grove.NORTH

    # FACE ID == 6
    if faceid == 6:
        if facing == Grove.EAST:
            return 3, Posn(50-1-posn.row, 50-1), Grove.WEST
        if facing == Grove.SOUTH:
            return 5, Posn(posn.col, 50-1), Grove.WEST
        if facing == Grove.WEST:
            return 4, Posn(posn.row, 50-1), Grove.WEST
        if facing == Grove.NORTH:
            return 2, Posn(50-1, posn.col), Grove.NORTH

    msg = f"Cannot wrap: {faceid=} {posn=} {facing=}"
    raise Exception(msg)


#
# Testing
#


def test_wrap():
    grove = Grove(*(read_input('../test.txt')))

    grove.posn = Posn(6, 0)
    grove.facing = Grove.WEST
    assert grove.wrap() == Posn(6, 11)

    grove.posn = Posn(6, 11)
    grove.facing = Grove.EAST
    assert grove.wrap() == Posn(6, 0)

    grove.posn = Posn(4, 5)
    grove.facing = Grove.NORTH
    assert grove.wrap() == Posn(7, 5)

    grove.posn = Posn(7, 5)
    grove.facing = Grove.SOUTH
    assert grove.wrap() == Posn(4, 5)


def test_solve_a():
    grove = Grove(*(read_input('../test.txt')))
    assert grove.solve() == 6032


def test_solve_b():
    grid, path = read_input('../test.txt')
    facesize, facemap = 4, [[0, 0, 1, 0], [5, 4, 2, 0], [0, 0, 6, 3]]
    grove = CubeGrove(grid, path, facesize, facemap, wrapping_for_test_input)
    assert grove.solve() == 5031


#
# Main
#


def main():
    "Main program."
    import pyperclip
    inp = read_input('../input22.txt')
    grove = Grove(*inp)
    soln_a = grove.solve()
    print(f"The solution to part A is {soln_a}.")
    assert soln_a == 88226

    grid, path = read_input('../input22.txt')
    facesize, facemap = 50, [[0, 1, 3], [0, 2, 0], [4, 6, 0], [5, 0, 0]]
    grove = CubeGrove(grid, path, facesize, facemap, wrapping_for_actual_input)
    soln_b = grove.solve()
    print(f"The solution to part B is {soln_b}.")
    assert soln_b == 57305
    pyperclip.copy(soln_b)
    print(f"{soln_b} has been placed on the clipboard.")


if __name__ == '__main__':
    main()
