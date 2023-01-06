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

# puzzle = '''
# Valve AA has flow rate=0; tunnels lead to valves BB, CC
# Valve BB has flow rate=1; tunnels lead to valves AA, FF
# Valve CC has flow rate=1; tunnels lead to valves AA, DD
# Valve DD has flow rate=0; tunnels lead to valves CC, EE
# Valve EE has flow rate=1; tunnels lead to valves DD
# Valve FF has flow rate=4; tunnels lead to valves BB
# '''

# puzzle = '''
# Valve AA has flow rate=0; tunnels lead to valves BB, DD
# Valve BB has flow rate=0; tunnels lead to valves AA, CC
# Valve CC has flow rate=1; tunnels lead to valves BB
# Valve DD has flow rate=1; tunnels lead to valves AA, EE
# Valve EE has flow rate=1; tunnels lead to valves DD, FF
# Valve FF has flow rate=1; tunnels lead to valves EE
# '''

with open('puzzle.in') as f:
    puzzle = f.read()

import re
# import numpy as np

# from scipy.sparse.csgraph import dijkstra
# from collections import namedtuple

# +
p = re.compile(r"Valve (\w{2}) has flow rate=(\d+); tunnels? leads? to valves? (.*)")

data = []
for line in puzzle.strip().split("\n"):
    node, flow, tunnels = p.match(line).groups()
    data.append((node, int(flow), tunnels.split(", ")))
# if there is a valve at AA we can reach & open it in one step
data.insert(0, ("start", 0, ["AA"]))
flows = [0] + [flow for _, flow, _ in data if flow]

# # Build an adjacency matrix
# G = np.zeros((len(data), len(data)), dtype=int)
# to_number = {name: i for i, (name, _, _) in enumerate(data)}
# for name, flow, tunnels in data:
#     for tunnel in tunnels:
#         G[to_number[name], to_number[tunnel]] = 1

# non_zero_flow = np.array([0] + [to_number[name] for name, flow, _ in data if flow])

# # use scipy for simplicity
# D = dijkstra(G)
# # remove zero nodes we will never visit for themselves
# D = D[non_zero_flow, :][:, non_zero_flow]
# # add cost of opening valve to paths
# D = np.vstack((D[0], D[1:] + 1))
# D[D == np.inf] = 0
# D = D.astype(int)


# # part1
# def dfs(node, remaining, flow, output, to_visit, walk=[]):
#     # print(node, remaining, flow, output, to_visit, walk)
#     if remaining <= 0:
#         return output, walk
#     return max(
#         [(output + (flow + flows[node]) * max(0, remaining), walk)]
#         + [
#             dfs(
#                 i,
#                 remaining - D[node, i],
#                 flow + flows[node],
#                 output + (flow + flows[node]) * D[node, i],
#                 to_visit - {i},
#                 walk + [i],
#             )
#             for i in to_visit
#             if not remaining - D[node, i] < 0
#         ]
#     )


# dfs(0, 30, 0, 0, set(range(1, D.shape[0])))

# np.array([flows]), D
# D = D.tolist()
# -

D = [
    [0, 6, 6, 4, 9, 4, 8, 8, 4, 4, 9, 6, 7, 3, 6, 5],
    [0, 1, 9, 4, 4, 7, 11, 3, 4, 9, 12, 9, 10, 4, 11, 6],
    [0, 9, 1, 6, 12, 3, 3, 11, 8, 5, 4, 3, 6, 8, 7, 8],
    [0, 4, 6, 1, 7, 4, 8, 6, 3, 7, 9, 6, 7, 4, 9, 6],
    [0, 4, 12, 7, 1, 10, 14, 6, 7, 12, 15, 12, 13, 7, 14, 9],
    [0, 7, 3, 4, 10, 1, 5, 9, 6, 5, 6, 3, 4, 6, 7, 8],
    [0, 11, 3, 8, 14, 5, 1, 13, 10, 7, 4, 5, 8, 10, 9, 10],
    [0, 3, 11, 6, 6, 9, 13, 1, 6, 11, 14, 11, 12, 6, 13, 8],
    [0, 4, 8, 3, 7, 6, 10, 6, 1, 7, 11, 8, 9, 3, 9, 4],
    [0, 9, 5, 7, 12, 5, 7, 11, 7, 1, 6, 3, 8, 6, 3, 4],
    [0, 12, 4, 9, 15, 6, 4, 14, 11, 6, 1, 4, 9, 11, 8, 9],
    [0, 9, 3, 6, 12, 3, 5, 11, 8, 3, 4, 1, 6, 8, 5, 6],
    [0, 10, 6, 7, 13, 4, 8, 12, 9, 8, 9, 6, 1, 9, 10, 11],
    [0, 4, 8, 4, 7, 6, 10, 6, 3, 6, 11, 8, 9, 1, 8, 3],
    [0, 11, 7, 9, 14, 7, 9, 13, 9, 3, 8, 5, 10, 8, 1, 6],
    [0, 6, 8, 6, 9, 8, 10, 8, 4, 4, 9, 6, 11, 3, 6, 1],
]

# +
# %%time
from itertools import product, cycle, permutations
from collections import namedtuple

Agent = namedtuple("Agent", "time target id")
Option = namedtuple(
    "Option",
    "clock remaining agents previous",
)


def solve(A, M, S):
    max_output = 0
    stopped = -1
    options = [
        Option(
            M,
            {stopped} | set(range(1, len(D))),
            [Agent(0, 0, a) for a in A],
            [],
        )
    ]

    options_seen = 0
    while options:
        current = options.pop()
        options_seen += 1
        # print(f"Remaining options: {len(options):04d} clock: {current.clock:02d}", end="\r")

        active_agents = [agent for agent in current.agents if agent.time == 0]
        inactive_agents = [agent for agent in current.agents if agent.time != 0]
        conditions = (
            not current.remaining - {-1},
            all(
                D[agent.target][unvisited] > current.clock
                for agent in active_agents
                for unvisited in current.remaining
            ),
        )

        # FIXME find out why this contains duplicates
        if any(conditions):
            final_output = sum(flow * time for time, flow, _, _ in current.previous)
            max_output = max(max_output, final_output)
            #             print()
            #             print("FINAL:", current)
            print(
                f"Achieved final_output={final_output:4} max_output={max_output} options_seen={options_seen}",
                end="\r",
            )
            #             for p in current.previous:
            #                 print(p)
            continue

        if (
            sum(flow * time for time, flow, _, _ in current.previous)
            + (
                sum(flow for _, flow, _, _ in current.previous)
                + sum(
                    sorted(
                        flows[i]
                        for i in current.remaining - {-1}
                        if any(
                            D[a.target][i] < current.clock - a.time - 2
                            for a in current.agents
                        )
                    )[-current.clock // 2 :]
                )
            )
            * current.clock
            < max_output
        ):
            continue

        #     print()
        #     print("CURRENT:", current)
        for targets in permutations(current.remaining, r=len(active_agents)):
            # At the beginning the human goes for the
            # smaller letters if distances are the same.
            # Should cut options in half.
            if (
                len(current.agents) == 2
                and current.agents[0].target == current.agents[1].target
                and all(a.time == 0 for a in current.agents)
                and targets[0] < targets[1]
            ):
                continue
            # Since we get all the permutations we want to
            # ignore those where both agents would reach the
            # others target faster.
            if (
                len(active_agents) == 2
                and D[active_agents[0].target][targets[0]]
                > D[active_agents[1].target][targets[0]]
                and D[active_agents[0].target][targets[1]]
                < D[active_agents[1].target][targets[1]]
            ):
                continue

            actions = [
                Agent(
                    D[agent.target][target],
                    target,
                    agent.id,
                )
                for agent, target in zip(active_agents, targets)
                if target != stopped
            ]
            if any(action.time > current.clock for action in actions):
                continue

            next_action = [a for a in actions + inactive_agents]
            if not next_action:
                continue
            next_action_in = min(next_action).time if next_action else 0

            options.append(
                Option(
                    current.clock - next_action_in,
                    current.remaining - set(a.target for a in actions) | {stopped},
                    [
                        Agent(action.time - next_action_in, action.target, action.id)
                        for action in actions + inactive_agents
                    ],
                    current.previous
                    + [
                        (current.clock - a.time, flows[a.target], a.target, a.id)
                        for a in actions
                    ],
                )
            )
    #             print("APPENDED:", options[-1])
    print()
    print(
        "options seen", options_seen, "output", max_output, "correct", max_output == S
    )


# solve("h", 30, 1651)
solve("he", 26, 1707)
# -




