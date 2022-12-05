"""
Advent of Code 2022
Day 5: Supply Stacks
jramaswami
"""

import string


def read_file(filename):
    "Return list of lines from filename."
    with open(filename) as infile:
        lines = infile.readlines()
    return lines


def find_blank_line(lines):
    "Return the index of the blank line."
    for i, line in enumerate(lines):
        if not line.strip():
            return i
    return -1


def partition_file(lines):
    "Partitition lines into the stack description and rearrangment procedure."
    # Find the first blank line.
    mid = find_blank_line(lines)
    assert mid >= 0
    # Remove the newline from all lines returned.
    return [l[:-1] for l in lines[:mid]], [l.strip() for l in lines[mid+1:]]


def parse_stacks(stack_lines):
    "Parse the stack input."
    stack = []
    for line in stack_lines[:-1]:
        for i, j in enumerate(range(1, len(line), 4)):
            while i >= len(stack):
                stack.append([])
            if line[j] in string.ascii_uppercase:
                stack[i].append(line[j])
    return [s[::-1] for s in stack]


def parse_instruction(instruction):
    "Parse instruction int count, source, sink."
    tokens = instruction.split()
    return tuple(int(tokens[t]) for t in [1, 3, 5])


def tick_a(stacks, instruction):
    "Perform one tick (instruction) of simulation a."
    count, source, sink = parse_instruction(instruction)
    for _ in range(count):
        stacks[sink-1].append(stacks[source-1].pop())


def tick_b(stacks, instruction):
    "Perform one tick (instruction) of simulation b."
    count, source, sink = parse_instruction(instruction)
    stacks[sink-1].extend(stacks[source-1][-count:])
    stacks[source-1] = stacks[source-1][:-count]


def simulate(stacks, instructions, tick_fn):
    "Simulate with the given tick function."
    for instruction in instructions:
        tick_fn(stacks, instruction)
    return stacks


def solve(lines, part):
    "Solve the given part of the puzzle."
    tick_fn = (tick_a if part == 'a' else tick_b)
    stack_lines, instructions = partition_file(lines)
    stacks = parse_stacks(stack_lines)
    simulate(stacks, instructions, tick_fn)
    return "".join(s[-1] for s in stacks)


#
# Testing
#


def test_find_blank_line():
    lines = read_file('../test.txt')
    assert find_blank_line(lines) == 4
    lines = read_file('../input05.txt')
    assert find_blank_line(lines) == 9


def test_parse_stacks():
    lines = read_file('../test.txt')
    stack_lines, _ = partition_file(lines)
    stacks = parse_stacks(stack_lines)
    expected = [['Z', 'N'], ['M', 'C', 'D'], ['P']]
    assert stacks == expected


def test_tick_a():
    lines = read_file('../test.txt')
    stack_lines, instructions = partition_file(lines)
    stacks = parse_stacks(stack_lines)
    for i, line in enumerate(instructions):
        tick_a(stacks, line)
        expected = parse_stacks(read_file(f"../tick{i+1}_a.txt"))
        assert stacks == expected


def test_simulate_a():
    lines = read_file('../test.txt')
    stack_lines, instructions = partition_file(lines)
    stacks = parse_stacks(stack_lines)
    simulate(stacks, instructions, tick_a)
    expected = parse_stacks(read_file(f"../tick4_a.txt"))
    assert stacks == expected


def test_solve_a():
    lines = read_file('../test.txt')
    assert solve(lines, 'a') == 'CMZ'


def test_tick_b():
    lines = read_file('../test.txt')
    stack_lines, instructions = partition_file(lines)
    stacks = parse_stacks(stack_lines)
    for i, line in enumerate(instructions):
        tick_b(stacks, line)
        expected = parse_stacks(read_file(f"../tick{i+1}_b.txt"))
        assert stacks == expected


def test_simulate_b():
    lines = read_file('../test.txt')
    stack_lines, instructions = partition_file(lines)
    stacks = parse_stacks(stack_lines)
    simulate(stacks, instructions, tick_b)
    expected = parse_stacks(read_file(f"../tick4_b.txt"))
    assert stacks == expected


def test_solve_b():
    lines = read_file('../test.txt')
    assert solve(lines, 'b') == 'MCD'


def main():
    "Main program."
    import pyperclip
    lines = read_file('../input05.txt')
    soln_a = solve(lines, 'a')
    assert soln_a == 'CFFHVVHNC'
    print(f"The message for part A is {soln_a}")
    soln_b = solve(lines, 'b')
    assert soln_b == 'FSZWBPTBG'
    print(f"The message for part B is {soln_b}")
    pyperclip.copy(soln_b)
    print(f"{soln_b} has been placed in the clipboard.")


if __name__ == '__main__':
    main()