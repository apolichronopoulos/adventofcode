# -*- coding: utf-8 -*-
import sys

import numpy as np
from utils.utils import file, print_index, puzzle, read_file, time_and_color

sys.setrecursionlimit(10000)

matrix = []
path = []

moves_forward = {
    "^": (-1, 0),
    ">": (0, 1),
    "v": (1, 0),
    "<": (0, -1),
}

turn_right = {
    "^": ">",
    ">": "v",
    "v": "<",
    "<": "^",
}


def valid_loc(i, j, h, l):
    return 0 <= i < h and 0 <= j < l


def solve(part=1, elements=None):
    res = 0

    matrix = elements
    path.clear()

    np_matrix = np.array(elements)
    h, l = np_matrix.shape
    print(f"h: {h}, l: {l}")

    for i in range(h):
        if len(path) != 0:
            break
        for j in range(l):
            c = matrix[i][j]
            if c != "." and c != "#":
                path.append([i, j])
                break

    if debug:
        print(f"part: {part}")

    i, j = path[-1]
    c = matrix[i][j]
    while valid_loc(i, j, h, l):

        stepi, stepj = moves_forward[c]
        i2, j2 = i + stepi, j + stepj
        if not valid_loc(i2, j2, h, l):
            break

        c2 = matrix[i2][j2]
        while c2 == "#":
            c = turn_right[c]
            stepi, stepj = moves_forward[c]
            i2, j2 = i + stepi, j + stepj
            if not valid_loc(i2, j2, h, l):
                break
            c2 = matrix[i2][j2]

        if (i, j) == (i2, j2):
            print("loop")
            break

        if valid_loc(i2, j2, h, l):
            path.append([i2, j2])
            i, j = i2, j2

    if debug:
        print_index(matrix, path)

    if part == 1:
        res += len(list(set([f"{i}-{j}" for i, j in path])))

    return res


if __name__ == "__main__":
    time_and_color(start=True)
    debug = False

    assert puzzle(file("/2024/06/example.txt"), read_file, solve, 1) == 41
    assert puzzle(file("/2024/06/input.txt"), read_file, solve, 1) == 4826
    # assert puzzle(file("/2024/06/example.txt"), read_file, solve, 2) == 6
    # assert puzzle(file("/2024/06/input.txt"), read_file, solve, 2) == 0

    time_and_color(start=False)
