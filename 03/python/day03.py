"""
Advent of Code 2022
Day 3: Rucksack Reorganization
jramaswami
"""

import string


ITEM_PRIORITIES = {c: i+1 for i, c in enumerate(string.ascii_letters)}


def read_rucksacks(filename):
    "Read rucksacks from the given file."
    rucksacks = []
    with open(filename) as infile:
        for line in infile:
            rucksacks.append(line.strip())
    return rucksacks


def get_compartment_overlap(rucksack):
    "Compute the overlap between the rucksacks two compartments."
    mid = len(rucksack) // 2
    left = set(rucksack[:mid])
    right = set(rucksack[mid:])
    overlap = set(string.ascii_letters)
    overlap.intersection_update(left, right)
    assert len(overlap) == 1
    return list(overlap)[0]


def solve_a(rucksacks):
    "Solve part a of puzzle."
    return sum(ITEM_PRIORITIES[get_compartment_overlap(r)] for r in rucksacks)


def get_badges(rucksacks):
    "Get the badges from the list of rucksacks."
    badges = []
    curr_overlap = set(string.ascii_letters)
    for i, r in enumerate(rucksacks):
        if i > 0 and i % 3 == 0:
            assert len(curr_overlap) == 1
            badges.append(list(curr_overlap)[0])
            curr_overlap = set(string.ascii_letters)
        curr_overlap.intersection_update(set(r))
    assert len(curr_overlap) == 1
    badges.append(list(curr_overlap)[0])
    return badges


def solve_b(rucksacks):
    "Solve part b of puzzle."
    return sum(ITEM_PRIORITIES[b] for b in get_badges(rucksacks))


#
# Testing
#


def test_compartment_overlap():
    rucksacks = read_rucksacks('../test.txt')
    expected = ['p', 'L', 'P', 'v', 't', 's']
    for r, e in zip(rucksacks, expected):
        assert get_compartment_overlap(r) == e


def test_rucksack_priority():
    rucksacks = read_rucksacks('../test.txt')
    expected = [16, 38, 42, 22, 20, 19]
    for r, e in zip(rucksacks, expected):
        o = get_compartment_overlap(r)
        assert ITEM_PRIORITIES[o] == e


def test_solve_a():
    rucksacks = read_rucksacks('../test.txt')
    expected = 157
    assert solve_a(rucksacks) == expected


def test_get_badges():
    rucksacks = read_rucksacks('../test.txt')
    expected = ['r','Z']
    assert get_badges(rucksacks) == expected


def test_solve_b():
    rucksacks = read_rucksacks('../test.txt')
    expected = 70
    assert solve_b(rucksacks) == expected


#
# Main
#


def main():
    import pyperclip
    rucksacks = read_rucksacks('../input03.txt')
    soln_a = solve_a(rucksacks)
    assert soln_a == 7716
    print(f"The solution to part A is {soln_a}.")
    soln_b = solve_b(rucksacks)
    assert soln_b == 2973
    print(f"The solution to part B is {soln_b}.")
    pyperclip.copy(str(soln_b))
    print(f"{soln_b} has been placed in clipboard.")


if __name__ == '__main__':
    main()