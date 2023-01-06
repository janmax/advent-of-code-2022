forest = """
30373
25512
65332
33549
35390
"""

with open("puzzle.in") as f:
    forest = f.read()


def rotate(array):
    return [list(z) for z in zip(*array)][::-1]


forest = [list(row) for row in forest.strip().split()]
visible = [[False] * len(forest) for _ in range(len(forest))]

for side in range(4):
    for i, row in enumerate(forest):
        visible[i][0] = True
        max_height = row[0]
        for j in range(1, len(forest) - 1):
            visible[i][j] = visible[i][j] or row[j] > max_height
            max_height = max(max_height, row[j])
    forest = rotate(forest)
    visible = rotate(visible)

print(sum(sum(row) for row in visible))
