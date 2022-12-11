"""
Advent of Code 2022
Day 11: Monkey in the Middle
jramaswami

I had to get a hint to solve part B.
"""

from dataclasses import dataclass
from typing import *
import collections
import functools
import operator
import os


@dataclass
class Monkey:
    "Class representing a monkey."
    items: Deque[int]
    operation: Callable
    test: Callable
    truemonkey: int
    falsemonkey: int
    divisor: int
    inspected: int = 0


def parse_input(filename):
    "Parse input file into a list of monkeys."
    operations = {
        '*': operator.mul,
        '+': operator.add,
        'square': lambda x: x * x
    }
    monkeys = []
    with open(filename) as infile:
        while infile:
            # Read lines describing a single monkey.
            lines = [infile.readline().strip() for _ in range(7)]
            if not lines[0]:
                break
            # Parse the starting items.
            header, data = lines[1].split(':')
            items = collections.deque(int(i) for i in data.split(','))
            # Parse the operation performed.
            tokens = lines[2].split()
            operation = None
            if tokens[-3] == 'old' and tokens[-2] == '*' and tokens[-1] == 'old':
                operation = operations['square']
            else:
                operation = functools.partial(operations[tokens[-2]], int(tokens[-1]))
            # Parse test.
            tokens = lines[3].split()
            divisor = int(tokens[-1])
            test = functools.partial(lambda y, x: x % y, int(tokens[-1]))
            # Parse true/false monkeys.
            truemonkey = int(lines[4].split()[-1])
            falsemonkey = int(lines[5].split()[-1])

            monkeys.append(Monkey(items, operation, test, truemonkey, falsemonkey, divisor))

    return monkeys


def tick(monkeys, reduceworry=True, verbose=False):
    "Simulate one tick."
    MOD = functools.reduce(operator.mul, (m.divisor for m in monkeys), 1)
    for i, monkey in enumerate(monkeys):
        if verbose:
            print(f"Monkey {i}:")
        while monkey.items:
            item = monkey.items.popleft()
            monkey.inspected += 1
            if verbose:
                print(f"Worry level starts at {item}")
            item = monkey.operation(item)
            if verbose:
                print(f"Worry level goes to {item}")
            if reduceworry:
                item //= 3
                if verbose:
                    print(f"Worry level reduced to {item}")
            if monkey.test(item) == 0:
                if verbose:
                    print(f"{item} thrown to monkey {monkey.truemonkey}")
                monkeys[monkey.truemonkey].items.append(item % MOD)
            else:
                if verbose:
                    print(f"{item} thrown to monkey {monkey.falsemonkey}")
                monkeys[monkey.falsemonkey].items.append(item % MOD)


def simulate(monkeys, ticks, reduceworry=True):
    "Simulate for the given number of ticks."
    for _ in range(ticks):
        tick(monkeys, reduceworry=reduceworry)


def solve_a(monkeys):
    "Solve part A of puzzle."
    simulate(monkeys, 20)
    m1, m2 = sorted([m.inspected for m in monkeys], reverse=True)[:2]
    return m1 * m2


def solve_b(monkeys):
    "Solve part B of puzzle."
    simulate(monkeys, 10000, reduceworry=False)
    m1, m2 = sorted([m.inspected for m in monkeys], reverse=True)[:2]
    return m1 * m2

#
# Testing
#

def parse_expected_tick(filename):
    "Parse the expected items for each monkey for the given tick file."
    monkey_items = []
    with open(filename) as infile:
        for line in infile:
            head, data = line.split(':')
            if data.strip():
                monkey_items.append(
                    collections.deque([int(i) for i in data.strip().split(',')])
                )
            else:
                monkey_items.append(collections.deque([]))
    return monkey_items


def test_1():
    monkeys = parse_input('../test.txt')
    for i in range(1, 21):
        filename = f"../tick{i}.txt"
        tick(monkeys)
        if os.path.exists(filename):
            expected = parse_expected_tick(filename)
            result = [m.items for m in monkeys]
            assert result == expected


def test_2():
    monkeys = parse_input('../test.txt')
    simulate(monkeys, 20)
    expected = [101, 95, 7, 105]
    assert [m.inspected for m in monkeys] == expected


def test_solve_a():
    monkeys = parse_input('../test.txt')
    expected = 10605
    result = solve_a(monkeys)
    assert result == expected


def test_solve_b():
    monkeys = parse_input('../test.txt')
    expected = 2713310158
    result = solve_b(monkeys)
    assert result == expected


#
# Main
#

def main():
    "Main program."
    import pyperclip
    monkeys = parse_input('../input11.txt')
    soln_a = solve_a(monkeys)
    assert soln_a == 50830
    print(f"The solution to part A is {soln_a}.")

    monkeys = parse_input('../input11.txt')
    soln_b = solve_b(monkeys)
    assert soln_b == 14399640002
    print(f"The solution to part B is {soln_b}.")
    pyperclip.copy(str(soln_b))
    print(f"{soln_b} has been placed in the clipboard.")


if __name__ == '__main__':
    main()
