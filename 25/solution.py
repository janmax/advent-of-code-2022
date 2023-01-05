puzzle = """
1=-0-2
12111
2=0=
21
2=01
111
20012
112
1=-1=
1-12
12
1=
122
"""

with open('puzzle.in') as f:
    puzzle = f.read()

base = 5
digits = {"2": 2, "1": 1, "0": 0, "-": -1, "=": -2}
r_digits = dict(map(reversed, digits.items()))
P = {i: base**i for i in range(20)}


def snafu_to_dec(snafu):
    return sum(
        P[power] * digits[c] for c, power in zip(reversed(snafu), range(len(snafu)))
    )


def snafu_add(a, b, carry=0):
    if not a and not b:
        return r_digits[carry] or ''
    if not a:
        return snafu_add([r_digits[carry]], b, 0)
    if not b:
        return snafu_add(a, [r_digits[carry]], 0)
    *a_head, a = a
    *b_head, b = b
    s = digits[a] + digits[b] + carry
    if s < -2:
        carry = -1
    elif s > 2:
        carry = 1
    else:
        carry = 0
    s = [0, 1, 2, -2, -1][s % base]
    # print(a, b, s, carry)
    return snafu_add(a_head, b_head, carry) + r_digits[s]


from functools import reduce

numbers = list(line for line in puzzle.strip().split("\n"))


def check(i, j):
    print(numbers[i], snafu_to_dec(numbers[i]))
    print(numbers[j], snafu_to_dec(numbers[j]))
    s = snafu_add(numbers[i], numbers[j])
    print("n[i] + n[j] = ", s)
    print("check", sum(map(snafu_to_dec, (numbers[i], numbers[j]))), snafu_to_dec(s))


check(3, 2)
check(3, 6)

n = reduce(snafu_add, numbers)
print(n)
