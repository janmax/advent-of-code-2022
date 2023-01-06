with open("puzzle.in") as f:
    forest = f.read()


def rotate(array):
    return [list(z) for z in zip(*array)][::-1]


forest = [list(row) for row in forest.strip().split()]
scenic = [[1] * len(forest) for _ in range(len(forest))]


for side in ("right", "down", "left", "up"):
    for i in range(1, len(forest) - 1):
        for j in range(1, len(forest) - 1):
            height = forest[i][j]
            distance = 1
            while j + distance < len(forest) - 1 and forest[i][j + distance] < height:
                distance += 1
            # print(f'{side=} {i=} {j=} {height=} {distance=}')
            scenic[i][j] *= distance
    forest = rotate(forest)
    scenic = rotate(scenic)

print(max(max(row) for row in scenic))
