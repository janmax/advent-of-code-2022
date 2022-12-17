steps = """
R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20
"""

# with open("09.in") as f:
#     steps = f.read()

vectors = {
    "R": (1, 0),
    "D": (0, -1),
    "L": (-1, 0),
    "U": (0, 1),
}

moves = [line.split() for line in steps.strip().split("\n")]
rope_length = 9


def add(a, b):
    return tuple(map(sum, zip(a, b)))


def adj(a, b):
    return max(map(abs, add(a, (-1 * _b for _b in b)))) <= 1


t = (0, 0)
h = (0, 0)
T = {t}
for direction, steps in moves:
    v = vectors[direction]
    for _ in range(int(steps)):
        h_last = h
        h = add(h, v)
        if not adj(h, t):
            t = h_last
            T.add(t)

print(len(T))
