with open("puzzle.in") as f:
    steps = f.read()

vectors = {
    "R": (1, 0),
    "D": (0, -1),
    "L": (-1, 0),
    "U": (0, 1),
}

moves = [line.split() for line in steps.strip().split("\n")]


def add(a, b):
    return tuple(map(sum, zip(a, b)))


def sub(a, b):
    return add(a, (-1 * _b for _b in b))


def solve(rope_length):
    r = {i: (0, 0) for i in range(rope_length)}
    T = {(0, 0)}
    for direction, steps in moves:
        v = vectors[direction]
        for _ in range(int(steps)):
            r[0] = add(r[0], v)
            for i in range(1, rope_length):
                diff = sub(r[i - 1], r[i])
                if not max(map(abs, diff)) <= 1:  # adjecency
                    vv = (x // 2 if x % 2 == 0 else x for x in diff)
                    r[i] = add(r[i], vv)
                    T.add(r[rope_length - 1])
                else:
                    break
    return len(T)


print(solve(2))
print(solve(10))
