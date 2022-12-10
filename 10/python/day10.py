"""
Advent of Code 2022
Day 10: Cathode-Ray Tube
jramaswami
"""



class VM:

    def __init__(self, instructions):
        self.instructions = instructions
        self.register = 1
        self.cycles = [self.register]

    def noop(self):
        self.cycles.append(self.register)

    def addx(self, val):
        self.cycles.append(self.register)
        self.cycles.append(self.register)
        self.register += val

    def run(self):
        for instruction in self.instructions:
            tokens = instruction.strip().split()
            if tokens[0] == 'noop':
                self.noop()
            else:
                self.addx(int(tokens[1]))

    def solve_a(self):
        soln_a = 0
        cs = [20, 60, 100, 140, 180, 220]
        return sum(c * self.cycles[c] for c in cs)


class CRT:

    def __init__(self, vm_cycles):
        # Chop off the zero cycle.
        self.vm_cycles = vm_cycles[1:]
        self.image = [['.' for _ in range(40)] for _ in range(6)]
        for i, v in enumerate(vm_cycles[1:]):
            r, c = divmod(i, 40)
            if c - 1 <= v <= c + 1:
                self.image[r][c] = '#'

    def __str__(self):
        return "\n".join("".join(row) for row in self.image)


def read_instructions(filename):
    "Read instructions from input file."
    instructions = []
    with open(filename) as infile:
        instructions = infile.readlines()
    return instructions


#
# Testing
#


def test_1():
    instructions = read_instructions('../test1.txt')
    vm = VM(instructions)
    vm.run()
    expected = [1, 1, 1, 1, 4, 4]
    assert vm.cycles == expected


def test_2():
    instructions = read_instructions('../test2.txt')
    vm = VM(instructions)
    vm.run()
    expected = [(20, 21), (60, 19), (100, 18), (140, 21), (180, 16), (220, 18)]
    for i, v in expected:
        assert vm.cycles[i] == v


def test_solve_a():
    instructions = read_instructions('../test2.txt')
    vm = VM(instructions)
    vm.run()
    expected = 13140
    assert vm.solve_a() == expected


#
# Main
#


def main():
    "Main program."
    import pyperclip
    instructions = read_instructions('../input10.txt')
    vm = VM(instructions)
    vm.run()
    soln_a = vm.solve_a()
    assert soln_a == 16480
    print(f"The solution to part A is {soln_a}.")
    crt = CRT(vm.cycles)
    print(f"\n{crt}\n")
    soln_b = "PLEFULPB"
    assert soln_b == 'PLEFULPB'
    print(f"The solution to part B is {soln_b}.")
    pyperclip.copy(str(soln_b))
    print(f"{soln_b} has been placed on the clipboard.")


if __name__ == '__main__':
    main()
