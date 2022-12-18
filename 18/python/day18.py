"""
Advent of Code 2022
Day 18: Boiling Boulders
jramaswami
"""


import collections


Droplet = collections.namedtuple('Droplet', ['x', 'y', 'z'])


def read_input(filename):
    "Read input file and parse into list of droplets."
    droplets = []
    with open(filename) as infile:
        for line in infile:
            droplet = Droplet(*(int(n) for n in line.strip().split(',')))
            droplets.append(droplet)
    return droplets


def solve_a(droplets):
    "Solve part A of puzzle."
    soln_a = 6 * len(droplets)
    offsets = ((0, 0, 1), (0, 0, -1),
               (0, 1, 0), (0, -1, 0),
               (1, 0, 0), (-1, 0, 0))
    for a in droplets:
        for dx, dy, dz in offsets:
            a0 = Droplet(a.x + dx, a.y + dy, a.z + dz)
            if a0 in droplets:
                soln_a -= 1
    return soln_a


def solve_b(droplets):
    "Flood fill to solve part B of puzzle."
    init_posn = Droplet(0, 0, 0)
    assert init_posn not in droplets
    offsets = ((0, 0, 1), (0, 0, -1),
               (0, 1, 0), (0, -1, 0),
               (1, 0, 0), (-1, 0, 0))

    max_x = max(p.x for p in droplets)
    max_y = max(p.y for p in droplets)
    max_z = max(p.z for p in droplets)
    max_dim = max(max_x, max_y, max_z) + 2

    def inbounds(p):
        "Limit the scope of the map to just enough to surround droplets."
        return (
            p.x >= -2 and p.x < max_dim and
            p.y >= -2 and p.y < max_dim and
            p.z >= -2 and p.z < max_dim
        )

    def neighbors(p):
        "Helper generator for neighbors to p."
        for dx, dy, dz in offsets:
            p0 = Droplet(p.x + dx, p.y + dy, p.z + dz)
            if inbounds(p0):
                yield p0

    soln_b = 0
    visited = set()
    visited.add(init_posn)
    queue = collections.deque()
    queue.append(init_posn)
    while queue:
        p = queue.popleft()
        for p0 in neighbors(p):
            if p0 in droplets:
                soln_b += 1
            elif p0 not in visited:
                visited.add(p0)
                queue.append(p0)
    return soln_b


# Testing
#


def test_soln_a():
    droplets = read_input('../test.txt')
    expected = 64
    result = solve_a(droplets)
    assert result == expected


def test_soln_b():
    droplets = read_input('../test.txt')
    expected = 58
    result = solve_b(droplets)
    assert result == expected


#
# Main
#


def main():
    "Main program."
    import pyperclip
    droplets = read_input('../input18.txt')
    soln_a = solve_a(droplets)
    print(f"The solution to part A is {soln_a}.")
    assert soln_a == 4628
    soln_b = solve_b(droplets)
    print(f"The solution to part B is {soln_b}.")
    assert soln_b == 2582
    pyperclip.copy(soln_b)
    print(f"{soln_b} has been placed in the clipboard.")


if __name__ == '__main__':
    main()
