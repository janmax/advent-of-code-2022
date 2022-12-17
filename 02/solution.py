possibilities = dict(
    (
        ("A X", 4),
        ("A Y", 8),
        ("A Z", 3),
        ("B X", 1),
        ("B Y", 5),
        ("B Z", 9),
        ("C X", 7),
        ("C Y", 2),
        ("C Z", 6),
    )
)

# lose draw win
possibilities_part2 = dict(
    (
        ("A X", 3),
        ("A Y", 4),
        ("A Z", 8),
        ("B X", 1),
        ("B Y", 5),
        ("B Z", 9),
        ("C X", 2),
        ("C Y", 6),
        ("C Z", 7),
    )
)

with open("games.in") as f:
    games = f.read()

print(sum(possibilities_part2[game] for game in games.strip().split("\n")))
