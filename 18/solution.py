puzzle = """
2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5
"""

with open("puzzle.in") as f:
    puzzle = f.read()


def add(a, b):
    return tuple(map(sum, zip(a, b)))


def sub(a, b):
    return add(a, (-1 * _b for _b in b))


cubes = {tuple(map(int, line.split(","))) for line in puzzle.strip().split("\n")}
N = max(s for point in cubes for s in point)
sides = [
    (1, 0, 0),
    (0, 1, 0),
    (0, 0, 1),
    (-1, 0, 0),
    (0, -1, 0),
    (0, 0, -1),
]

print("part1", sum(add(cube, side) not in cubes for side in sides for cube in cubes))

assert (0, 0, 0) not in cubes
stack = [(0, 0, 0)]
visited = set()
outer = 0
while stack:
    c = stack.pop()
    if c in visited:
        continue
    for side in sides:
        s = add(c, side)
        if s not in visited and min(s) >= -1 and max(s) < N + 2:
            if s in cubes:
                outer += 1
            else:
                stack.append(s)
    visited.add(c)

print("part2", outer)
