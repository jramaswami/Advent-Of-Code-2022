"""
Advent of Code 2022
Day 16: Proboscidea Volcanium
jramaswami
"""


import collections
import itertools
import math
import tqdm


State = collections.namedtuple(
    'State',
    ['valve', 'flow', 'acc', 'time', 'closedvalves', 'id']
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


def add_to_path(path, valve, flow, start):
    "Add a given flow event to the path."
    path0 = list(path)
    path0.append((valve, flow, start))
    return tuple(path0)


def trackback(parents, start):
    "Track back to reconstruct path."
    stack = [start]
    while stack[-1] >= 0:
        stack.append(parents[stack[-1]])
    return stack[::-1]


def solve_a(valve_flows, valve_graph):
    "Solve part A of puzzle."
    dist = floyd_warshall(valve_graph)
    soln_a = 0
    init_state = State('AA', 0, 0, 0, frozenset(valve_flows), -1)
    queue = collections.deque()
    queue.append(init_state)

    parents = dict()
    all_states = dict()
    all_states[-1] = init_state

    while queue:
        state = queue.popleft()
        total_flow = state.acc + ((30 - state.time) * state.flow)
        if total_flow > soln_a:
            soln_a = total_flow
            soln_end = state.id

        for neighbor in state.closedvalves:
            time_to_open = dist[state.valve][neighbor] + 1
            if state.time + time_to_open <= 30:
                state0 = State(
                    neighbor,
                    state.flow + valve_flows[neighbor],
                    state.acc + (time_to_open * state.flow),
                    state.time + time_to_open,
                    state.closedvalves - frozenset([neighbor]),
                    len(parents)
                )
                parents[state0.id] = state.id
                all_states[state0.id] = state0
                queue.append(state0)

    path = []
    for i in trackback(parents, soln_end):
        s = all_states[i]
        path.append((s.time, s.valve))

    return soln_a, path


# From Python docs.
def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return itertools.chain.from_iterable(itertools.combinations(s, r) for r in range(len(s)+1))


def solve_b(valve_flows, valve_graph):
    "Solve part B of puzzle."
    # Takes less than a second to do the entire set.
    # I do some, elephant does the rest.
    # Only 2^N items in a powerset.
    # Compute best flow *and* path/time for each set of valves.
    # Maximize (my best with set nodes) + (elephants best with rest of nodes)

    soln_b = solve_a(valve_flows, valve_graph)[0]
    P = list(powerset(valve_flows))
    for me in tqdm.tqdm(P):
        if not me:
            continue
        me0 = frozenset(me)
        my_valves = {v: f for v, f in valve_flows.items() if v in me0}
        el_valves = {v: f for v, f in valve_flows.items() if v not in me0}
        if not el_valves:
            continue
        _, my_path = solve_a(my_valves, valve_graph)
        _, el_path = solve_a(el_valves, valve_graph)

        events = list(my_path)
        events.extend(el_path)
        events.sort()
        curr_flow = 0
        curr_time = 0
        total_flow = 0
        for event_time, valve_opened in events:
            if valve_opened != 'AA':
                delta = event_time - curr_time
                total_flow += (curr_flow * delta)
                curr_flow += valve_flows[valve_opened]
                curr_time = event_time
        delta = 26 - event_time
        total_flow += (curr_flow * delta)
        soln_b = max(soln_b, total_flow)
    return soln_b


#
# Testing
#


def test_solve_a():
    valve_flows, valve_graph = parse_input('../test.txt')
    expected = 1651
    result = solve_a(valve_flows, valve_graph)


def test_solve_b():
    valve_flows, valve_graph = parse_input('../test.txt')
    expected = 1707
    result = solve_b(valve_flows, valve_graph)
    assert result == expected


#
# Main
#


def main():
    "Main program."
    import pyperclip
    # valve_flows, valve_graph = parse_input('../test.txt')
    valve_flows, valve_graph = parse_input('../input16.txt')
    soln_a, soln_path = solve_a(valve_flows, valve_graph)
    assert soln_a == 1940
    print(f"The solution to part A is {soln_a}.")
    soln_b = solve_b(valve_flows, valve_graph)
    print(f"The solution to part B is {soln_b}.")
    pyperclip.copy(str(soln_b))
    print(f"{soln_b} has been placed on the clipboard.")


if __name__ == '__main__':
    main()
