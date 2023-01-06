monkeys_input = """
Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1
"""

with open("puzzle.in") as f:
    monkeys_input = f.read()

monkeys = {}

for i, mnky in enumerate(monkeys_input.strip().split("\n\n")):
    _, starting, operation, test, test_true, test_false = (
        line.strip() for line in mnky.split("\n")
    )

    starting = list(map(int, starting.split(": ")[1].split(", ")))
    operation = operation.split(": ")[1].split(" = ")[1]
    divisor = int(test.split()[-1])
    true_target = int(test_true.split()[-1])
    false_target = int(test_false.split()[-1])

    monkeys[i] = {
        "items": starting,
        "operation": operation,
        "divisor": divisor,
        "score": 0,
        True: true_target,
        False: false_target,
    }

ring = 1
for m in monkeys.values():
    ring *= m["divisor"]

rounds, d = 20, 3  # part1
rounds, d = 10_000, 1  # part2
for _ in range(rounds):
    for monkey_no in range(len(monkeys)):
        monkey = monkeys[monkey_no]
        while monkey["items"]:
            monkey["score"] += 1
            old = monkey["items"].pop(0)
            final_level = (eval(monkey["operation"]) // d) % ring
            target = monkey[final_level % monkey["divisor"] == 0]
            monkeys[target]["items"].append(final_level)

p = 1
for m in sorted(v["score"] for v in monkeys.values())[-2:]:
    p *= m
print(p)
