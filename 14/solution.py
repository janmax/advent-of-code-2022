cave = """
498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
"""

with open("puzzle.in") as f:
    cave = f.read()

from collections import namedtuple

Point = namedtuple("Point", "x y")

rocks = [
    [Point(*map(int, point.split(","))) for point in line.split(" -> ")]
    for line in cave.strip().split("\n")
]


def add(a, b):
    return tuple(map(sum, zip(a, b)))


def sub(a, b):
    return add(a, (-1 * _b for _b in b))


cave = {}
for line in rocks:
    for a, b in zip(line[:-1], line[1:]):
        dX, dY = sub(b, a)
        for dx in range(0, dX):
            cave[Point(a.x + dx, a.y)] = "#"
        for dx in range(dX, 0):
            cave[Point(a.x + dx, a.y)] = "#"
        for dy in range(0, dY):
            cave[Point(a.x, a.y + dy)] = "#"
        for dy in range(dY, 0):
            cave[Point(a.x, a.y + dy)] = "#"
        cave[a] = "#"
        cave[b] = "#"
y_max = max(p.y for p in cave)


def print_cave():
    x_min = min(p.x for p in cave)
    x_max = max(p.x for p in cave)
    for y in range(0, y_max + 3):
        for x in range(x_min - 1, x_max + 2):
            c = "."
            if Point(x, y) in cave:
                c = cave[Point(x, y)]
            print(c, end="")
        print()


part2 = True

while True:
    # print_cave()
    s = Point(500, 0)
    while True:
        if part2 and s.y == y_max + 1:
            cave[s] = "o"
            break
        elif (n := Point(s.x, s.y + 1)) not in cave:
            s = n
        elif (n := Point(s.x - 1, s.y + 1)) not in cave:
            s = n
        elif (n := Point(s.x + 1, s.y + 1)) not in cave:
            s = n
        else:
            cave[s] = "o"
            break
        if not part2 and s.y > y_max:
            break
    if part2 and s == Point(500, 0):
        break
    if not part2 and s.y > y_max:
        break

print(sum(v == "o" for v in cave.values()))
