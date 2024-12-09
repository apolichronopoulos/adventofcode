# -*- coding: utf-8 -*-
import sys
from functools import lru_cache
from itertools import combinations
from math import dist, hypot

import numpy as np
from utils.utils import file, print_index, puzzle, read_file, time_and_color, valid_loc

sys.setrecursionlimit(10000)


def shift_block(storage):
    stop = False
    while not stop:
        # if debug:
        #     print("".join(storage))
        first_free_space = storage.index(".")
        for j in range(len(storage) - 1, 0, -1):
            n = storage[j]
            if n != ".":
                if j > first_free_space:
                    storage[first_free_space] = n
                    storage[j] = "."
                    break
                else:
                    stop = True
    return storage


def solve(part=1, elements=None):
    res = 0
    matrix = np.array(elements)
    h, l = matrix.shape
    if debug:
        print(f"h{h}, l={l}")
        print_index(matrix)

    storages = []
    for i in range(h):
        files = True
        id = 0
        storage = []
        for j in range(l):
            for n in range(int(elements[i][j])):
                if files:
                    storage.append(str(id))
                else:
                    storage.append(".")
            if files:
                id += 1
            files = not files

        storages.append(storage)
        if debug:
            print("".join(storage))

    if part == 1:
        print(f"part: {part}")
        for storage in storages:
            storage = shift_block(storage)
            checksum = 0
            for i, n in enumerate(storage):
                if n != ".":
                    checksum += i * int(n)
            res += checksum
    else:
        print(f"part: {part}")

    return res


if __name__ == "__main__":
    time_and_color(start=True)
    debug = False

    assert puzzle(file("/2024/09/example.txt"), read_file, solve, 1) == 1928
    assert puzzle(file("/2024/09/input.txt"), read_file, solve, 1) == 6519155389266
    # assert puzzle(file("/2024/09/example.txt"), read_file, solve, 2) == 0
    # assert puzzle(file("/2024/09/input.txt"), read_file, solve, 2) == 0

    time_and_color(start=False)
