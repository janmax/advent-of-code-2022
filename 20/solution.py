puzzle = [1, 2, -3, 3, -2, 0, 4]

with open("puzzle.in") as f:
    puzzle = list(map(int, f.read().strip().split("\n")))

d, rounds = 811589153, 10
# d, rounds = 1, 1


def resize(a):
    while a >= n or a <= -n:
        a = sum(divmod(a, n))
    return a


def swap(a, i, j):
    a[i], a[j] = a[j], a[i]


n = len(puzzle)
answer = [(a * d, i, resize(a * d)) for i, a in enumerate(puzzle)]
indices = list(range(len(puzzle)))

for _ in range(rounds):
    for i in range(n):
        _, _, a = answer[indices[i]]
        sign = [1, -1][a < 0]
        if a + indices[i] < 0 or a + indices[i] >= n:
            sign *= -1
            a = n + sign * a - 1
        for _ in range(abs(a)):
            swap_to = indices[i] + sign
            original_index_of_swap = answer[swap_to][1]
            swap(answer, indices[i], swap_to)
            indices[i] += sign
            indices[original_index_of_swap] -= sign

answer = [a[0] for a in answer]
i_zero = answer.index(0)

print(sum(answer[(i_zero + i * 1000) % len(puzzle)] for i in (1, 2, 3)))
