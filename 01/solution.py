with open("calories.in") as f:
    calories = f.read()

print(max(sum(map(int, elf.split("\n"))) for elf in calories.strip().split("\n\n")))
print(
    sum(
        sorted(
            sum(map(int, elf.split("\n"))) for elf in calories.strip().split("\n\n")
        )[-3:]
    )
)
