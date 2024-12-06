# -*- coding: utf-8 -*-
import sys
from copy import deepcopy

import numpy as np
from utils.utils import file, print_index, puzzle, read_file, time_and_color

sys.setrecursionlimit(10000)

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


def find_path(matrix, start, block):
    h, l = len(matrix), len(matrix[0])

    i, j = start
    c = matrix[i][j]

    if block:
        matrix[block[0]][block[1]] = "O"

    path = [start]
    path_with_d = set()
    path_with_d.add((i, j, c))

    loop = 0

    while valid_loc(i, j, h, l):

        stepi, stepj = moves_forward[c]
        i2, j2 = i + stepi, j + stepj
        if not valid_loc(i2, j2, h, l):
            break

        c2 = matrix[i2][j2]
        while c2 in ["#", "O"]:
            c = turn_right[c]
            stepi, stepj = moves_forward[c]
            i2, j2 = i + stepi, j + stepj
            if not valid_loc(i2, j2, h, l):
                break
            c2 = matrix[i2][j2]

        if (i, j) == (i2, j2):
            print(f"Found a dead end")
            loop += 1
            break

        if valid_loc(i2, j2, h, l):
            path.append([i2, j2])
            new_path = (i2, j2, c)
            if new_path in path_with_d:  # or len(path) >= h * l:
                loop += 1
                print(f"Found an infinite loop")
                break
            path_with_d.add(new_path)
            i, j = i2, j2

    if block:
        matrix[block[0]][block[1]] = "."

    return path, path_with_d, loop


def valid_loc(i, j, h, l):
    return 0 <= i < h and 0 <= j < l


def solve(part=1, elements=None):
    res = 0

    matrix = elements
    np_matrix = np.array(elements)
    h, l = np_matrix.shape
    print(f"h: {h}, l: {l}")

    start = None
    for i in range(h):
        for j in range(l):
            if matrix[i][j] in ["^", "v", ">", "<"]:
                start = [i, j]
                break

    blocks = [[]]
    if part == 2:
        for i in range(h):
            for j in range(l):
                if matrix[i][j] == ".":
                    blocks.append([i, j])

    for index, block in enumerate(blocks):
        print(f"block index: {index}")
        path, path_with_d, loop = find_path(matrix, start, block)

        if part == 1:
            res += len(list(set([f"{i}-{j}" for i, j in path])))
            print_index(matrix, path)
        elif part == 2:
            res += loop

    return res


if __name__ == "__main__":
    time_and_color(start=True)
    debug = False

    assert puzzle(file("/2024/06/example.txt"), read_file, solve, 1) == 41
    assert puzzle(file("/2024/06/input.txt"), read_file, solve, 1) == 4826
    assert puzzle(file("/2024/06/example.txt"), read_file, solve, 2) == 6
    assert puzzle(file("/2024/06/input.txt"), read_file, solve, 2) == 1721

    time_and_color(start=False)
