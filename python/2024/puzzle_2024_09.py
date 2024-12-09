# -*- coding: utf-8 -*-
import math
import sys

import numpy as np
from utils.utils import file, print_index, puzzle, read_file, time_and_color

sys.setrecursionlimit(20000)


def shift_block(storage):
    stop = False
    while not stop:
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


def shift_file(storage, max_id):
    if max_id < 0:
        return storage

    id = str(max_id)
    file_index = storage.index(id)
    c = 0
    for j in range(file_index, len(storage)):
        if storage[j] == id:
            c += 1
        else:
            break

    spaces = 0
    for j in range(0, file_index + 1):
        if storage[j] == ".":
            spaces += 1
        else:
            if spaces > 0:
                space_index = j - spaces
                if c <= spaces:
                    for x in range(c):
                        storage[file_index + x] = "."
                        storage[space_index + x] = id
                    return shift_file(storage, max_id - 1)
            spaces = 0

    return shift_file(storage, max_id - 1)


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

    for i, storage in enumerate(storages):
        if part == 1:
            storage = shift_block(storage)
        else:
            max_id = math.ceil(len(elements[i]) / 2) - 1
            storage = shift_file(storage, max_id)
        res += sum(i * int(n) for i, n in enumerate(storage) if n != ".")

    return res


if __name__ == "__main__":
    time_and_color(start=True)
    debug = False

    assert puzzle(file("/2024/09/example.txt"), read_file, solve, 1) == 1928
    assert puzzle(file("/2024/09/input.txt"), read_file, solve, 1) == 6519155389266
    assert puzzle(file("/2024/09/example.txt"), read_file, solve, 2) == 2858
    assert puzzle(file("/2024/09/input.txt"), read_file, solve, 2) == 6547228115826

    time_and_color(start=False)
