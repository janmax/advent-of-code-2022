from dataclasses import dataclass
from functools import total_ordering
from heapq import *

abc = "SabcdefghijklmnopqrstuvwxyzE"

with open('puzzle.in') as f:
    heights = f.read()


@total_ordering
@dataclass(eq=False)
class Node:
    x: int
    y: int
    v: int
    d: int
    n: list["Node"]
    visited = False

    def __repr__(self):
        return f"Node(x={self.x}, y={self.y}, v={self.v}, d={self.d}, len(n)={len(self.n)}, visited={self.visited})"

    def __eq__(self, other):
        return self.d == other.d

    def __lt__(self, other):
        return self.d < other.d


sides = ((1, 0), (0, -1), (-1, 0), (0, 1))

grid = [list(line) for line in heights.strip().split("\n")]
nodes = [
    [Node(i, j, abc.find(field), 1e9, []) for j, field in enumerate(row)]
    for i, row in enumerate(grid)
]

for i, row in enumerate(nodes):
    for j, n in enumerate(row):
        if n.v == abc.find("S"):
            S = n
            S.d = 0
        if n.v == abc.find("E"):
            E = n
        for x, y in (
            (i + k, j + l)
            for k, l in sides
            if 0 <= i + k < len(nodes) and 0 <= j + l < len(row)
        ):
            if nodes[x][y].v - nodes[i][j].v <= 1:
                n.n.append(nodes[x][y])


def all_nodes():
    yield from (node for row in nodes for node in row)


def dijkstra(start_node):
    for node in all_nodes():
        node.d = 1e9 if node is not start_node else 0
        node.visited = False
    pq = [start_node]
    while pq:
        current_node = heappop(pq)
        if current_node.visited:
            continue
        for neighbor in current_node.n:
            if not neighbor.visited:
                neighbor.d = min(neighbor.d, current_node.d + 1)
                heapify(pq)
                heappush(pq, neighbor)
        current_node.visited = True
    # print('field:', start_node)
    # for row in nodes:
    #     for node in row:
    #         print('%3d' % (node.d if node.d != 1e9 else -1), end='')
    #     print()
    return E.d


print(dijkstra(S))
a_nodes = [n for n in all_nodes() if n.v <= 1]
print(min(map(dijkstra, a_nodes)))
