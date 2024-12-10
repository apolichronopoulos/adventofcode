# -*- coding: utf-8 -*-
import sys

import numpy as np
from utils.utils import file, print_index, puzzle, read_file, time_and_color, valid_loc

sys.setrecursionlimit(20000)


def find_neighbours(x, y, h, l):
    neighbours = []
    for i, j in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        x2, y2 = x + i, y + j
        if valid_loc(x2, y2, h, l):
            neighbours.append([x2, y2])
    return neighbours


def find_paths(x, y, matrix, h, l, paths=[], path=[]):
    step = matrix[x][y]
    path.append([x, y])

    if step == 9:
        paths.append(path)
        return paths

    for x2, y2 in find_neighbours(x, y, h, l):
        if matrix[x2][y2] == step + 1:
            find_paths(x2, y2, matrix, h, l, paths, path.copy())

    return paths


def solve(part=1, elements=None):
    res = 0

    matrix = np.array(elements)
    h, l = matrix.shape
    if debug:
        print(f"h{h}, l={l}")
        print_index(matrix)

    matrix = matrix.astype(int)

    trailheads = set()
    for i in range(h):
        for j in range(l):
            if matrix[i][j] == 0:
                trailheads.add((i, j))

    all_paths = set()
    for x, y in trailheads:
        paths = find_paths(x, y, matrix, h, l, paths=[])
        for path in paths:
            x2, y2 = path[-1]
            if matrix[x2][y2] == 9:
                all_paths.add((x, y, x2, y2))
                if part == 2:
                    res += 1

    if part == 1:
        res += len(all_paths)

    return res


if __name__ == "__main__":
    time_and_color(start=True)
    debug = False

    assert puzzle(file("/2024/10/example.txt"), read_file, solve, 1) == 1
    assert puzzle(file("/2024/10/example2.txt"), read_file, solve, 1) == 36
    assert puzzle(file("/2024/10/input.txt"), read_file, solve, 1) == 667
    assert puzzle(file("/2024/10/example2.txt"), read_file, solve, 2) == 81
    assert puzzle(file("/2024/10/input.txt"), read_file, solve, 2) == 1344

    time_and_color(start=False)
