"""
Advent of Code 2022
Day 15: Beacon Exclusion Zone
jramaswami
"""


import collections
import math
import tqdm


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


def row_coverage(sensor, md_limit, row_y):
    "Compute the interval for which the sensor covers row_y."
    off = md_limit - abs(sensor.y - row_y)
    if off >= 0:
        return (sensor.x - off, sensor.x + off)


def compute_covered_intervals(sensors_and_beacons, row_y):
    "Compute the set of intervals covered by a sensor in row_y."
    intervals = []
    for s, b in sensors_and_beacons:
        m = manhattan_distance(s, b)
        interval = row_coverage(s, m, row_y)
        if interval is not None:
            intervals.append(interval)

    # Merge intervals
    intervals.sort()
    merged_intervals = [intervals[0]]
    for interval in intervals[1:]:
        if interval[0] <= merged_intervals[-1][1] + 1:
            merged_intervals[-1] = (
                merged_intervals[-1][0],
                max(merged_intervals[-1][1], interval[1])
            )
        else:
            merged_intervals.append(interval)
    return merged_intervals


def solve_a(sensors_and_beacons, row_y):
    "Solve part A of puzzle."
    covered_interval = compute_covered_intervals(sensors_and_beacons, row_y)
    assert len(covered_interval) == 1
    min_x, max_x = covered_interval[0]
    # Remove the beacons from the count.
    beacons_in_row = set()
    for _, b in sensors_and_beacons:
        if b.y == row_y and min_x <= b.x <= max_x:
            beacons_in_row.add(b.x)
    return (max_x - min_x + 1) - len(beacons_in_row)



def find_missing_beacon(sensors_and_beacons, mn, mx):
    "Find the coordinates of the missing beacon."
    ys = []
    for row_y in tqdm.tqdm(range(mn, mx)):
        covered_intervals = compute_covered_intervals(sensors_and_beacons, row_y)
        if len(covered_intervals) > 1:
            ys.append((row_y, covered_intervals))
    assert len(ys) == 1
    beacon_y, row_intervals = ys[0]
    assert len(row_intervals) == 2
    beacon_x = row_intervals[0][1]+1
    return Posn(beacon_x, beacon_y)


def solve_b(sensors_and_beacons, mn, mx):
    "Solve part B of puzzle."
    multiplier = 4000000
    beacon_x, beacon_y = find_missing_beacon(sensors_and_beacons, mn, mx)
    return (beacon_x * multiplier) + beacon_y


#
# Testing
#


def test_covered_intervals():
    sensors_and_beacons = read_input('../test.txt')
    row_y = 10
    expected = set(Posn(x, row_y) for x in range(-2, 25))
    covered_intervals = compute_covered_intervals(sensors_and_beacons, row_y)
    assert len(covered_intervals) == 1
    assert covered_intervals == [(-2, 24)]


def test_solve_a():
    sensors_and_beacons = read_input('../test.txt')
    row_y = 10
    expected = 26
    result = solve_a(sensors_and_beacons, row_y)
    assert result == expected


def test_find_beacon():
    sensors_and_beacons = read_input('../test.txt')
    mn, mx = 0, 20
    expected = Posn(14, 11)
    result = find_missing_beacon(sensors_and_beacons, mn, mx)
    assert result == expected


def test_solve_b():
    sensors_and_beacons = read_input('../test.txt')
    mn, mx = 0, 20
    expected = 56000011
    result = solve_b(sensors_and_beacons, mn, mx)
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
    mn, mx = 0, 4000000
    soln_b = solve_b(sensors_and_beacons, mn, mx)
    assert soln_b == 12630143363767
    print(f"The solution to part B is {soln_b}.")
    pyperclip.copy(str(soln_b))
    print(f"{soln_b} has been placed on the clipboard.")


if __name__ == '__main__':
    main()
