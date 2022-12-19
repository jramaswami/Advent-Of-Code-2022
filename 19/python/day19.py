"""
Advent of Code 2022
Day 19: Not Enough Minerals
jramaswami
"""


import collections
import functools


ROBOT_NAMES = ['ore', 'clay', 'obsidian', 'geode']


Resources = collections.namedtuple(
    'Resources',
    ['ore', 'clay', 'obsidian', 'geode']
)


Recipes = collections.namedtuple(
    'Recipes',
    ['ore', 'clay', 'obsidian', 'geode']
)


Robots = collections.namedtuple(
    'Robots',
    ['ore', 'clay', 'obsidian', 'geode']
)


def read_input(filename):
    "Read and parse input."
    blueprints = []
    with open(filename) as infile:
        for line in infile:
            tokens = [int(t) for t in line.split() if t.isnumeric()]
            assert len(tokens) == 6
            ore_robot = Resources(tokens[0], 0, 0, 0)
            clay_robot = Resources(tokens[1], 0, 0, 0)
            obsidian_robot = Resources(tokens[2], tokens[3], 0, 0)
            geode_robot = Resources(tokens[4], tokens[5], 0, 0)
            blueprints.append(
                Recipes(ore_robot, clay_robot, obsidian_robot, geode_robot)
            )
    return blueprints


def can_buy(robot, resources, blueprint):
    recipe = getattr(blueprint, robot)
    for i, _ in enumerate(recipe):
        if resources[i] < recipe[i]:
            return False
    return True


def buy_robot(robot, robots, resources, blueprint):
    recipe = getattr(blueprint, robot)
    resources0 = []
    robots0 = []
    for i, _ in enumerate(recipe):
        resources0.append(resources[i] - recipe[i])
        robots0.append(robots[i])
        if ROBOT_NAMES[i] == robot:
            robots0[i] += 1
    return Robots(*robots0), Resources(*resources0)


def mine_resources(robots, resources):
    resources0 = []
    for robot in ROBOT_NAMES:
        resources0.append(
            getattr(resources, robot) + getattr(robots, robot)
        )
    return Resources(*resources0)


def simulate(blueprint):

    @functools.cache
    def rec(i, robots, resources):
        # Base Case.
        if i >= 24:
            return resources

        # Collect resources
        resources = mine_resources(robots, resources)

        result = resources
        for robot in ROBOT_NAMES:
            dont_buy = rec(i+1, robots, resources)
            if dont_buy.geode > result.geode:
                result = dont_buy
            if can_buy(robot, resources, blueprint):
                robots0, resources0 = buy_robot(robot, robots, resources, blueprint)
                buy = rec(i+1, robots0, resources0)
                if buy.geode > result.geode:
                    result = buy
        return result

    init_robots = Robots(1, 0, 0 ,0)
    init_resources = Resources(0, 0, 0, 0)
    return rec(0, init_robots, init_resources)


def solve_a(blueprints):
    for blueprint in blueprints:
        print('Simulating', blueprint, '...')
        result = simulate(blueprint)
        print(blueprint, result)

#
# Main
#


def main():
    "Main program."
    import pyperclip
    blueprints = read_input('../test.txt')
    soln_a = solve_a(blueprints)
    print("The solution to part A is {soln_a}.")


if __name__ == '__main__':
    main()
