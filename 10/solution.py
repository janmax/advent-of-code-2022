points = list(range(0, 40 * 7, 40))

with open("instructions.in") as f:
    instructions = f.read()

instr = instructions.strip().split("\n")
X = 1
C = 1
signals = []
to_add = []
busy_for = 0
for C in range(1, 241):
    if not busy_for:
        instruction = instr.pop(0)
        if instruction == "noop":
            busy_for = 1
        elif instruction.startswith("addx"):
            busy_for = 2
            to_add.append(int(instruction[5:]))
        # print(f'start {C=} {instruction=} {X=}, {to_add=}')
    if X - 1 <= (C - 1) % 40 <= X + 1:
        print("#", end="")
    else:
        print(".", end="")
    if C in points:
        # print(C, X)
        signals.append(C * X)
        print()
    busy_for -= 1
    if not busy_for and to_add:
        X += to_add.pop()
    # print(f'end {C=} with {X=}')

print(sum(signals))
