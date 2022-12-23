"""
Advent of Code 2022
Day 23: Unstable Diffusion
jramaswami
"""


import collections
import math
import os


Posn = collections.namedtuple('Posn', ['row', 'col'])
Posn.__add__ = lambda x, y: Posn(x.row + y.row, x.col + y.col)


OFFSETS = {
    'N': Posn(-1, 0), 'S': Posn(1, 0), 'W': Posn(0, -1), 'E':  Posn(0, 1),
    'NE': Posn(-1, 1), 'NW': Posn(-1, -1),'SE': Posn(1, 1), 'SW': Posn(1, -1)
}


def read_input(filename):
    with open(filename) as infile:
        return [list(line.strip()) for line in infile]


class Grid:

    def __init__(self, grid, verbose=False):
        self.verbose = verbose
        self.height = len(grid)
        self.width = len(grid[0])
        self.moves = collections.deque(
            [('N', 'NE', 'NW'), ('S', 'SE', 'SW'),
             ('W', 'NW', 'SW'), ('E', 'NE', 'SE')]
        )
        self.elves = set()
        for r, row in enumerate(grid):
            for c, val in enumerate(row):
                if val == '#':
                    self.elves.add(Posn(r, c))

    def log(self, msg):
        if self.verbose:
            print(msg)

    def propose(self, posn):
        self.log(f"propose({posn=})")
        # Each Elf considers the eight positions adjacent to themself. If no
        # other Elves are in one of those eight positions, the Elf does not do
        # anything during this round.
        neighbors = {}
        for k, o in OFFSETS.items():
            p = posn+o
            if p in self.elves:
                neighbors[k] = p
            else:
                neighbors[k] = None
        self.log(f"{neighbors=}")
        if all(n is None for n in neighbors.values()):
            self.log(f"Not moving because I have no neighbors.")
            return None
        # Otherwise, the Elf looks in each of four directions in the following
        # order and proposes moving one step in the first valid direction:
        # If there is no Elf in the N, NE, or NW adjacent positions, the Elf
        # proposes moving north one step.
        # Etc.
        for ms in self.moves:
            self.log(f"Considering {ms=}: {[neighbors[n] for n in ms]}")
            if all(neighbors[n] is None for n in ms):
                posn0 = posn + OFFSETS[ms[0]]
                self.log(f"That's the one! I'm moving {ms[0]} to {posn0}.")
                return posn0
        return None

    def tick(self):
        # During the first half of each round, each Elf ... roposes moving one
        # step in the first valid direction.
        self.log('Making proposals ...')
        proposals = collections.defaultdict(list)
        for posn in self.elves:
            prop = self.propose(posn)
            proposals[prop].append(posn)
        # After each Elf has had a chance to propose a move, the second half of
        # the round can begin. Simultaneously, each Elf moves to their proposed
        # destination tile if they were the only Elf to propose moving to that
        # position. If two or more Elves propose moving to the same position,
        # none of those Elves move.
        self.log(f"{proposals=}")
        self.log('Making moves ...')
        elves0 = set()
        for to_posn in proposals:
            if len(proposals[to_posn]) == 1:
                self.log(f"Moving {proposals[to_posn][0]} to {to_posn}")
                elves0.add(to_posn)
            else:
                self.log(f"Elves trying to move to {to_posn} collide:")
                for from_posn in proposals[to_posn]:
                    self.log(f"{from_posn} cannot move to {to_posn}")
                    elves0.add(from_posn)
        self.elves = elves0
        # Finally, at the end of the round, the first direction the Elves
        # considered is moved to the end of the list of directions.
        self.log('Rotating moves ...')
        self.log(f"{self.moves}")
        self.moves.rotate(-1)
        self.log(f"{self.moves}")

    def get_grid(self):
        grid = []
        for r in range(self.height):
            row = []
            for c in range(self.width):
                if Posn(r, c) in self.elves:
                    row.append('#')
                else:
                    row.append('.')
            grid.append(row)
        return grid

    def solve_a(self):
        for _ in range(10):
            self.tick()

        # Find dimensions of rectangle.
        min_row, max_row = math.inf, -math.inf
        min_col, max_col = math.inf, -math.inf
        for r, c in self.elves:
            min_row = min(min_row, r)
            max_row = max(max_row, r)
            min_col = min(min_col, c)
            max_col = max(max_col, c)

        height = max_row - min_row + 1
        width = max_col - min_col + 1
        return (height * width) - len(self.elves)


    def __str__(self):
        return "\n".join("".join(row) for row in self.get_grid())


#
# Testing
#

def test_propose():
    grid = Grid(read_input('../test1.txt'), verbose=True)

    # Round 1
    elf = Posn(1, 2)
    expected = elf + OFFSETS['N']
    assert grid.propose(elf) == expected

    elf = Posn(1, 3)
    expected = elf + OFFSETS['N']
    assert grid.propose(elf) == expected

    elf = Posn(4, 2)
    expected = elf + OFFSETS['N']
    assert grid.propose(elf) == expected

    elf = Posn(4, 3)
    expected = elf + OFFSETS['N']
    assert grid.propose(elf) == expected

    elf = Posn(2, 2)
    expected = elf + OFFSETS['S']
    assert grid.propose(elf) == expected

    grid.tick()
    expected = read_input('../expected1_1.txt')
    assert grid.get_grid() == expected

    # Round 2

    print('*' * 50, 'Round 2 ...')
    elf = Posn(0, 2)
    expected = elf + OFFSETS['S']
    assert grid.propose(elf) == expected

    elf = Posn(0, 3)
    expected = elf + OFFSETS['S']
    assert grid.propose(elf) == expected

    elf = Posn(4, 2)
    expected = elf + OFFSETS['S']
    assert grid.propose(elf) == expected

    elf = Posn(2, 2)
    expected = elf + OFFSETS['W']
    assert grid.propose(elf) == expected

    elf = Posn(3, 3)
    expected = elf + OFFSETS['E']
    assert grid.propose(elf) == expected

    grid.tick()
    expected = read_input('../expected1_2.txt')
    assert grid.get_grid() == expected

    # Round 3
    print('*' * 50, 'Round 3 ...')
    print(str(grid))

    elf = Posn(5, 2)
    expected = None
    assert grid.propose(elf) == expected

    grid.tick()
    expected = read_input('../expected1_3.txt')
    assert grid.get_grid() == expected

def test_tick_1():
    grid = Grid(read_input('../test1.txt'))
    for t in range(1, 11):
        grid.tick()
        expected_filename = f"../expected1_{t}.txt"
        if os.path.exists(expected_filename):
            expected = read_input(expected_filename)
            print('Expected:')
            print("\n".join("".join(row) for row in expected))
            print('Actual:')
            print(str(grid))
            assert grid.get_grid() == expected


def test_tick_2():
    grid = Grid(read_input('../test2.txt'), verbose=False)
    for t in range(1, 11):
        grid.tick()
        expected_filename = f"../expected2_{t}.txt"
        if os.path.exists(expected_filename):
            expected = read_input(expected_filename)
            assert grid.get_grid() == expected


def test_solve_a():
    grid = Grid(read_input('../test2.txt'), verbose=False)
    assert grid.solve_a() == 110


#
# Main
#


def main():
    "Main program."
    import pyperclip
    grid = Grid(read_input('../input23.txt'))
    soln_a = grid.solve_a()
    print(f"The solution to part A is {soln_a}.")
    pyperclip.copy(str(soln_a))
    assert soln_a == 4025
    print(f"{soln_a} has been placed in the clipboard.")


if __name__ == '__main__':
    main()
