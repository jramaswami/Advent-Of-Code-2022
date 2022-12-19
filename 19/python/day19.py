"""
Advent of Code 2022
Day 19: Not Enough Minerals
jramaswami
"""


import functools


ORE_ROBOTS = 0
CLAY_ROBOTS = 1
OBSIDIAN_ROBOTS = 2
GEODE_ROBOTS = 3
ORE_UNITS = 4
CLAY_UNITS = 5
OBSIDIAN_UNITS = 6
GEODE_UNITS = 7

ORE_ROBOT_ORE_COST = 0
CLAY_ROBOT_ORE_COST = 1
OBSIDIAN_ROBOT_ORE_COST = 2
OBSIDIAN_ROBOT_CLAY_COST = 3
GEODE_ROBOT_CLAY_COST = 4
GEODE_ROBOT_OBSIDIAN_COST = 5



def read_input(filename):
    blueprints = []
    with open(filename) as infile:
        for line in infile:
            line = line.strip()
            i = line.find(': ')
            blueprints.append(
                tuple([int(t) for t in line[i+1:].split() if t.isnumeric()])
            )
    return blueprints


def max_geodes(blueprint):
    # state = (
    #   ore robots, clay robots, obsidian robots, geode robots,
    #   ore units, clay units, obsidian units, geode units
    # )

    @functools.cache
    def rec(timer, state):
        # Base case.
        if timer >= 24:
            return state[GEODE_UNITS]

        # Don't buy anything
        state0 = list(state)
        for i, robot in enumerate(state0[:ORE_UNITS]):
            state0[i+4] += state0[i]
        state0 = tuple(state0)
        result = rec(timer+1, state0)

        # Buy ore robot?
        if state[ORE_UNITS] >= blueprint[ORE_ROBOT_ORE_COST]:
            state0 = list(state)
            # Buy robot.
            state0[ORE_UNITS] -= blueprint[ORE_ROBOT_ORE_COST]
            # Mine resources.
            for i, robot in enumerate(state0[:4]):
                state0[i+4] += state0[i]
            # Deliver robot.
            state0[ORE_ROBOTS] += 1
            state0 = tuple(state0)
            result = max(result, rec(timer+1, state0))

        # Buy clay robot?
        if state[ORE_UNITS] >= blueprint[CLAY_ROBOT_ORE_COST]:
            state0 = list(state)
            # Buy robot.
            state0[ORE_UNITS] -= blueprint[CLAY_ROBOT_ORE_COST]
            # Mine resources.
            for i, robot in enumerate(state0[:4]):
                state0[i+4] += state0[i]
            # Deliver robot.
            state0[CLAY_ROBOTS] += 1
            state0 = tuple(state0)
            result = max(result, rec(timer+1, state0))

        # Buy obsidian robot?
        if (state[ORE_UNITS] >= blueprint[OBSIDIAN_ROBOT_ORE_COST]
        and state[CLAY_UNITS] >= blueprint[OBSIDIAN_ROBOT_CLAY_COST]):
            state0 = list(state)
            # Buy robot.
            state0[ORE_UNITS] -= blueprint[OBSIDIAN_ROBOT_ORE_COST]
            state0[CLAY_UNITS] -= blueprint[OBSIDIAN_ROBOT_CLAY_COST]
            # Mine resources.
            for i, robot in enumerate(state0[:4]):
                state0[i+4] += state0[i]
            # Deliver robot.
            state0[OBSIDIAN_ROBOTS] += 1
            state0 = tuple(state0)
            result = max(result, rec(timer+1, state0))

        # Buy geode robot?
        if (state[CLAY_UNITS] >= blueprint[GEODE_ROBOT_CLAY_COST]
        and state[OBSIDIAN_UNITS] >= blueprint[GEODE_ROBOT_OBSIDIAN_COST]):
            state0 = list(state)
            # Buy robot.
            state0[CLAY_UNITS] -= blueprint[GEODE_ROBOT_CLAY_COST]
            state0[OBSIDIAN_UNITS] -= blueprint[GEODE_ROBOT_OBSIDIAN_COST]
            # Mine resources.
            for i, robot in enumerate(state0[:4]):
                state0[i+4] += state0[i]
            # Deliver robot.
            state0[GEODE_ROBOTS] += 1
            state0 = tuple(state0)
            result = max(result, rec(timer+1, state0))
        return result

    init_state = tuple([1, 0, 0, 0, 0, 0, 0, 0])
    return rec(0, init_state)

def solve_a(blueprints):
    print(max_geodes(blueprints[0]))


#
# Main
#


def main():
    "Main program."
    import pyperclip
    recipes = read_input('../test.txt')
    soln_a = solve_a(recipes)


if __name__ == '__main__':
    main()
