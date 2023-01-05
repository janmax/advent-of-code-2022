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
data.insert(0, ("start", 0, ["AA"]))

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

np.array([flows]), D

# +
# %%time
from itertools import product, cycle, permutations

Agent = namedtuple("Agent", "time target id")
Option = namedtuple(
    "Option",
    "output flow clock remaining agents previous",
)


def solve(A, M, S):
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

        active_agents = [agent for agent in current.agents if agent.time == 0]
        inactive_agents = [agent for agent in current.agents if agent.time != 0]
        conditions = (
            not current.remaining - {-1},
            all(
                D[agent.target, unvisited] > current.clock
                for agent in active_agents
                for unvisited in current.remaining
            ),
        )
        if any(conditions):
            final_output = sum(flow * time for time, flow, _, _ in set(current.previous))
            max_output = max(max_output, final_output)
#             print()
#             print("FINAL:", current)
#             print(f"Achieved {final_output=} {max_output=} {options_seen=}", end="\n")
#             for p in current.previous:
#                 print(p)
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

        #     print()
        #     print("CURRENT:", current)
        for targets in permutations(current.remaining, r=len(active_agents)):
            if (
                len(current.agents) == 2
                and current.agents[0].target == current.agents[1].target
                and all(a.time == 0 for a in current.agents)
                and targets[0] < targets[1]
            ):
                continue
            actions = [
                Agent(
                    D[agent.target, target] if target != stopped else 99,
                    target,
                    agent.id,
                )
                for agent, target in zip(active_agents, targets)
            ]
            if any(
                action.time > current.clock
                for action in actions
                if action.target != stopped
            ):
                continue

            next_action = [a for a in actions + inactive_agents if a.target != stopped]
            if not next_action:
                continue
            next_action_in = min(next_action).time if next_action else 0

            added_flow = sum(
                flows[agent.target]
                for agent in actions + inactive_agents
                if agent.time == next_action_in
            )

            options.append(
                Option(
                    current.output + current.flow * next_action_in,
                    current.flow + added_flow,
                    current.clock - next_action_in,
                    current.remaining - set(a.target for a in actions) | {stopped},
                    [
                        Agent(action.time - next_action_in, action.target, action.id)
                        for action in actions + inactive_agents
                        if action.target != stopped
                    ],
                    current.previous
                    + [(current.clock - a.time, flows[a.target], a.target, a.id) for a in next_action],
                )
            )
#             print("APPENDED:", options[-1])
    print(
        "options seen", options_seen, "output", max_output, "correct", max_output == S
    )


solve("h", 30, 1651)
# solve("he", 26, 1707)
# -


