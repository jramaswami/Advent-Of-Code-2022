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
    with open(filename) as infile:
        jets = infile.readline().strip()
    return jets


class Simulator:

    def __init__(self, jets):
        self.jets = jets
        self.tower_height = -1
        self.rock_tower = set()
        self.clock = 0
        self.rock_index = 0
        self.falling_rock = None

        self.left_wall = 0
        self.right_wall = 7

        self.launch_rock()

        self.jet_index = 0


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
        # print(f"Launching rock {self.rock_index} ...")
        # print(f"Current height {self.tower_height} ...")
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

    def tick(self):
        "Simulate a single unit of time."
        self.clock += 1

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
            # print('rock moved', jet)

        # See if rock can fall.
        falling_rock0 = tuple((x, y-1) for x, y in self.falling_rock)
        if self.cannot_fall(falling_rock0):
            self.settle_rock()
            self.launch_rock()
        else:
            # print('rock moved v')
            self.falling_rock = falling_rock0

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


def solve_a(jets, limit=2022):
    "Solve part A of puzzle."
    simulator = Simulator(jets)
    while simulator.rock_index <= limit:
        simulator.tick()
    return simulator.tower_height + 1


def test_solve_a():
    jets = read_input('../test.txt')
    expected = 3068
    result = solve_a(jets)
    assert result == expected


#
# Main
#


def main():
    "Main program."
    import pyperclip
    jets = read_input('../input17.txt')
    soln_a = solve_a(jets)
    print(f"The solution to part A is {soln_a}.")
    assert soln_a == 3071
    pyperclip.copy(str(soln_a))
    print(f"{soln_a} has been placed in the clipboard.")

if __name__ == '__main__':
    main()
