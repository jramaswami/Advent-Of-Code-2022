"""
Advent of Code 2022
Day 6: Tuning Troubl
jramaswami
"""


import collections


def all_different(window):
    "Return True if all chars in window are different."
    return len(set(window)) == len(window)


def solve(buffer, window_size):
    "Solve puzzle for given window size."
    window = collections.deque()
    for i, c in enumerate(buffer):
        window.append(c)
        while len(window) > window_size:
            window.popleft()
        if len(window) == window_size and all_different(window):
            return i + 1
    assert False


#
# Testing
#


def test_1():
    test_buffers = [
        "mjqjpqmgbljsphdztnvjfqwrcgsmlb",
        "bvwbjplbgvbhsrlpgdmjqwftvncz",
        "nppdvjthqldpwncqszvftbrmjlhg",
        "nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg",
        "zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw"
    ]
    expected = [7, 5, 6, 10, 11]
    for i, buffer in enumerate(test_buffers):
        assert solve(buffer, 4) == expected[i]


def test_2():
    test_buffers = [
        "mjqjpqmgbljsphdztnvjfqwrcgsmlb",
        "bvwbjplbgvbhsrlpgdmjqwftvncz",
        "nppdvjthqldpwncqszvftbrmjlhg",
        "nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg",
        "zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw"
    ]
    expected = [19, 23, 23, 29, 26]
    for i, buffer in enumerate(test_buffers):
        print('ex', buffer[5:19])
        assert solve(buffer, 14) == expected[i]


def main():
    "Main program."
    import pyperclip
    with open('../input06.txt') as infile:
        buffer = infile.readline().strip()
    soln_a = solve(buffer, 4)
    assert soln_a == 1134
    print(f"The solution to part A is {soln_a}.")
    soln_b = solve(buffer, 14)
    assert soln_b == 2263
    print(f"The solution to part B is {soln_b}.")
    pyperclip.copy(str(soln_b))
    print(f"{soln_b} has been placed in the clipboard.")


if __name__ == '__main__':
    main()