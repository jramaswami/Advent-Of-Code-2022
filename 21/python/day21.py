"""
Advent of Code 2022
Day 21: Monkey Math
jramaswami
"""


import operator
import math


class Node:
    def __init__(self, name, operation=None, value=None):
        self.name = name
        self.operation = operation
        self.value = value
        self.left = None
        self.right = None

    def is_leaf(self):
        return self.left is None and self.right is None

    def get_value(self):
        if self.is_leaf():
            return self.value
        x = self.left.get_value()
        y = self.right.get_value()
        return self.operation(x, y)

    def __repr__(self):
        return f"Node({self.name})"


def read_input(filename):
    "Read input file into a tree."

    operation_functions = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': operator.floordiv
    }

    nodes = dict()
    operations = dict()
    with open(filename) as infile:
        for line in infile:
            line = line.strip()
            name, operation_clause = line.split(': ')
            operation_tokens = operation_clause.split()
            nodes[name] = Node(name)
            operations[name] = operation_tokens

    for node in nodes.values():
        operation_tokens = operations[node.name]
        if len(operation_tokens) == 1:
            assert operation_tokens[0].isnumeric()
            node.value = int(operation_tokens[0])
        else:
            assert len(operation_tokens) == 3
            node.operation = operation_functions[operation_tokens[1]]
            node.left = nodes[operation_tokens[0]]
            node.right = nodes[operation_tokens[2]]
    return nodes['root']


def solve_a(root):
    "Solve part A of puzzle."
    return root.get_value()


def set_humn(node, value):
    "Set the value of the 'humn' node."
    if node is None:
        return

    if node.name == 'humn':
        node.value = value
    else:
        set_humn(node.left, value)
        set_humn(node.right, value)


def solve_b(root):
    "Solve part B of puzzle. Binary search for the answer."
    root.operation = lambda x, y: x == y
    lo = 0
    hi = pow(10, 100)

    # Figure out which way the binary search should raise/lower range
    # based on the effect of increasing the value of the 'humn' node.
    set_humn(root, lo)
    left = root.left.get_value()
    right = root.right.get_value()
    delta0 = left - right

    set_humn(root, pow(10, 10))
    left = root.left.get_value()
    right = root.right.get_value()
    delta1 = left - right

    should_lower_range = lambda x, y: x < y
    should_raise_range = lambda x, y: x > y

    if delta0 < delta1:
        should_lower_range, should_raise_range = should_raise_range, should_lower_range

    soln_b = math.inf
    while lo <= hi:
        mid = lo + ((hi - lo) // 2)
        set_humn(root, mid)
        left = root.left.get_value()
        right = root.right.get_value()
        if should_raise_range(left, right):
            lo = mid + 1
        elif should_lower_range(left, right):
            hi = mid - 1
        else:
            soln_b = min(soln_b, mid)
            hi = mid - 1

    set_humn(root, soln_b)
    left = root.left.get_value()
    right = root.right.get_value()
    assert left == right
    return soln_b


#
# Testing
#


def test_solve_a():
    root = read_input('../test.txt')
    expected = 152
    assert solve_a(root) == expected


def test_solve_b():
    root = read_input('../test.txt')
    expected = 301
    assert solve_b(root) == expected


#
# Main
#


def main():
    "Main program."
    import pyperclip
    root = read_input('../input21.txt')
    soln_a = solve_a(root)
    print(f"The solution to part A is {soln_a}.")
    assert soln_a == 309248622142100
    soln_b = solve_b(root)
    print(f"The solution to part B is {soln_b}.")
    assert soln_b == 3757272361782
    pyperclip.copy(str(soln_b))
    print(f"{soln_b} has been placed on the clipboard.")


if __name__ == '__main__':
    main()
