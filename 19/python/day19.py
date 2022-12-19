"""
Advent of Code 2022
Day 19: Not Enough Minerals
jramaswami
"""


import collections
import functools
import heapq


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
    init_robots = Robots(1, 0, 0 ,0)
    init_resources = Resources(0, 0, 0, 0)
    queue = set([(init_robots, init_resources)])
    new_queue = set()
    curr_max_geodes = 0
    for t in range(24):
        print(t, len(queue), curr_max_geodes)
        for robots, resources in queue:
            print(robots, resources)
            # print(robots, resources)
            # Do not buy.
            resources1 = mine_resources(robots, resources)
            new_queue.add((robots, resources1))

            # Buy a robot.
            for robot in ROBOT_NAMES:
                resources0 = resources
                if can_buy(robot, resources0, blueprint):
                    robots0, resources0 = buy_robot(
                        robot, robots, resources0, blueprint
                    )
                    resources1 = mine_resources(robots, resources0)
                    new_queue.add((robots0, resources1))
        curr_max_geodes = max(r.geode for _, r in new_queue)
        queue, new_queue = new_queue, set()

    return max(resources.geode for _, resources in queue)




def solve_a(blueprints):
    result = simulate(blueprints[0])

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
