puzzle = """
Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3
"""
xy_max = 20

import re

with open("puzzle.in") as f:
    puzzle = f.read()
    xy_max = 4_000_000

p = re.compile(
    r"Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)"
)

lines = [list(map(int, p.match(line).groups())) for line in puzzle.strip().split("\n")]

blocked = set()
for sx, sy, bx, by in lines:
    blocked.add((sx, sy))
    blocked.add((bx, by))


def merge_intervals(intervals):
    intervals.sort()
    stack = intervals[:1]
    for i in intervals[1:]:
        if stack[-1][0] <= i[0] <= stack[-1][-1]:
            stack[-1][-1] = max(stack[-1][-1], i[-1])
        else:
            stack.append(i)
    return stack


part1 = [2_000_000]
part2 = range(0, xy_max + 1)
for y in part2:
    overlaps = []
    for sx, sy, bx, by in lines:
        d = abs(bx - sx) + abs(by - sy)
        n = d - abs(y - sy)
        a, b = sx - n, sx + n
        if a < b and b >= 0 and a <= xy_max:
            overlaps.append([a, b])
    overlaps = merge_intervals(overlaps)
    gaps = list(
        filter(
            lambda p: (p[0], y) not in blocked,
            (
                (x2 + 1, y1 - 1)
                for ((_, x2), (y1, _)) in zip(overlaps[:-1], overlaps[1:])
                if y1 - x2 > 1
            ),
        )
    )
    if gaps:
        print(y, overlaps)
        print(gaps)
        print(gaps[0][0] * 4000000 + y)
        break
    # part1
    # print(abs(overlaps[0][1] - overlaps[0][0]))
