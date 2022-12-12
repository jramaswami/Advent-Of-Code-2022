"""
Advent of Code 2022
Day 12: Hill Climbing Algorithm
jramaswami
"""


import collections
import math


def read_input(filename):
    "Return elevation grid."
    with open(filename) as infile:
        grid = [line.strip() for line in infile]
    return grid


def get_height(code):
    "Return height as integer."
    if code == 'S':
        return 0
    elif code == 'E':
        return 26
    return ord(code) - ord('a')


def find_start(grid):
    "Find the starting point."
    for r, row in enumerate(grid):
        for c, code in enumerate(row):
            if code == 'S':
                return r, c


def find_zero_elevations(grid):
    "Generator to yield all positions with zero elevation."
    for r, row in enumerate(grid):
        for c, code in enumerate(row):
            if code == 'S' or code == 'a':
                yield r, c


def bfs(init_r, init_c, grid):
    """
    Return the minimum number of steps from start to end, where
    each step can only increase the height by at most 1.
    """

    def inbounds(r, c):
        "Return True if r, c is inside the grid."
        return r >= 0 and c >= 0 and r < len(grid) and c < len(grid[r])

    OFFSETS = ((1, 0), (-1, 0), (0, 1), (0, -1))

    def neighbors(r, c):
        "Generator for neighbors of r, c."
        for dr, dc in OFFSETS:
            r0, c0 = r + dr, c + dc
            if inbounds(r0, c0):
                yield r0, c0

    # BFS to find smallest distance.
    queue = collections.deque([(init_r, init_c, 0)])
    visited = [[False for _ in row] for row in grid]
    visited[init_r][init_c] = True
    while queue:
        r, c, d = queue.popleft()
        code = grid[r][c]
        if grid[r][c] == 'E':
            return d
        for r0, c0 in neighbors(r, c):
            code0 = grid[r0][c0]
            if not visited[r0][c0] and get_height(code0) - get_height(code) <= 1:
                visited[r0][c0] = True
                queue.append((r0, c0, d+1))

    # Unreachable.
    return math.inf


def solve_a(grid):
    "Solve part A of puzzle."
    init_r, init_c = find_start(grid)
    return bfs(init_r, init_c, grid)


def solve_b(grid):
    "Solve part B of puzzle."
    return min(bfs(r, c, grid) for r, c in find_zero_elevations(grid))


#
# Testing
#


def test_solve_a():
    grid = read_input('../test.txt')
    expected = 31
    assert solve_a(grid) == expected


def test_solve_b():
    grid = read_input('../test.txt')
    expected = 29
    assert solve_b(grid) == expected


#
# Main
#


def main():
    "Main program."
    import pyperclip
    grid = read_input('../input12.txt')
    soln_a = solve_a(grid)
    assert soln_a == 449
    print(f"The solution to part A is {soln_a}.")
    soln_b = solve_b(grid)
    assert soln_b == 443
    print(f"The solution to part B is {soln_b}.")
    pyperclip.copy(str(soln_b))
    print(f"{soln_b} has been placed on the clipboard.")


if __name__ == '__main__':
    main()
