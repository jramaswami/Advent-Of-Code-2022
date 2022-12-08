"""
Advent of Code 2022
Day 8: Treetop Tree House
jramaswami
"""


import math
import functools
import operator


def get(r, c, grid, default=-math.inf):
    "Helper fn to return grid value or default value if out of bounds."
    if r < 0 or c < 0 or r >= len(grid) or c >= len(grid[0]):
        return default
    return grid[r][c]


class TreeGrid:

    def __init__(self, input_file_name):
        # Read input
        self.tree_grid = []
        with open(input_file_name) as infile:
            for line in infile:
                self.tree_grid.append([int(t) for t in line.strip()])

        # Compute row/col prefix/suffix heights.
        H = len(self.tree_grid)
        W = len(self.tree_grid[0])

        self.row_prefix = [[-math.inf for _ in row] for row in self.tree_grid]
        self.row_suffix = [[-math.inf for _ in row] for row in self.tree_grid]
        self.col_prefix = [[-math.inf for _ in col] for col in self.tree_grid]
        self.col_suffix = [[-math.inf for _ in col] for col in self.tree_grid]

        for r in range(H):
            for c in range(W):
                self.row_prefix[r][c] = max(
                    get(r, c, self.tree_grid),
                    get(r, c-1, self.row_prefix)
                )
            for c in range(W-1, -1, -1):
                self.row_suffix[r][c] = max(
                    get(r, c, self.tree_grid),
                    get(r, c+1, self.row_suffix)
                )

        for c in range(W):
            for r in range(H):
                self.col_prefix[r][c] = max(
                    get(r, c, self.tree_grid),
                    get(r-1, c, self.col_prefix)
                )
            for r in range(H-1, -1, -1):
                self.col_suffix[r][c] = max(
                    get(r, c, self.tree_grid),
                    get(r+1, c, self.col_suffix)
                )

    def is_visible_dirn(self, r, c):
        "Return list of visibility directions for given tree."
        tree = get(r, c, self.tree_grid)
        left = get(r, c-1, self.row_prefix)
        right = get(r, c+1, self.row_suffix)
        up = get(r-1, c, self.col_prefix)
        down = get(r+1, c, self.col_suffix)
        return [tree > other for other in (left, right, up, down)]

    def is_tree_visible(self, r, c):
        "Return True if tree is visible from one of the edges."
        return any(self.is_visible_dirn(r, c))

    def solve_a(self):
        "Return the count of visible trees."
        soln_a = 0
        for r, row in enumerate(self.tree_grid):
            for c, _ in enumerate(row):
                if self.is_tree_visible(r, c):
                    soln_a += 1
        return soln_a

    def inbounds(self, r, c):
        "Return True if (r, c) is inbounds."
        return (
            r >= 0 and c >= 0 and
            r < len(self.tree_grid) and
            c < len(self.tree_grid[r])
        )

    def visible_trees_in_dirn(self, r, c, dirn):
        "Return the number of visible trees in the given direction."
        dist = 0
        dr, dc = dirn
        r0, c0 = r + dr, c + dc
        while self.inbounds(r0, c0):
            dist += 1
            if get(r0, c0, self.tree_grid, math.inf) >= self.tree_grid[r][c]:
                break
            r0, c0 = r0 + dr, c0 + dc
        return dist

    def visible_trees_in_all_dirns(self, r, c):
        "Return number of trees [Left, Right, Up, Down]."
        dirns = ((0, -1), (0, 1), (-1, 0), (1, 0))
        return [self.visible_trees_in_dirn(r, c, d) for d  in dirns]

    def scenic_score(self, r, c):
        "Return scenic score for given tree."
        return functools.reduce(
            operator.mul,
            self.visible_trees_in_all_dirns(r, c),
            1
        )

    def solve_b(self):
        "Return the maximum scenic score."
        soln_b = 0
        for r, row in enumerate(self.tree_grid):
            for c, _ in enumerate(row):
                soln_b = max(soln_b, self.scenic_score(r, c))
        return soln_b


#
# Testing
#


def test_visible_dirns():
    tree_grid = TreeGrid('../test.txt')
    assert tree_grid.is_visible_dirn(1, 1) == [True, False, True, False]
    assert tree_grid.is_visible_dirn(1, 2) == [False, True, True, False]
    assert tree_grid.is_visible_dirn(1, 3) == [False, False, False, False]
    assert tree_grid.is_visible_dirn(2, 1) == [False, True, False, False]
    assert tree_grid.is_visible_dirn(2, 2) == [False, False, False, False]
    assert tree_grid.is_visible_dirn(2, 3) == [False, True, False, False]
    assert tree_grid.is_visible_dirn(3, 1) == [False, False, False, False]
    assert tree_grid.is_visible_dirn(3, 2) == [True, False, False, True]
    assert tree_grid.is_visible_dirn(3, 3) == [False, False, False, False]


def test_is_visible():
    expected = [[True, True, True, True, True],
                [True, True, True, False, True],
                [True, True, False, True, True],
                [True, False, True, False, True],
                [True, True, True, True, True]]
    tree_grid = TreeGrid('../test.txt')
    for r, row in enumerate(tree_grid.tree_grid):
        for c, _ in enumerate(row):
            assert tree_grid.is_tree_visible(r, c) == expected[r][c]


def test_soln_a():
    tree_grid = TreeGrid('../test.txt')
    assert tree_grid.solve_a() == 21



def test_visible_trees_in_dir():
    tree_grid = TreeGrid('../test.txt')
    # L, R, U, D
    result = tree_grid.visible_trees_in_all_dirns(1, 2)
    expected = [1, 2, 1, 2]
    assert result == expected
    result = tree_grid.visible_trees_in_all_dirns(3, 2)
    expected = [2, 2, 2, 1]
    assert result == expected


def test_scenic_score():
    tree_grid = TreeGrid('../test.txt')
    assert tree_grid.scenic_score(1, 2) == 4
    assert tree_grid.scenic_score(3, 2) == 8


def test_solve_b():
    tree_grid = TreeGrid('../test.txt')
    assert tree_grid.solve_b() == 8


#
# Main
#


def main():
    "Main program."
    import pyperclip
    tree_grid = TreeGrid('../input08.txt')
    soln_a = tree_grid.solve_a()
    assert soln_a == 1538
    print(f"The solution to part A is {soln_a}.")
    soln_b = tree_grid.solve_b()
    assert soln_b == 496125
    print(f"The solution to part B is {soln_b}.")
    pyperclip.copy(str(soln_b))
    print(f"{soln_b} has been placed on the clipboard.")


if __name__ == '__main__':
    main()