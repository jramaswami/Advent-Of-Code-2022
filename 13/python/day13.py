"""
Advent of Code 2022
Day 13: Distress Signal
jramaswami
"""


import functools
import itertools
import math


OK, UNKNOWN, NOTOK = -1, 0, 1


def tokenize(line):
    "Generator to tokenize the given line."
    line = line.strip()
    i = 0
    val = None
    while i < len(line):
        if line[i] in '[]':
            if val is not None:
                yield val
                val = None
            yield line[i]
        elif line[i] == ',':
            if val is not None:
                yield val
                val = None
        else:
            if val is None:
                val = 0
            val *= 10
            val += int(line[i])
        i += 1


def parse(tokens):
    "Parse tokens into list of lists."
    stack = []
    for token in tokens:
        if token == '[':
            stack.append([])
        elif token == ']':
            l = stack.pop()
            if len(stack) == 0:
                return l
            stack[-1].append(l)
        else:
            stack[-1].append(token)
    return stack[-1]


def read_input(filename):
    "Read input data from file."
    packets = []
    with open(filename) as infile:
        lines = infile.readlines()
        for i in range(0, len(lines), 3):
            packet = []
            # packet.append(parse(tokenize(lines[i])))
            # packet.append(parse(tokenize(lines[i+1])))
            packet.append(eval(lines[i]))
            packet.append(eval(lines[i+1]))
            packets.append(packet)
    return packets


def compare(left, right):
    "Compare left and right."
    # If both values are integers, the lower integer should come first. If the
    # left integer is lower than the right integer, the inputs are in the right
    # order. If the left integer is higher than the right integer, the inputs
    # are not in the right order. Otherwise, the inputs are the same integer;
    # continue checking the next part of the input.
    if isinstance(left, int) and isinstance(right, int):
        if left > right:
            return NOTOK
        if left < right:
            return OK
        return UNKNOWN

    # If exactly one value is an integer, convert the integer to a list which
    # contains that integer as its only value, then retry the comparison. For
    # example, if comparing [0,0,0] and 2, convert the right value to [2] (a
    # list containing 2); the result is then found by instead comparing [0,0,0]
    # and [2].
    if isinstance(left, list) and isinstance(right, int):
        return compare(left, [right])
    if isinstance(left, int) and isinstance(right, list):
        return compare([left], right)

    # If both values are lists, compare the first value of each list, then the
    # second value, and so on. If the left list runs out of items first, the
    # inputs are in the right order. If the right list runs out of items first,
    # the inputs are not in the right order. If the lists are the same length
    # and no comparison makes a decision about the order, continue checking the
    # next part of the input.
    for i, _ in enumerate(left):
        if i >= len(right):
            return NOTOK
        result = compare(left[i], right[i])
        if result != UNKNOWN:
            return result
    if len(left) < len(right):
        return OK
    return UNKNOWN


def solve_a(packets):
    "Solve part A of puzzle."
    soln_a = 0
    for i , p in enumerate(packets):
        if compare(*p) == OK:
            soln_a += (i + 1)
    return soln_a


def flatten_packets(packets):
    "Flatten packets, add extra packets, and return sorted list."
    flat_packets = [[[2]], [[6]]]
    for left, right in packets:
        flat_packets.append(left)
        flat_packets.append(right)
    flat_packets.sort(key=functools.cmp_to_key(compare))
    return flat_packets


def solve_b(packets):
    "Solve part B of puzzle."
    flat_packets = flatten_packets(packets)
    i = flat_packets.index([[2]]) + 1
    j = flat_packets.index([[6]]) + 1
    return i * j


#
# Testing
#


def test_parse():
    expected = [
        [[1,1,3,1,1], [1,1,5,1,1]],
        [[[1],[2,3,4]], [[1],4]],
        [[9], [[8,7,6]]],
        [[[4,4],4,4], [[4,4],4,4,4]],
        [[7,7,7,7], [7,7,7]],
        [[], [3]],
        [[[[]]], [[]]],
        [[1,[2,[3,[4,[5,6,7]]]],8,9], [1,[2,[3,[4,[5,6,0]]]],8,9]]
    ]
    result = read_input('../test.txt')
    assert len(result) == len(expected)
    assert result == expected


def test_compare():
    packets = read_input('../test.txt')
    expected = [OK, OK, NOTOK, OK, NOTOK, OK, NOTOK, NOTOK]
    for p, e in zip(packets, expected):
        assert compare(*p) == e


def test_solve_a():
    packets = read_input('../test.txt')
    expected = 13
    result = solve_a(packets)
    assert result == expected


def test_flatten_packets():
    packets = read_input('../test.txt')
    flat_packets = flatten_packets(packets)
    expected = [
        [],
        [[]],
        [[[]]],
        [1,1,3,1,1],
        [1,1,5,1,1],
        [[1],[2,3,4]],
        [1,[2,[3,[4,[5,6,0]]]],8,9],
        [1,[2,[3,[4,[5,6,7]]]],8,9],
        [[1],4],
        [[2]],
        [3],
        [[4,4],4,4],
        [[4,4],4,4,4],
        [[6]],
        [7,7,7],
        [7,7,7,7],
        [[8,7,6]],
        [9],
    ]
    assert flat_packets == expected


def test_solve_b():
    packets = read_input('../test.txt')
    expected = 140
    assert solve_b(packets) == expected


#
# Main
#


def main():
    "Main program."
    import pyperclip
    packets = read_input('../input13.txt')
    # packets = read_input('../test.txt')
    soln_a = solve_a(packets)
    assert soln_a == 6101
    print(f"The solution to part A is {soln_a}.")
    soln_b = solve_b(packets)
    assert soln_b == 21909
    print(f"The solution to part B is {soln_b}.")
    pyperclip.copy(str(soln_b))
    print(f"{soln_b} has been placed on the clipboard.")


if __name__ == '__main__':
    main()
