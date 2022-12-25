"""
Advent of Code 2022
Day 25: Full of Hot Air
jramaswami
"""


import collections
from typing import *


SNAFU_DIGITS = {'=': -2, '-': -1, '0': 0, '1': 1, '2': 2}


def read_input(filename):
    "Return list of snafu numbers from input file."
    with open(filename) as infile:
        return [line.strip() for line in infile]


def snafu_to_decimal(snafu: str) -> int:
    "Convert snafu number to decimal number."
    m = 1
    decimal = 0
    for t in reversed(snafu):
        decimal += (SNAFU_DIGITS[t] * m)
        m *= 5
    return decimal


def decimal_to_snafu(decimal: int) -> str:
    "Convert a decimal number into a snafu number."
    # Convert to base 5
    place = pow(5, 19)
    base5 = collections.deque()
    decimal0 = decimal
    for i in range(20):
        t, decimal0 = divmod(decimal0, place)
        base5.append(t)
        place //= 5
        i -= 1

    # Check base 5
    x = "".join(str(i) for i in base5)
    assert decimal == int(x, 5)

    # Pad to 20 digits
    while len(base5) < 20:
        base5.appendleft(0)

    # Convert to snafu
    snafu = collections.deque('0' for _ in range(20))
    for i in range(19, -1, -1):
        if base5[i] == 5:
            # Carry
            base5[i-1] += 1
            base5[i] = 0

        if base5[i] == 4:
            base5[i-1] += 1
            snafu[i] = '-'
        elif base5[i] == 3:
            base5[i-1] += 1
            snafu[i] = '='
        else:
            snafu[i] = str(base5[i])

    # Remove leading zeros.
    while len(snafu) > 1 and snafu[0] == '0':
        snafu.popleft()

    return "".join(snafu)


def solve_a(snafus):
    "Solve part A of puzzle."
    snafus_sum = sum(snafu_to_decimal(t) for t in snafus)
    return decimal_to_snafu(snafus_sum)


#
# Testing
#


def test_snafu_to_decimal():
    with open('../snafu_to_decimal.txt') as infile:
        # Skip header.
        infile.readline()
        for line in infile:
            snafu, decimal = (t.strip() for t in line.strip().split())
            decimal = int(decimal)
            assert snafu_to_decimal(snafu) == decimal


def test_decimal_to_snafu():
    with open('../decimal_to_snafu.txt') as infile:
        # Skip header.
        infile.readline()
        for line in infile:
            decimal, snafu = (t.strip() for t in line.strip().split())
            decimal = int(decimal)
            assert decimal_to_snafu(decimal) == snafu


def test_sum_snafu():
    snafus = read_input('../test.txt')
    assert sum(snafu_to_decimal(t) for t in snafus) == 4890


def test_solve_a():
    snafus = read_input('../test.txt')
    assert solve_a(snafus) == '2=-1=0'



#
# Main
#


def main():
    "Main program."
    import pyperclip
    snafus = read_input('../input25.txt')
    soln_a = solve_a(snafus)
    print(f"The solution to part A is {soln_a}.")
    pyperclip.copy(soln_a)
    print(f"{soln_a} has been placed on the clipboard.")


if __name__ == '__main__':
    main()
