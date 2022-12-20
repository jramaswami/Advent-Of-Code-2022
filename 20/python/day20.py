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
    N = len(nums)
    i = find_zth(nums, z)
    x = nums[i]

    if x.value == 0:
        return

    nums.pop(i)
    j = i + x.value
    j = j % len(nums)
    before = nums[(j-1)%len(nums)].value
    after = nums[j].value
    if j == 0:
        j = len(nums)
    nums.insert(j, x)


def mix_one_round(nums):
    "Mix one round of nums."
    for i in range(len(nums)):
        mix(nums, i)


def solve_a(nums):
    "Solve part A of puzzle."
    # Do not mutate original list.
    nums0 = list(nums)

    # Mix it up!
    mix_one_round(nums0)

    # Find zero and then sum the wanted numbers.
    z = find_zero(nums0)
    IS = [1000+z, 2000+z, 3000+z]
    return sum(nums0[i%len(nums0)].value for i in IS)


def apply_decryption_key(nums):
    "Apply decryption key by multiplying all values by key value."
    decryption_key = 811589153
    return [Item(x.index, x.value * decryption_key) for x in nums]


def solve_b(nums):
    "Solve part B of puzzle."
    nums0 = apply_decryption_key(nums)
    for _ in range(10):
        mix_one_round(nums0)
    # Find zero and then sum the wanted numbers.
    z = find_zero(nums0)
    IS = [1000+z, 2000+z, 3000+z]
    return sum(nums0[i%len(nums0)].value for i in IS)


#
# Testing
#


def test_mix_1():
    "Test mix without decryption key."
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
        assert [n.value for n in nums] == ex



def test_apply_decryption_key():
    expected_values = [
        811589153, 1623178306, -2434767459, 2434767459,
        -1623178306, 0, 3246356612
    ]
    nums = read_input('../test.txt')
    decrypted_nums = apply_decryption_key(nums)
    assert [x.value for x in decrypted_nums] == expected_values


def test_mix_2():
    "Test mix with decryption key."
    expected = [
        [0, -2434767459, 3246356612, -1623178306, 2434767459, 1623178306, 811589153],
        [0, 2434767459, 1623178306, 3246356612, -2434767459, -1623178306, 811589153],
        [0, 811589153, 2434767459, 3246356612, 1623178306, -1623178306, -2434767459],
        [0, 1623178306, -2434767459, 811589153, 2434767459, 3246356612, -1623178306],
        [0, 811589153, -1623178306, 1623178306, -2434767459, 3246356612, 2434767459],
        [0, 811589153, -1623178306, 3246356612, -2434767459, 1623178306, 2434767459],
        [0, -2434767459, 2434767459, 1623178306, -1623178306, 811589153, 3246356612],
        [0, 1623178306, 3246356612, 811589153, -2434767459, 2434767459, -1623178306],
        [0, 811589153, 1623178306, -2434767459, 3246356612, 2434767459, -1623178306],
        [0, -2434767459, 1623178306, 3246356612, -1623178306, 2434767459, 811589153],
    ]
    nums = apply_decryption_key(read_input('../test.txt'))
    for i, ex in enumerate(expected):
        mix_one_round(nums)
        result = [n.value for n in nums]
        assert result == ex


def test_solve_a():
    nums = read_input('../test.txt')
    expected = 3
    assert solve_a(nums) == expected


def test_solve_b():
    nums = read_input('../test.txt')
    expected = 1623178306
    assert solve_b(nums) == expected


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
    soln_b = solve_b(nums)
    print(f"The solution to part B is {soln_b}.")
    pyperclip.copy(str(soln_b))
    print(f"{soln_b} has been placed on the clipboard.")


if __name__ == '__main__':
    main()
