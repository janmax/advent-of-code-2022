with open("puzzle.in") as f:
    test = f.read()


def solve(n):
    z = zip(*(test[i : -n + i] for i in range(n)))
    r = min(i for i, marker in enumerate(z) if len(set(marker)) == n)
    return r + n


print(solve(4))
print(solve(14))
