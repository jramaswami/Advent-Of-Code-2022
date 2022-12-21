"""
Advent of Code 2022
Day 21: Monkey Math
jramaswami
"""

# 152 is too low.

import operator


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
        if not self.is_leaf() and self.value is None:
            self.value = self.operation(
                self.left.get_value(), self.right.get_value()
            )
        return self.value

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
    return root.get_value()


#
# Testing
#


def test_solve_a():
    root = read_input('../test.txt')
    expected = 152
    assert solve_a(root) == expected


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
    pyperclip.copy(str(soln_a))
    print(f"{soln_a} has been placed on the clipboard.")


if __name__ == '__main__':
    main()
