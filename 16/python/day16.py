"""
Advent of Code 2022
Day 16: Proboscidea Volcanium
jramaswami
"""


import collections
import itertools
import math
import os
import tqdm


State = collections.namedtuple(
    'State',
    ['valve', 'flow', 'acc', 'time', 'key']
)

def parse_input(filename):
    valve_flows = dict()
    valve_graph = collections.defaultdict(list)
    valve_clause_prefix = 'Valve '
    valve_offset = len(valve_clause_prefix)
    with open(filename) as infile:
        for line in infile:
            valve_clause, tunnel_clause = line.strip().split('; ')
            valve = valve_clause[valve_offset:valve_offset+2]
            i = valve_clause.index('=')
            flow = int(valve_clause[i+1:])
            if flow:
                valve_flows[valve] = flow

            i = tunnel_clause.find('valves')
            if i < 0:
                i = tunnel_clause.find('valve')
            j = tunnel_clause.find(' ', i)
            tunnels = tunnel_clause[j+1:].split(', ')
            valve_graph[valve] = tunnels
    return valve_flows, valve_graph


def floyd_warshall(valve_graph):
    dist = collections.defaultdict(lambda: collections.defaultdict(lambda: math.inf))
    for u, neighbors in valve_graph.items():
        dist[u][u] = 0
        for v in neighbors:
            dist[u][v] = 1
    for k in valve_graph:
        for i in valve_graph:
            for j in valve_graph:
                if dist[i][j] > dist[i][k] + dist[k][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    return dist


def solve_a(valve_flows, valve_graph, time_limit=30):
    "Solve part A of puzzle."

    dist = floyd_warshall(valve_graph)

    soln_a = 0
    init_state = State('AA', 0, 0, 0, 0)
    queue = collections.deque()
    queue.append(init_state)

    while queue:
        state = queue.popleft()
        total_flow = state.acc + ((time_limit - state.time) * state.flow)
        if total_flow > soln_a:
            soln_a = total_flow

        for i, neighbor in enumerate(valve_flows):
            key0 = state.key | (1 << i)
            if key0 == state.key:
                continue

            time_to_open = dist[state.valve][neighbor] + 1
            if state.time + time_to_open <= time_limit:
                state0 = State(
                    neighbor,
                    state.flow + valve_flows[neighbor],
                    state.acc + (time_to_open * state.flow),
                    state.time + time_to_open,
                    key0
                )
                queue.append(state0)

    return soln_a


# From Python docs.
def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return itertools.chain.from_iterable(itertools.combinations(s, r) for r in range(len(s)+1))


def solve_b(valve_flows, valve_graph, use_cache=True):
    "Solve part B of puzzle."
    # Takes less than a second to do the entire set.
    # I do some, elephant does the rest.
    # Only 2^N items in a powerset.
    # Compute best flow for each set of valves.
    # Maximize (my best with set nodes) + (elephants best with rest of nodes)

    def compute_key(vs):
        key = 0
        for i, u in enumerate(valve_flows):
            mask = (1 << i)
            if u in vs:
                key |= mask
        return key

    if use_cache and os.path.exists('cache_file.txt'):
        print('Reading cached flows for each set of valves ...')
        with open('cache_file.txt') as infile:
            scores = [int(line.strip()) for line in infile]
    else:
        P = [tuple(sorted(p)) for p in powerset(valve_flows)]
        scores = [0 for _ in P]

        print(f"There are {len(P)} kinds to check.")
        print("It takes approximately 15 minutes to check them.")
        for me in tqdm.tqdm(P):
            my_valves = {v: f for v, f in valve_flows.items() if v in me}
            my_key = compute_key(my_valves)
            my_flow = solve_a(my_valves, valve_graph, 26)
            scores[my_key] = my_flow

        if use_cache:
            print('Caching flow results ...')
            with open('cache_file.txt', 'w') as outfile:
                for score in scores:
                    print(score, file=outfile)

    soln_b = 0
    for key, _ in enumerate(scores):
        soln_b = max(soln_b, (scores[key] + scores[~key]))
    return soln_b


#
# Testing
#


def test_solve_a():
    valve_flows, valve_graph = parse_input('../test.txt')
    expected = 1651
    result = solve_a(valve_flows, valve_graph)
    assert result == expected


def test_solve_b():
    valve_flows, valve_graph = parse_input('../test.txt')
    expected = 1707
    result = solve_b(valve_flows, valve_graph, use_cache=False)
    assert result == expected


#
# Main
#


def main():
    "Main program."
    import pyperclip
    # valve_flows, valve_graph = parse_input('../test.txt')
    valve_flows, valve_graph = parse_input('../input16.txt')
    soln_a = solve_a(valve_flows, valve_graph)
    assert soln_a == 1940
    print(f"The solution to part A is {soln_a}.")
    soln_b = solve_b(valve_flows, valve_graph)
    print(f"The solution to part B is {soln_b}.")
    assert soln_b == 2469
    pyperclip.copy(str(soln_b))
    print(f"{soln_b} has been placed on the clipboard.")


if __name__ == '__main__':
    main()
