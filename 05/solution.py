stacks = list(
    map(
        list,
        [
            "JHPMSFNV",
            "SRLMJDQ",
            "NQDHCSWB",
            "RSCL",
            "MVTPFB",
            "TRQNC",
            "GVR",
            "CZSPDLR",
            "DSJVGPBF",
        ],
    )
)


def solve_part_1():
    while command := input():
        _, times, _, start, _, to = command.split()
        for _ in range(int(times)):
            stacks[int(to) - 1].append(stacks[int(start) - 1].pop())


def solve_part_2():
    while command := input():
        _, times, _, start, _, to = command.split()
        tmp = []
        for _ in range(int(times)):
            tmp.append(stacks[int(start) - 1].pop())
        for _ in range(int(times)):
            stacks[int(to) - 1].append(tmp.pop())


# solve_part_1()
solve_part_2()
print("".join(s[-1] for s in stacks))
