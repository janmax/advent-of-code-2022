with open("puzzle.in") as f:
    pairs = f.read()


def good1(line):
    (x1, x2), (y1, y2) = (map(int, p.split("-")) for p in line.split(","))
    return x1 >= y1 and x2 <= y2 or x1 <= y1 and x2 >= y2


def good2(line):
    (x1, x2), (y1, y2) = (map(int, p.split("-")) for p in line.split(","))
    return not (x2 < y1 or x1 > y2)


def solve(f):
    return sum(f(line) for line in pairs.strip().split("\n"))


print(solve(good1))
print(solve(good2))
