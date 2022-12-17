"""
Advent of Code 2022
Day 17: Pyroclastic Flow
jramaswami
"""


ROCKS = tuple([
    tuple([(0, 0), (1, 0), (2, 0), (3, 0)]),
    tuple([(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)]),
    tuple([(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)]),
    tuple([(0, 0), (0, 1), (0, 2), (0, 3)]),
    tuple([(0, 0), (0, 1), (1, 0), (1, 1)])
])


def read_input(filename):
    "Read jets from input file."
    with open(filename) as infile:
        jets = infile.readline().strip()
    return jets


class Simulator:

    def __init__(self, jets, limit=2022, cycle_detection=False):
        self.jets = jets
        self.tower_height = -1
        self.rock_tower = set()
        self.rock_index = 0
        self.jet_index = 0
        self.falling_rock = None

        self.left_wall = 0
        self.right_wall = 7

        self.limit = limit

        self.cycle_detection = cycle_detection
        self.xs = []
        self.prev_cycles = dict()
        self.cycle_detected = False
        self.offset = 0

        self.launch_rock()

    def lateral_collision(self, falling_rock):
        "Return True if falling_rock collides with anything, laterally."
        for x, y in falling_rock:
            if x < self.left_wall or x >= self.right_wall:
                return True
            if (x, y) in self.rock_tower:
                return True
        return False

    def cannot_fall(self, falling_rock):
        "Return True if falling_rock cannot fall down any farther."
        for x, y in falling_rock:
            if y < 0:
                return True
            if (x, y) in self.rock_tower:
                return True
        return False

    def launch_rock(self):
        "Begin a new rock falling."
        # Pick next rock
        falling_rock0 = ROCKS[self.rock_index % len(ROCKS)]
        self.rock_index += 1
        # Move rock into position.
        rock_bottom = self.tower_height + 4
        self.falling_rock = tuple((x + 2, y + rock_bottom) for x, y in falling_rock0)

    def settle_rock(self):
        "Settle the current falling rock."
        # Add rock to rock tower and compute new tower height.
        for x, y in self.falling_rock:
            self.rock_tower.add((x, y))
            self.tower_height = max(self.tower_height, y)

        # Cycle detection
        if self.cycle_detection == True:
            if not self.cycle_detected:
                self.xs.append(self.falling_rock[0][0])
                if self.rock_index % len(ROCKS) == 0 and self.rock_index >= len(ROCKS) * 2:
                    i = self.rock_index - (len(ROCKS) * 2)
                    j = self.rock_index - len(ROCKS)
                    curr_cycle = (tuple(self.xs), self.jet_index % len(self.jets))
                    self.xs = []
                    if curr_cycle in self.prev_cycles:
                        self.cycle_detected = True
                        curr_rock, curr_height = self.rock_index, self.tower_height
                        prev_rock, prev_height = self.prev_cycles[curr_cycle]
                        delta_rock = curr_rock - prev_rock
                        delta_height = curr_height - prev_height

                        remaining_rocks = self.limit - curr_rock
                        cycles_added = remaining_rocks // delta_rock
                        self.rock_index += (delta_rock * cycles_added)
                        self.offset += (delta_height * cycles_added)

                    self.prev_cycles[curr_cycle] = (self.rock_index, self.tower_height)

    def tick(self):
        "Simulate a single unit of time."

        # Rocks alternate between being pushed by jet and then falling down one
        # unit.

        # See which direction the current jet is blowing.
        jet = self.jets[self.jet_index]
        self.jet_index = (self.jet_index + 1) % len(self.jets)
        dx = 1
        if jet == '<':
            dx = -1

        # First see if jet can blow
        falling_rock0 = tuple((x+dx, y) for x, y in self.falling_rock)
        if not self.lateral_collision(falling_rock0):
            self.falling_rock = falling_rock0

        # See if rock can fall.
        falling_rock0 = tuple((x, y-1) for x, y in self.falling_rock)
        if self.cannot_fall(falling_rock0):
            self.settle_rock()
            self.launch_rock()
        else:
            self.falling_rock = falling_rock0

    def solve(self):
        "Solve puzzle."
        prev_rock_index = 0
        while self.rock_index <= self.limit:
            self.tick()
            prev_rock_index = self.rock_index
        return self.tower_height + self.offset + 1

    def __str__(self):
        lines = []
        # Find top of display
        top = self.tower_height
        for _, y in self.falling_rock:
            top = max(top, y)

        for y in range(top, -1, -1):
            row = ['.' for _ in range(self.right_wall)]
            for x in range(self.left_wall, self.right_wall):
                if (x, y) in self.falling_rock:
                    row[x] = '@'
                if (x, y) in self.rock_tower:
                    row[x] = '#'
            line = ''.join(row)
            lines.append(f"|{line}|")
        lines.append('+' + ('-' * self.right_wall) + '+')
        lines.append(f"Time = {self.clock}")
        return "\n".join(lines)


def test_solve_a():
    jets = read_input('../test.txt')
    simulator = Simulator(jets)
    expected = 3068
    result = simulator.solve()
    assert result == expected


def test_cycle_detection():
    jets = read_input('../test.txt')
    for limit in range(10000, 100000, 1000001 ):
        simulator = Simulator(jets, limit)
        soln_x = simulator.solve()
        simulator0 = Simulator(jets, limit, True)
        soln_y = simulator.solve()
        assert soln_x == soln_y


def test_solve_b():
    jets = read_input('../test.txt')
    simulator = Simulator(jets, 1000000000000, cycle_detection=True)
    expected = 1514285714288
    result = simulator.solve()
    assert result == expected


#
# Main
#


def main():
    "Main program."
    import pyperclip
    jets = read_input('../input17.txt')
    simulator_a = Simulator(jets)
    soln_a = simulator_a.solve()
    print(f"The solution to part A is {soln_a}.")
    assert soln_a == 3071
    simulator_b = Simulator(jets, limit=1000000000000, cycle_detection=True)
    soln_b = simulator_b.solve()
    print(f"The solution to part B is {soln_b}.")
    assert soln_b == 1523615160362
    pyperclip.copy(str(soln_b))
    print(f"{soln_b} has been placed in the clipboard.")


if __name__ == '__main__':
    main()
