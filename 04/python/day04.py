"""
Advent of Code 2022
Day 4: Camp Cleanup
jramaswami
"""


def parse_pair_assignment(assignment):
    "Parse a pair assignment into a tuple."
    return tuple(int(x) for x in assignment.split('-'))


def read_input(filename):
    "Read input file and return list of pair assignments."
    pair_assignments = []
    with open(filename) as infile:
        for line in infile:
            a, b = line.strip().split(',')
            pair_assignment = (
                parse_pair_assignment(a),
                parse_pair_assignment(b)
            )
            pair_assignments.append(pair_assignment)
    return pair_assignments


def fully_contains(pair_assignment):
    "Return True if one section assignment contains the other."
    a, b = pair_assignment
    return (
        a[0] <= b[0] and b[1] <= a[1] or
        b[0] <= a[0] and a[1] <= b[1]
    )


def solve_a(pair_assignments):
    "Solve part a of puzzle."
    return sum(fully_contains(p) for p in pair_assignments)


def overlaps(pair_assignment):
    "Return True if segment assignments overlap."
    a, b = pair_assignment
    return a[1] >= b[0] and b[1] >= a[0]


def solve_b(pair_assignments):
    "Solve part b of puzzle."
    return sum(overlaps(p) for p in pair_assignments)


#
# Testing
#


def test_1():
    "Test fully_contains()."
    expected = [False, False, False, True, True, False]
    pair_assignments = read_input('../test.txt')
    result = [fully_contains(p) for p in pair_assignments]
    assert result == expected


def test_2():
    "Test solve_a()."
    expected = 2
    pair_assignments = read_input('../test.txt')
    assert solve_a(pair_assignments) == expected


def test_3():
    "Test overlaps()."
    expected = [False, False, True, True, True, True]
    pair_assignments = read_input('../test.txt')
    result = [overlaps(p) for p in pair_assignments]
    assert result == expected


def test_4():
    "Test solve_b()."
    expected = 4
    pair_assignments = read_input('../test.txt')
    assert solve_b(pair_assignments) == expected


#
# Main
#


def main():
    "Main program."
    import pyperclip
    pair_assignments = read_input('../input04.txt')
    soln_a = solve_a(pair_assignments)
    assert soln_a == 498
    print(f"{soln_a} assignment pairs have one range fully containing the other.")
    soln_b = solve_b(pair_assignments)
    assert soln_b == 859
    print(f"{soln_b} assignment pairs have ranges that overlap.")
    pyperclip.copy(str(soln_b))
    print(f"{soln_b} has been placed in the clipboard.")


if __name__ == '__main__':
    main()