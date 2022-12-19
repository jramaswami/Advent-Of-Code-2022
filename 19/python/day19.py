"""
Advent of Code 2022
Day 19: Not Enough Minerals
jramaswami

Needed some help figuring out how to prune solution space.
"""


import collections
import tqdm


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
GEODE_ROBOT_ORE_COST = 4
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


def max_geodes(blueprint, timelimit):
    # state = (
    #   ore robots, clay robots, obsidian robots, geode robots,
    #   ore units, clay units, obsidian units, geode units
    # )

    queue = collections.deque()
    init_state = tuple([1, 0, 0, 0, 0, 0, 0, 0])

    max_ore_needed = max(
        blueprint[ORE_ROBOT_ORE_COST], blueprint[CLAY_ROBOT_ORE_COST],
        blueprint[OBSIDIAN_ROBOT_ORE_COST], blueprint[GEODE_ROBOT_ORE_COST]
    )
    max_clay_needed = blueprint[OBSIDIAN_ROBOT_CLAY_COST]
    max_obsidian_needed = blueprint[GEODE_ROBOT_OBSIDIAN_COST]

    queue.append(init_state)
    new_queue = []
    curr_max_geode_robots = 0
    visited = set()
    visited.add(init_state)
    for tick in range(timelimit):
        # print(tick+1, len(queue), curr_max_geodes)
        for state in queue:
            curr_max_geode_robots = max(curr_max_geode_robots, state[GEODE_ROBOTS])
            if state[GEODE_ROBOTS] + 1 < curr_max_geode_robots:
                continue

            # Buy geode robot?
            if (state[ORE_UNITS] >= blueprint[GEODE_ROBOT_ORE_COST]
            and state[OBSIDIAN_UNITS] >= blueprint[GEODE_ROBOT_OBSIDIAN_COST]):
                state0 = list(state)
                # Buy robot.
                state0[ORE_UNITS] -= blueprint[GEODE_ROBOT_ORE_COST]
                state0[OBSIDIAN_UNITS] -= blueprint[GEODE_ROBOT_OBSIDIAN_COST]
                # Mine resources.
                for i, robot in enumerate(state0[:4]):
                    state0[i+4] += state0[i]
                # Deliver robot.
                state0[GEODE_ROBOTS] += 1
                state0 = tuple(state0)
                if state0 not in visited:
                    visited.add(state0)
                    new_queue.append(state0)
                # Don't bother checking anyting else if you can buy the geode
                # robot
                continue

            # Don't buy anything
            state0 = list(state)
            for i, robot in enumerate(state0[:ORE_UNITS]):
                state0[i+4] += state0[i]
            state0 = tuple(state0)
            if state0 not in visited:
                visited.add(state0)
                new_queue.append(state0)

            # Buy ore robot?
            if (state[ORE_ROBOTS] < max_ore_needed
            and state[ORE_UNITS] >= blueprint[ORE_ROBOT_ORE_COST]):
                state0 = list(state)
                # Buy robot.
                state0[ORE_UNITS] -= blueprint[ORE_ROBOT_ORE_COST]
                # Mine resources.
                for i, robot in enumerate(state0[:4]):
                    state0[i+4] += state0[i]
                # Deliver robot.
                state0[ORE_ROBOTS] += 1
                state0 = tuple(state0)
                if state0 not in visited:
                    visited.add(state0)
                    new_queue.append(state0)

            # Buy clay robot?
            if (state[CLAY_ROBOTS] < max_clay_needed
            and state[ORE_UNITS] >= blueprint[CLAY_ROBOT_ORE_COST]):
                state0 = list(state)
                # Buy robot.
                state0[ORE_UNITS] -= blueprint[CLAY_ROBOT_ORE_COST]
                # Mine resources.
                for i, robot in enumerate(state0[:4]):
                    state0[i+4] += state0[i]
                # Deliver robot.
                state0[CLAY_ROBOTS] += 1
                state0 = tuple(state0)
                if state0 not in visited:
                    visited.add(state0)
                    new_queue.append(state0)

            # Buy obsidian robot?
            if (state[OBSIDIAN_ROBOTS] < max_obsidian_needed
            and state[ORE_UNITS] >= blueprint[OBSIDIAN_ROBOT_ORE_COST]
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
                if state0 not in visited:
                    visited.add(state0)
                    new_queue.append(state0)

        # print('Swapping ...')
        queue, new_queue = new_queue, []

    return max(s[GEODE_UNITS] for s in queue)


def solve_a(blueprints, timelimit=24):
    soln_a = 0
    for i in tqdm.tqdm(range(len(blueprints))):
        soln_a += ((i+1) * max_geodes(blueprints[i], timelimit))
    return soln_a


def solve_b(blueprints, timelimit=32):
    soln_b = 1
    limit = 3
    if len(blueprints) < 3:
        limit = len(blueprints)
    for i in tqdm.tqdm(range(limit)):
        soln_b *= max_geodes(blueprints[i], timelimit)
    return soln_b


def test_solve_a():
    recipes = read_input('../test.txt')
    expected = 33
    soln_a = solve_a(recipes)
    assert soln_a == expected


def test_solve_b():
    recipes = read_input('../test.txt')
    assert solve_b(recipes) == (56 * 62)



#
# Main
#


def main():
    "Main program."
    import pyperclip
    recipes = read_input('../input19.txt')
    soln_a = solve_a(recipes)
    print(f"The solution to part A is {soln_a}.")
    assert soln_a == 1487
    soln_b = solve_b(recipes)
    print(f"The solution to part B is {soln_b}.")
    assert soln_b == 13440
    pyperclip.copy(str(soln_b))
    print(f"{soln_b} has been placed on the clipboard.")


if __name__ == '__main__':
    main()
