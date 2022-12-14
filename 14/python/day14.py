"""
Advent of Code 2022
Day 14: Regolith Reservoir
jramaswami
"""


import collections


Point = collections.namedtuple('Point', ['x', 'y'])


def read_input(filename):
    "Return lilst of lines, where each line is a list of points."
    lines = []
    with open(filename) as infile:
        for line in infile:
            tokens = line.strip().split('->')
            points = [Point(*(int(i) for i in t.split(','))) for t in tokens]
            lines.append(points)
    return lines


def draw_grid(lines):
    "Draw the map by placing each point in a set."
    grid = set()
    for line in lines:
        for p1, p2 in zip(line[:-1], line[1:]):
            # Which way does line go?
            if p1.x == p2.x:
                # Vertical
                for y in range(min(p1.y, p2.y), max(p1.y, p2.y) + 1):
                    grid.add(Point(p1.x, y))
            else:
                # Horizontal
                for x in range(min(p1.x, p2.x), max(p1.x, p2.x) + 1):
                    grid.add(Point(x, p1.y))
    return grid


def drop_sand_a(grid):
    """
    Drop a piece of sand.
    Return True if it settled.
    Return False if it fell into the abyss.
    """

    # Determine bottom of grid.
    bottom = max(p.y for p in grid)

    sand = Point(500, 0)
    while sand.y < bottom:
        down = Point(sand.x, sand.y + 1)
        diag_left = Point(sand.x - 1, sand.y + 1)
        diag_right = Point(sand.x + 1, sand.y + 1)
        if down not in grid:
            sand = down
        elif diag_left not in grid:
            sand = diag_left
        elif diag_right not in grid:
            sand = diag_right
        else:
            # Sand comes to rest.
            grid.add(sand)
            return True

    # Sand fell off into the abyss
    return False


def solve_a(grid):
    "Solve part A of puzzle."
    sand = 0
    while 1:
        if drop_sand_a(grid):
            sand += 1
        else:
            return sand


def drop_sand_b(grid, floor):
    """
    Drop a piece of sand.
    Return True if it settled lower than 500, 0.
    Return False if it settled at 500, 0.
    """

    def point_is_occupied(p):
        "Helper fn to determine if point is occupied."
        if p.y == floor:
            return True
        return p in grid

    sand = Point(500, 0)
    while 1:
        down = Point(sand.x, sand.y + 1)
        diag_left = Point(sand.x - 1, sand.y + 1)
        diag_right = Point(sand.x + 1, sand.y + 1)
        if not point_is_occupied(down):
            sand = down
        elif not point_is_occupied(diag_left):
            sand = diag_left
        elif not point_is_occupied(diag_right):
            sand = diag_right
        else:
            # Sand comes to rest.
            grid.add(sand)
            break
    return sand != Point(500, 0)


def solve_b(grid):
    "Solve part B of puzzle."
    # Determine bottom of grid.
    floor = max(p.y for p in grid) + 2

    sand = 0
    while 1:
        if drop_sand_b(grid, floor):
            sand += 1
        else:
            return sand + 1 # Add the sand at (500, 0)


#
# Testing
#


def test_solve_a():
    lines = read_input('../test.txt')
    grid = draw_grid(lines)
    expected = 24
    assert solve_a(grid) == expected


def test_solve_b():
    lines = read_input('../test.txt')
    grid = draw_grid(lines)
    expected = 93
    assert solve_b(grid) == expected


#
# Main
#


def main():
    "Main program."
    import pyperclip
    lines = read_input('../input14.txt')
    grid = draw_grid(lines)
    soln_a = solve_a(grid)
    assert soln_a == 964
    print(f"The solution to part A is {soln_a}.")
    grid = draw_grid(lines)
    soln_b = solve_b(grid)
    assert soln_b == 32041
    print(f"The solution to part B is {soln_b}.")
    pyperclip.copy(str(soln_b))
    print(f"{soln_b} has been placed on the clipboard.")



if __name__ == '__main__':
    main()
