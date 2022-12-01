"""
Advent of Code 2022 :: Day 1: Calorie Counting
jramaswami
"""


def main():
    "Main program."
    import sys
    import pyperclip
    elves = []
    curr_calories = 0
    for line in sys.stdin:
        line = line.strip()
        if line:
            curr_calories += int(line)
        else:
            elves.append(curr_calories)
            curr_calories = 0
    elves.append(curr_calories)   # Last elf.

    soln_a = max(elves)
    assert soln_a == 70613
    print(f"The maximum calories carried by an elf is {soln_a}")

    elves.sort()
    soln_b = sum(elves[-3:])
    assert soln_b == 205805
    pyperclip.copy(str(soln_b))
    print(f"The top three elves are carrying {soln_b} calories.")
    print(f"{soln_b} has been placed in clipboard.")


if __name__ == '__main__':
    main()