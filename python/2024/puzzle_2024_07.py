# -*- coding: utf-8 -*-
import sys

from utils.utils import file, print_index, puzzle, read_file, time_and_color

sys.setrecursionlimit(10000)


def solve(part=1, elements=None):
    res = 0

    matrix = elements
    h, l = len(matrix), len(matrix[0])
    print(f"h: {h}, l: {l}")

    if debug:
        print_index(matrix)

    return res


if __name__ == "__main__":
    time_and_color(start=True)
    debug = False

    assert puzzle(file("/2024/07/example.txt"), read_file, solve, 1) == 0
    # assert puzzle(file("/2024/07/input.txt"), read_file, solve, 1) == 0
    # assert puzzle(file("/2024/07/example.txt"), read_file, solve, 2) == 0
    # assert puzzle(file("/2024/07/input.txt"), read_file, solve, 2) == 0

    time_and_color(start=False)
