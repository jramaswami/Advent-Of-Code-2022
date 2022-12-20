"""
Advent of Code 2022
Day 20: Grove Positioning System
jramaswami
"""


import collections


Item = collections.namedtuple('Item', ['index', 'value'])


def read_input(filename):
    "Read input file."
    with open(filename) as infile:
        return [Item(i, int(line)) for i, line in enumerate(infile)]


def find_zero(nums):
    "Find the index of the item with a value of zero."
    for i, item in enumerate(nums):
        if item.value == 0:
            return i
    raise ValueError(f"Unable to find {z}-ith item.")


def find_zth(nums, z):
    "Find the item with the z-th original index."
    for i, item in enumerate(nums):
        if item.index == z:
            return i
    raise ValueError(f"Unable to find {z}-ith item.")


def mix(nums, z):
    "Mix z-th item nums, where i is the *original* index of the item."
    i = find_zth(nums, z)
    x = nums[i]
    nums.pop(i)
    j = i + x.value
    j = j % len(nums)
    if j == 0:
        j = len(nums)
    nums.insert(j, x)


def solve_a(nums):
    "Solve part A of puzzle."
    # Do not mutate original list.
    nums0 = list(nums)

    # Mix it up!
    for i in range(len(nums)):
        mix(nums0, i)

    # Find zero and then sum the wanted numbers.
    z = find_zero(nums0)
    IS = [1000+z, 2000+z, 3000+z]
    return sum(nums0[i%len(nums0)].value for i in IS)


#
# Testing
#


def test_mix():
    expected = [
        [2, 1, -3, 3, -2, 0, 4],
        [1, -3, 2, 3, -2, 0, 4],
        [1, 2, 3, -2, -3, 0, 4],
        [1, 2, -2, -3, 0, 3, 4],
        [1, 2, -3, 0, 3, 4, -2],
        [1, 2, -3, 0, 3, 4, -2],
        [1, 2, -3, 4, 0, 3, -2],
    ]
    nums = read_input('../test.txt')
    for i, ex in enumerate(expected):
        mix(nums, i)
        print(f"after test {i+1} nums is now {[n.value for n in nums]}")
        assert [n.value for n in nums] == ex


def test_solve_a():
    nums = read_input('../test.txt')
    expected = 3
    assert solve_a(nums) == expected


#
# Main
#


def main():
    "Main program."
    import pyperclip
    nums = read_input('../input20.txt')
    soln_a = solve_a(nums)
    print(f"The solution to part A is {soln_a}.")
    assert soln_a == 4151
    pyperclip.copy(str(soln_a))
    print(f"{soln_a} has been placed on the clipboard.")


if __name__ == '__main__':
    main()
