""" Advent of Code 2022
Day 2: Rock Paper Scissors
jramaswamio
"""


ROCK = 1
PAPER = 2
SCISSORS = 3

WIN = 6
DRAW = 3
LOSS = 0

CODES = {
    'A': ROCK, 'B': PAPER, 'C': SCISSORS,
    'X': ROCK, 'Y': PAPER, 'Z': SCISSORS
}

# Key = (Opponent, Me)
OUTCOMES = {
    (ROCK, ROCK): DRAW, (ROCK, PAPER): WIN, (ROCK, SCISSORS): LOSS,
    (PAPER, PAPER): DRAW, (PAPER, SCISSORS): WIN, (PAPER, ROCK): LOSS,
    (SCISSORS, SCISSORS): DRAW, (SCISSORS, ROCK): WIN, (SCISSORS, PAPER): LOSS
}


GUIDED_CODES = {
    'A': ROCK, 'B': PAPER, 'C': SCISSORS,
    'X': LOSS, 'Y': DRAW, 'Z': WIN
}


GUIDED_OUTCOME = {
                # Rock, Paper, Scissors
    LOSS: [None, SCISSORS, ROCK, PAPER],
    DRAW: [None, ROCK, PAPER, SCISSORS],
    WIN: [None, PAPER, SCISSORS, ROCK],
}


def run_round(line):
    "Return the result of the round."
    if not line.strip():
        return 0
    foe, me = line.strip().split()
    return OUTCOMES[(CODES[foe], CODES[me])] + CODES[me]


def run_tournament(lines):
    "Run the tournament."
    return sum(run_round(line) for line in lines)


def guide_round(line):
    "Return the result of a round run according to strategy."
    if not line.strip():
        return 0
    foe, outcome = line.strip().split()
    foe, outcome = GUIDED_CODES[foe], GUIDED_CODES[outcome]
    me = GUIDED_OUTCOME[outcome][foe]
    return outcome + me


def guide_tournament(lines):
    "Run the tournament according to strategy."
    return sum(guide_round(line) for line in lines)


def test_1():
    "Test each round of part a tournament."
    expected = [8, 1, 6]
    with open('../test.txt') as infile:
        for i, line in enumerate(infile):
            assert run_round(line) == expected[i]


def test_2():
    "Test part a tournament."
    with open('../test.txt') as infile:
        assert run_tournament(infile) == 15


def test_3():
    "Test each round of part b tournament."
    expected = [4, 1, 7]
    with open('../test.txt') as infile:
        for i, line in enumerate(infile):
            assert guide_round(line) == expected[i]


def test_4():
    "Test part b tournament."
    with open('../test.txt') as infile:
        assert guide_tournament(infile) == 12


def main():
    "Main program."
    import pyperclip
    with open('../input02.txt') as infile:
        lines = infile.readlines()
        soln_a = run_tournament(lines)
        assert soln_a == 8890
        print(f"Your total score (if everything goes as planned) is {soln_a}.")
        soln_b = guide_tournament(lines)
        assert soln_b == 10238
        print(f"Your total score (if you play the strategy) is {soln_b}.")
        pyperclip.copy(str(soln_b))
        print(f"{soln_b} has been placed in the clipboard.")


if __name__ == '__main__':
    main()