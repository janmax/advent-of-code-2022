# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.14.4
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# +
puzzle = '''
Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II
'''

puzzle = '''
Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II
'''

with open('puzzle.in') as f:
    puzzle = f.read()

import re
import numpy as np

from scipy.sparse.csgraph import dijkstra
from collections import namedtuple

# +
p = re.compile(r"Valve (\w{2}) has flow rate=(\d+); tunnels? leads? to valves? (.*)")

data: list[tuple[str, int, list[str]]] = []
for line in puzzle.strip().split("\n"):
    node, flow, tunnels = p.match(line).groups()
    data.append((node, int(flow), tunnels.split(", ")))
# if there is a valve at AA we can reach & open it in one step
data.insert(0, ('start', 0, ['AA']))

# Build an adjacency matrix
G = np.zeros((len(data), len(data)), dtype=int)
to_number = {name: i for i, (name, _, _) in enumerate(data)}
for name, flow, tunnels in data:
    for tunnel in tunnels:
        G[to_number[name], to_number[tunnel]] = 1

non_zero_flow = np.array([0] + [to_number[name] for name, flow, _ in data if flow])
flows = [0] + [flow for _, flow, _ in data if flow]

# use scipy for simplicity
D = dijkstra(G)
# remove zero nodes we will never visit for themself
D = D[non_zero_flow, :][:, non_zero_flow]
# add cost of opening valve to paths
D = np.vstack((D[0], D[1:] + 1))
D[D == np.inf] = 0
D = D.astype(int)


# part1
def dfs(node, remaining, flow, output, to_visit, walk=[]):
    # print(node, remaining, flow, output, to_visit, walk)
    if remaining <= 0:
        return output, walk
    return max(
        [(output + (flow + flows[node]) * max(0, remaining), walk)]
        + [
            dfs(
                i,
                remaining - D[node, i],
                flow + flows[node],
                output + (flow + flows[node]) * D[node, i],
                to_visit - {i},
                walk + [i],
            )
            for i in to_visit
            if not remaining - D[node, i] < 0
        ]
    )


dfs(0, 30, 0, 0, set(range(1, D.shape[0])))

# +
# part2
from itertools import product, cycle, permutations

Agent = namedtuple("Agent", "time target id")
Option = namedtuple(
    "Option",
    "output flow clock remaining agents previous",
)

A, M, S = "h", 30, 1828
A, M, S = "he", 26, 0

max_output = 0
stopped = -1
options = [
    Option(
        0,
        0,
        M,
        {stopped} | set(range(1, D.shape[0])),
        [Agent(0, 0, a) for a in A],
        [],
    )
]

options_seen = 0

while options:
    current = options.pop()
    options_seen += 1
    # print(f"Remaining options: {len(options):04d} clock: {current.clock:02d}", end="\r")

    #     print(current)
    active_agents = [
        agent for agent in current.agents if agent.time == 0 and agent.target != stopped
    ]
    inactive_agents = [
        agent for agent in current.agents if agent.time != 0 or agent.target == stopped
    ]
    #     print(current)
    #     print(active_agents)
    #     print(inactive_agents)
    conditions = (
        not current.remaining,
        not active_agents,
        all(
            D[agent.target, unvisited] > current.clock
            for agent in active_agents
            for unvisited in current.remaining
        ),
    )
    if any(conditions):
        last_state = current.previous[-1]
        max_output = max(max_output, last_state[0] + last_state[1] * last_state[2])
        #         print(conditions)
        print(f"Achieved {max_output=} {options_seen}", end="\r")
        #         for p in current.previous:
        #             print(p)
        continue

    if (
        current.output
        + (
            current.flow
            + sum(
                flows[i]
                for i in current.remaining | {a.target for a in current.agents}
                if i != -1
                and all(D[a.target, i] < current.clock for a in current.agents)
            )
        )
        * current.clock
        < max_output
    ):
        continue

    #     print('CURRENT:', current)
    for targets in permutations(current.remaining, r=len(active_agents)):
        actions = [
            Agent(
                D[agent.target, target] if target != stopped else -1, target, agent.id
            )
            for agent, target in zip(active_agents, targets)
        ]
        if any(action.time > current.clock for action in actions):
            continue
        # print(actions)
        next_action = [a for a in actions + inactive_agents if a.time != stopped]
        next_action_in = min(next_action).time if next_action else 0
        # print(next_action_in)

        finished_next = [
            flows[agent.target]
            for agent in actions + inactive_agents
            if agent.time == next_action_in
        ]
        added_flow = sum(finished_next)
        # print(finished_next)

        options.append(
            Option(
                current.output + current.flow * next_action_in,
                current.flow + added_flow,
                current.clock - next_action_in,
                current.remaining - set(a.target for a in actions) | {stopped},
                [
                    Agent(action.time - next_action_in, action.target, action.id)
                    for action in actions + inactive_agents
                ],
                current.previous
                + [(current.output, current.flow, current.clock, actions)],
            )
        )


print("options seen", options_seen, "output", max_output, "correct", max_output == S)
# -



o = Option(
    output=1055,
    flow=122,
    clock=3,
    remaining={4, 5, 6, -1, 10, 14},
    agents=[Agent(time=1, target=8, id="h"), Agent(time=0, target=11, id="e")],
    previous=[
        (
            0,
            0,
            26,
            [Agent(time=5, target=15, id="h"), Agent(time=7, target=12, id="e")],
        ),
        (0, 9, 21, [Agent(time=3, target=13, id="h")]),
        (18, 34, 19, [Agent(time=8, target=9, id="e")]),
        (52, 42, 18, [Agent(time=6, target=7, id="h")]),
        (304, 55, 12, [Agent(time=3, target=1, id="h")]),
        (359, 65, 11, [Agent(time=5, target=2, id="e")]),
        (489, 82, 9, [Agent(time=4, target=3, id="h")]),
        (735, 104, 6, [Agent(time=3, target=11, id="e")]),
        (839, 108, 5, [Agent(time=3, target=8, id="h")]),
    ],
)
r = list(o.remaining)
r, D[8, np.array(r)]

r = list({4, 6, 8, 11, 12, -1})
r, D[5, np.array(r)]

CURRENT: Option(
    output=938,
    flow=115,
    clock=6,
    remaining={4, 6, 8, 11, 12, -1},
    agents=[Agent(time=3, target=10, id="h"), Agent(time=0, target=5, id="e")],
    previous=[
        (
            0,
            0,
            26,
            [Agent(time=5, target=15, id="h"), Agent(time=3, target=13, id="e")],
        ),
        (0, 8, 23, [Agent(time=4, target=1, id="e")]),
        (16, 17, 21, [Agent(time=4, target=9, id="h")]),
        (50, 34, 19, [Agent(time=3, target=7, id="e")]),
        (118, 44, 17, [Agent(time=3, target=14, id="h")]),
        (162, 57, 16, [Agent(time=6, target=3, id="e")]),
        (276, 78, 14, [Agent(time=7, target=2, id="h")]),
        (588, 82, 10, [Agent(time=4, target=5, id="e")]),
        (834, 104, 7, [Agent(time=4, target=10, id="h")]),
    ],
)
Option(
    output=1283,
    flow=127,
    clock=3,
    remaining={4, 8, 11, 12, -1},
    agents=[Agent(time=2, target=6, id="e"), Agent(time=0, target=10, id="h")],
    previous=[
        (
            0,
            0,
            26,
            [Agent(time=5, target=15, id="h"), Agent(time=3, target=13, id="e")],
        ),
        (0, 8, 23, [Agent(time=4, target=1, id="e")]),
        (16, 17, 21, [Agent(time=4, target=9, id="h")]),
        (50, 34, 19, [Agent(time=3, target=7, id="e")]),
        (118, 44, 17, [Agent(time=3, target=14, id="h")]),
        (162, 57, 16, [Agent(time=6, target=3, id="e")]),
        (276, 78, 14, [Agent(time=7, target=2, id="h")]),
        (588, 82, 10, [Agent(time=4, target=5, id="e")]),
        (834, 104, 7, [Agent(time=4, target=10, id="h")]),
        (938, 115, 6, [Agent(time=5, target=6, id="e")]),
    ],
)
Option(
    output=1283,
    flow=127,
    clock=3,
    remaining={4, 6, 11, 12, -1},
    agents=[Agent(time=3, target=8, id="e"), Agent(time=0, target=10, id="h")],
    previous=[
        (
            0,
            0,
            26,
            [Agent(time=5, target=15, id="h"), Agent(time=3, target=13, id="e")],
        ),
        (0, 8, 23, [Agent(time=4, target=1, id="e")]),
        (16, 17, 21, [Agent(time=4, target=9, id="h")]),
        (50, 34, 19, [Agent(time=3, target=7, id="e")]),
        (118, 44, 17, [Agent(time=3, target=14, id="h")]),
        (162, 57, 16, [Agent(time=6, target=3, id="e")]),
        (276, 78, 14, [Agent(time=7, target=2, id="h")]),
        (588, 82, 10, [Agent(time=4, target=5, id="e")]),
        (834, 104, 7, [Agent(time=4, target=10, id="h")]),
        (938, 115, 6, [Agent(time=6, target=8, id="e")]),
    ],
)
Option(
    output=1283,
    flow=141,
    clock=3,
    remaining={4, 6, 8, 12, -1},
    agents=[Agent(time=0, target=11, id="e"), Agent(time=0, target=10, id="h")],
    previous=[
        (
            0,
            0,
            26,
            [Agent(time=5, target=15, id="h"), Agent(time=3, target=13, id="e")],
        ),
        (0, 8, 23, [Agent(time=4, target=1, id="e")]),
        (16, 17, 21, [Agent(time=4, target=9, id="h")]),
        (50, 34, 19, [Agent(time=3, target=7, id="e")]),
        (118, 44, 17, [Agent(time=3, target=14, id="h")]),
        (162, 57, 16, [Agent(time=6, target=3, id="e")]),
        (276, 78, 14, [Agent(time=7, target=2, id="h")]),
        (588, 82, 10, [Agent(time=4, target=5, id="e")]),
        (834, 104, 7, [Agent(time=4, target=10, id="h")]),
        (938, 115, 6, [Agent(time=3, target=11, id="e")]),
    ],
)
Option(
    output=1283,
    flow=127,
    clock=3,
    remaining={4, 6, 8, 11, -1},
    agents=[Agent(time=1, target=12, id="e"), Agent(time=0, target=10, id="h")],
    previous=[
        (
            0,
            0,
            26,
            [Agent(time=5, target=15, id="h"), Agent(time=3, target=13, id="e")],
        ),
        (0, 8, 23, [Agent(time=4, target=1, id="e")]),
        (16, 17, 21, [Agent(time=4, target=9, id="h")]),
        (50, 34, 19, [Agent(time=3, target=7, id="e")]),
        (118, 44, 17, [Agent(time=3, target=14, id="h")]),
        (162, 57, 16, [Agent(time=6, target=3, id="e")]),
        (276, 78, 14, [Agent(time=7, target=2, id="h")]),
        (588, 82, 10, [Agent(time=4, target=5, id="e")]),
        (834, 104, 7, [Agent(time=4, target=10, id="h")]),
        (938, 115, 6, [Agent(time=4, target=12, id="e")]),
    ],
)
Option(
    output=1283,
    flow=127,
    clock=3,
    remaining={4, 6, 8, 11, 12, -1},
    agents=[Agent(time=-4, target=-1, id="e"), Agent(time=0, target=10, id="h")],
    previous=[
        (
            0,
            0,
            26,
            [Agent(time=5, target=15, id="h"), Agent(time=3, target=13, id="e")],
        ),
        (0, 8, 23, [Agent(time=4, target=1, id="e")]),
        (16, 17, 21, [Agent(time=4, target=9, id="h")]),
        (50, 34, 19, [Agent(time=3, target=7, id="e")]),
        (118, 44, 17, [Agent(time=3, target=14, id="h")]),
        (162, 57, 16, [Agent(time=6, target=3, id="e")]),
        (276, 78, 14, [Agent(time=7, target=2, id="h")]),
        (588, 82, 10, [Agent(time=4, target=5, id="e")]),
        (834, 104, 7, [Agent(time=4, target=10, id="h")]),
        (938, 115, 6, [Agent(time=-1, target=-1, id="e")]),
    ],
)
CURRENT: Option(
    output=938,
    flow=115,
    clock=6,
    remaining={4, 8, 10, 11, 12, -1},
    agents=[Agent(time=2, target=6, id="h"), Agent(time=0, target=5, id="e")],
    previous=[
        (
            0,
            0,
            26,
            [Agent(time=5, target=15, id="h"), Agent(time=3, target=13, id="e")],
        ),
        (0, 8, 23, [Agent(time=4, target=1, id="e")]),
        (16, 17, 21, [Agent(time=4, target=9, id="h")]),
        (50, 34, 19, [Agent(time=3, target=7, id="e")]),
        (118, 44, 17, [Agent(time=3, target=14, id="h")]),
        (162, 57, 16, [Agent(time=6, target=3, id="e")]),
        (276, 78, 14, [Agent(time=7, target=2, id="h")]),
        (588, 82, 10, [Agent(time=4, target=5, id="e")]),
        (834, 104, 7, [Agent(time=3, target=6, id="h")]),
    ],
)
Option(
    output=1168,
    flow=138,
    clock=4,
    remaining={4, 10, 11, 12, -1},
    agents=[Agent(time=4, target=8, id="e"), Agent(time=0, target=6, id="h")],
    previous=[
        (
            0,
            0,
            26,
            [Agent(time=5, target=15, id="h"), Agent(time=3, target=13, id="e")],
        ),
        (0, 8, 23, [Agent(time=4, target=1, id="e")]),
        (16, 17, 21, [Agent(time=4, target=9, id="h")]),
        (50, 34, 19, [Agent(time=3, target=7, id="e")]),
        (118, 44, 17, [Agent(time=3, target=14, id="h")]),
        (162, 57, 16, [Agent(time=6, target=3, id="e")]),
        (276, 78, 14, [Agent(time=7, target=2, id="h")]),
        (588, 82, 10, [Agent(time=4, target=5, id="e")]),
        (834, 104, 7, [Agent(time=3, target=6, id="h")]),
        (938, 115, 6, [Agent(time=6, target=8, id="e")]),
    ],
)
Option(
    output=1168,
    flow=138,
    clock=4,
    remaining={4, 8, 11, 12, -1},
    agents=[Agent(time=4, target=10, id="e"), Agent(time=0, target=6, id="h")],
    previous=[
        (
            0,
            0,
            26,
            [Agent(time=5, target=15, id="h"), Agent(time=3, target=13, id="e")],
        ),
        (0, 8, 23, [Agent(time=4, target=1, id="e")]),
        (16, 17, 21, [Agent(time=4, target=9, id="h")]),
        (50, 34, 19, [Agent(time=3, target=7, id="e")]),
        (118, 44, 17, [Agent(time=3, target=14, id="h")]),
        (162, 57, 16, [Agent(time=6, target=3, id="e")]),
        (276, 78, 14, [Agent(time=7, target=2, id="h")]),
        (588, 82, 10, [Agent(time=4, target=5, id="e")]),
        (834, 104, 7, [Agent(time=3, target=6, id="h")]),
        (938, 115, 6, [Agent(time=6, target=10, id="e")]),
    ],
)
Option(
    output=1168,
    flow=138,
    clock=4,
    remaining={4, 8, 10, 12, -1},
    agents=[Agent(time=1, target=11, id="e"), Agent(time=0, target=6, id="h")],
    previous=[
        (
            0,
            0,
            26,
            [Agent(time=5, target=15, id="h"), Agent(time=3, target=13, id="e")],
        ),
        (0, 8, 23, [Agent(time=4, target=1, id="e")]),
        (16, 17, 21, [Agent(time=4, target=9, id="h")]),
        (50, 34, 19, [Agent(time=3, target=7, id="e")]),
        (118, 44, 17, [Agent(time=3, target=14, id="h")]),
        (162, 57, 16, [Agent(time=6, target=3, id="e")]),
        (276, 78, 14, [Agent(time=7, target=2, id="h")]),
        (588, 82, 10, [Agent(time=4, target=5, id="e")]),
        (834, 104, 7, [Agent(time=3, target=6, id="h")]),
        (938, 115, 6, [Agent(time=3, target=11, id="e")]),
    ],
)
Option(
    output=1168,
    flow=138,
    clock=4,
    remaining={4, 8, 10, 11, -1},
    agents=[Agent(time=2, target=12, id="e"), Agent(time=0, target=6, id="h")],
    previous=[
        (
            0,
            0,
            26,
            [Agent(time=5, target=15, id="h"), Agent(time=3, target=13, id="e")],
        ),
        (0, 8, 23, [Agent(time=4, target=1, id="e")]),
        (16, 17, 21, [Agent(time=4, target=9, id="h")]),
        (50, 34, 19, [Agent(time=3, target=7, id="e")]),
        (118, 44, 17, [Agent(time=3, target=14, id="h")]),
        (162, 57, 16, [Agent(time=6, target=3, id="e")]),
        (276, 78, 14, [Agent(time=7, target=2, id="h")]),
        (588, 82, 10, [Agent(time=4, target=5, id="e")]),
        (834, 104, 7, [Agent(time=3, target=6, id="h")]),
        (938, 115, 6, [Agent(time=4, target=12, id="e")]),
    ],
)
Option(
    output=1168,
    flow=138,
    clock=4,
    remaining={4, 8, 10, 11, 12, -1},
    agents=[Agent(time=-3, target=-1, id="e"), Agent(time=0, target=6, id="h")],
    previous=[
        (
            0,
            0,
            26,
            [Agent(time=5, target=15, id="h"), Agent(time=3, target=13, id="e")],
        ),
        (0, 8, 23, [Agent(time=4, target=1, id="e")]),
        (16, 17, 21, [Agent(time=4, target=9, id="h")]),
        (50, 34, 19, [Agent(time=3, target=7, id="e")]),
        (118, 44, 17, [Agent(time=3, target=14, id="h")]),
        (162, 57, 16, [Agent(time=6, target=3, id="e")]),
        (276, 78, 14, [Agent(time=7, target=2, id="h")]),
        (588, 82, 10, [Agent(time=4, target=5, id="e")]),
        (834, 104, 7, [Agent(time=3, target=6, id="h")]),
        (938, 115, 6, [Agent(time=-1, target=-1, id="e")]),
    ],
)
