"""
Advent of Code 2022
Day 9: Rope Bridge
jramaswami
"""


import collections


Posn = collections.namedtuple('Posn', ['row', 'col'])


DIRNS = {
    'L': Posn(0, -1), 'R': Posn(0, 1),
    'U': Posn(-1, 0), 'D': Posn(1, 0)
}


def sign(x):
    "Return the sign of x."
    if x < 0:
        return -1
    if x > 0:
        return 1
    return 0


def move_head(head, dirn):
    "Return new position of head moved in given direction (L,R,U,D)."
    delta = DIRNS[dirn]
    return Posn(head.row + delta.row, head.col + delta.col)


def too_far(head, tail):
    "Return True if head and tail are not touching."
    return (
        abs(head.row - tail.row) > 1 or
        abs(head.col - tail.col) > 1
    )


def move_tail(head, tail):
    "Return the position of tail so that it remains touching the head."
    dr = sign(head.row - tail.row)
    dc = sign(head.col - tail.col)
    tail0 = tail
    if too_far(head, tail):
        tail0 = Posn(tail.row + dr, tail.col + dc)

    assert (
        abs(head.row - tail0.row) <= 2 and
        abs(head.col - tail0.col) <= 2
    )

    return tail0


def read_input(input_file):
    "Read input file."
    instructions = []
    with open(input_file) as infile:
        for line in infile:
            tokens = line.strip().split()
            instructions.append((tokens[0], int(tokens[1])))
    return instructions


def solve_a(instructions):
    "Solve part A of puzzle."
    visited = set()
    tail = Posn(0,0)
    head = Posn(0,0)
    visited.add(tail)
    for dirn, repeat in instructions:
        for _ in range(repeat):
            head0 = move_head(head, dirn)
            tail0 = move_tail(head0, tail)
            head, tail = head0, tail0
            visited.add(tail)
    return len(visited)


def move_multi_snake(snake, dirn):
    "Move snake with many parts."
    snake0 = list(snake)
    snake0[0] = move_head(snake0[0], dirn)
    for i in range(1, 10):
        if too_far(snake0[i-1], snake0[i]):
            snake0[i] = move_tail(snake0[i-1], snake0[i])
    return snake0


def solve_b(instructions):
    "Solve part B of puzzle."
    visited = set()
    snake = [Posn(0,0) for _ in range(10)]
    visited.add(snake[-1])
    for dirn, repeat in instructions:
        for _ in range(repeat):
            snake = move_multi_snake(snake, dirn)
            visited.add(snake[-1])
    return len(visited)


#
# Testing
#


def test_move_tail():
    head, tail = Posn(1, 2), Posn(1,1)
    head = move_head(head, 'R')
    tail = move_tail(head, tail)
    expected = Posn(1, 2)
    assert tail == expected

    head, tail = Posn(2, 1), Posn(1, 1)
    head = move_head(head, 'D')
    tail = move_tail(head, tail)
    expected = Posn(2, 1)
    assert tail == expected

    head, tail = Posn(2, 2), Posn(3, 1)
    head = move_head(head, 'U')


def test_solve_a():
    instructions = read_input('../test1.txt')
    soln_a = solve_a(instructions)
    assert soln_a == 13


def test_solve_b():
    instructions = read_input('../test2.txt')
    soln_b = solve_b(instructions)
    assert soln_b == 36


#
# Main
#


def main():
    "Main program."
    import pyperclip
    instructions = read_input('../input09.txt')
    soln_a = solve_a(instructions)
    assert soln_a == 6098
    print(f"The solution to part A is {soln_a}.")
    soln_b = solve_b(instructions)
    assert soln_b == 2597
    print(f"The solution to part B is {soln_b}.")
    pyperclip.copy(str(soln_b))
    print(f"{soln_b} has been placed on the clipboard.")


if __name__ == '__main__':
    main()