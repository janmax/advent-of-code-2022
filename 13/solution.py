from functools import cmp_to_key

with open("puzzle.in") as f:
    packets = f.read()


packet_pairs = list(
    list(map(eval, pair.split("\n"))) for pair in packets.strip().split("\n\n")
)


def list_cmp_is_smaller(a, b):
    if not a and not b:
        return 0
    if not a and b:
        return -1
    if a and not b:
        return 1
    x, y = a[0], b[0]
    # print(x, y)
    match [x, y]:
        case [int(), int()]:
            cmp = x - y
        case [int(), list()]:
            cmp = list_cmp_is_smaller([x], y)
        case [list(), int()]:
            cmp = list_cmp_is_smaller(x, [y])
        case [list(), list()]:
            cmp = list_cmp_is_smaller(x, y)
    if cmp != 0:
        return cmp
    return list_cmp_is_smaller(a[1:], b[1:])


s = 0
s = sum(i + 1 for i, (a, b) in enumerate(packet_pairs) if list_cmp_is_smaller(a, b) < 0)
print("part1:", s)

d1, d2 = [[2]], [[6]]
flat = [d1, d2, *(packet for pair in packet_pairs for packet in pair)]

stream = sorted(flat, key=cmp_to_key(list_cmp_is_smaller))
print("part2:", (stream.index(d1) + 1) * (stream.index(d2) + 1))
