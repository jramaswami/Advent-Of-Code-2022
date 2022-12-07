"""
Advent of Code 2022
Day 7: No Space Left On Device
jramaswami
"""


class Node:

    DIR = 0
    FILE = 1

    def __init__(self, name, node_type=DIR, size=-1):
        self.name = name
        self.size = size
        self.children = []
        self.type = node_type

    def get_child(self, child_name):
        for child in self.children:
            if child.name == child_name:
                return child

    def add_child(self, child):
        self.children.append(child)

    def get_size(self):
        if self.size < 0:
            self.size = sum(c.get_size() for c in self.children)
        return self.size

    def __repr__(self):
        return f"Node({self.name})"


def find_node(root, node_name):
    "Return node with given node_name."

    def find_node0(node):
        "Internal helper fn to recursively search for node."
        if node.name == node_name:
            return node

        if node.type == Node.FILE:
            return None

        for child in node.children:
            result = find_node0(child)
            if result:
                return result
        return None

    return find_node0(root)


def parse_tree(lines):
    "Parse the director tree from the input."
    root = Node('/')
    stack = [root]
    # Skip line that goes to /
    for line in lines[1:]:
        tokens = line.strip().split()
        if tokens[0] == '$' and tokens[1] == 'cd':
            if tokens[2] == '..':
                stack.pop()
            else:
                child = stack[-1].get_child(tokens[2])
                stack.append(child)
        elif tokens[0] == '$' and tokens[1] == 'ls':
            pass
        elif tokens[0] == 'dir':
            stack[-1].add_child(Node(tokens[1], Node.DIR))
        elif tokens[0].isnumeric():
            stack[-1].add_child(Node(tokens[1], Node.FILE, int(tokens[0])))
    return root


def tree_to_lines(node, level, acc):
    "Format tree into lines where left padding indicates level."
    padding = '  ' * level
    if node.type == Node.FILE:
        acc.append((f"{padding}- {node.name} (file, size={node.size})"))
    else:
        acc.append((f"{padding} - {node.name} (dir)"))
        for child in node.children:
            tree_to_lines(child, level+1, acc)


def print_tree(root):
    "Print tree."
    acc = []
    tree_to_lines(root, 0, acc)
    print("\n".join(acc))


def read_input(filename):
    "Read input into a list of lines."
    with open(filename) as infile:
        lines = infile.readlines()
    return lines


def solve_a(root):
    "Return sum of sizes of directories with size of at most 100000"

    def traverse(node):
        "Internal helper fn to recursively sum 'small' directories."
        if node.type == Node.FILE:
            return 0

        return (
            (node.get_size() if node.get_size() <= 100000 else 0) +
            sum(traverse(child) for child in node.children)
        )

    return traverse(root)


def solve_b(root):
    "Find the smallest directory that can be deleted."
    max_capacity = 70000000
    target_space = 30000000

    def collect_directories(node, acc):
        "Internal helper fn to recursively gather directory nodes."
        if node.type == Node.DIR:
            acc.append(node)
            for child in node.children:
                collect_directories(child, acc)

    directories = []
    total_used = root.get_size()
    soln_b = root
    collect_directories(root, directories)
    for dir in directories:
        used_if_deleted = total_used - dir.get_size()
        if max_capacity - used_if_deleted >= target_space:
            if dir.get_size() < soln_b.get_size():
                soln_b = dir
    return soln_b.get_size()


#
# Testing
#


def test_1():
    "Test parsing"
    root = parse_tree(read_input('../test.txt'))
    e = find_node(root, 'e')
    assert e.get_size() == 584
    a = find_node(root, 'a')
    assert a.get_size() == 94853
    d = find_node(root, 'd')
    assert d.get_size() == 24933642
    assert root.get_size() == 48381165


def test_2():
    "Test solve_a()"
    root = parse_tree(read_input('../test.txt'))
    assert solve_a(root) == 95437


def test_3():
    "Test solve_b()"
    root = parse_tree(read_input('../test.txt'))
    assert solve_b(root) == 24933642


#
# Main
#


def main():
    "Main program"
    import pyperclip
    lines = read_input('../input07.txt')
    root = parse_tree(lines)
    soln_a = solve_a(root)
    assert soln_a == 1783610
    print(f"The solution to part A is {soln_a}")
    soln_b = solve_b(root)
    assert soln_b == 4370655
    print(f"The solution to part B is {soln_b}")
    pyperclip.copy(soln_b)
    print(f"{soln_b} has been placed in the clipboard.")


if __name__ == '__main__':
    main()