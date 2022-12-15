"""
Advent of Code 2022
Day 15: Beacon Exclusion Zone
jramaswami
"""


import collections
import math


Posn = collections.namedtuple('Posn', ['x', 'y'])


def manhattan_distance(a, b):
    "Return the manhattan distance between the two points."
    return abs(a.x - b.x)  + abs(a.y - b.y)


def extract_coordinates(spec):
    "Extract the part of the spec with coordinates."
    i = spec.index('x')
    tokens = spec[i:].split(', ')
    return Posn(int(tokens[0][2:]), int(tokens[1][2:]))


def read_input(filename):
    "Parse input file."
    sensors_and_beacons = []
    with open(filename) as infile:
        for line in infile:
            sensor_spec, beacon_spec = line.strip().split(': ')
            sensor = extract_coordinates(sensor_spec)
            beacon = extract_coordinates(beacon_spec)
            sensors_and_beacons.append((sensor, beacon))
    return sensors_and_beacons


def compute_covered_posns(sensors_and_beacons, row_y):
    "Compute the set of positions covered by a sensor in row_y."
    covered_posns = set()
    for s, b in sensors_and_beacons:
        m = manhattan_distance(s, b)
        x_off = 0
        p = Posn(s.x + x_off, row_y)
        while manhattan_distance(s, p) <= m:
            covered_posns.add(p)
            x_off += 1
            p = Posn(s.x + x_off, row_y)

        x_off = -1
        p = Posn(s.x + x_off, row_y)
        while manhattan_distance(s, p) <= m:
            covered_posns.add(p)
            x_off -= 1
            p = Posn(s.x + x_off, row_y)
    return covered_posns


def solve_a(sensors_and_beacons, row_y):
    "Solve part A of puzzle."
    covered_posns = compute_covered_posns(sensors_and_beacons, row_y)
    # Remove beacons in row_y.
    for _, b in sensors_and_beacons:
        if b.y == row_y and b in covered_posns:
            covered_posns.remove(b)
    return len(covered_posns)


#
# Testing
#


def test_covered_posns():
    sensors_and_beacons = read_input('../test.txt')
    row_y = 10
    expected = set(Posn(x, row_y) for x in range(-2, 25))
    result = compute_covered_posns(sensors_and_beacons, row_y)
    assert result == expected


def test_solve_a():
    sensors_and_beacons = read_input('../test.txt')
    row_y = 10
    expected = 26
    result = solve_a(sensors_and_beacons, row_y)
    assert result == expected


#
# Main
#


def main():
    "Main program."
    import pyperclip
    sensors_and_beacons = read_input('../input15.txt')
    row_y = 2000000
    soln_a = solve_a(sensors_and_beacons, row_y)
    assert soln_a == 4919281
    print(f"The solution to part A is {soln_a}.")
    pyperclip.copy(str(soln_a))
    print(f"{soln_a} has been placed on the clipboard.")


if __name__ == '__main__':
    main()
