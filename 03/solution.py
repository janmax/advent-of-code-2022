from functools import reduce

values = " abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

with open("puzzle.in") as f:
    tests = f.read().strip().split("\n")


def contained_in_all(backpacks):
    return reduce(lambda a, b: a & b, map(set, backpacks)).pop()


part1 = ((test[: (p := len(test) // 2)], test[p:]) for test in tests)
part2 = (tests[i : i + 3] for i in range(0, len(tests), 3))

print(sum(values.find(contained_in_all(test)) for test in part1))
print(sum(values.find(contained_in_all(test)) for test in part2))
