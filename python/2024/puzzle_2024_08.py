# -*- coding: utf-8 -*-
import sys
from functools import lru_cache
from itertools import combinations
from math import dist, hypot

import numpy as np
from utils.utils import file, print_index, puzzle, read_file, time_and_color

sys.setrecursionlimit(10000)


def check_straight(nodes):
    antennas = {}
    antinodes = set()
    for x, node in enumerate(nodes):
        if node != ".":
            a = node
            if a not in antennas:
                antennas[a] = []
            antennas[a].append(x)

    for a in antennas:
        for c in combinations(antennas[a], 2):
            print(c)
            x1, x2 = c[0], c[1]

            for x, node in enumerate(nodes):
                d1 = x1 - x
                d2 = x2 - x
                if d1 == 2 * d2 or d1 * 2 == d2:
                    antinodes.add(x)

    return antinodes


@lru_cache
def distance(i, j, x1, y1, x2, y2):
    d1_x = x1 - i
    d1_y = y1 - j
    d2_x = x2 - i
    d2_y = y2 - j
    return (d1_x == 2 * d2_x and d1_y == 2 * d2_y) or (
        2 * d1_x == d2_x and 2 * d1_y == d2_y
    )


def solve(part=1, elements=None):
    res = 0

    antinodes = set()
    antennas = {}
    matrix = np.array(elements)
    h, l = matrix.shape
    if debug:
        print(f"h{h}, l={l}")
        print_index(matrix)

    if part == 1:
        print(f"part: {part}")

        for i in range(h):
            for j in range(l):
                a = matrix[i][j]
                if a != ".":
                    if a not in antennas:
                        antennas[a] = []
                    antennas[a].append([i, j])

        for a in antennas:
            for c in combinations(antennas[a], 2):
                for i in range(h):
                    for j in range(l):
                        if distance(i, j, c[0][0], c[0][1], c[1][0], c[1][1]):
                            antinodes.add((i, j))

        if debug:
            print_index(matrix, tuples=antinodes, tuple_char="#")

        res += len(antinodes)

    else:
        print(f"part: {part}")

    return res


if __name__ == "__main__":
    time_and_color(start=True)
    debug = True

    assert puzzle(file("/2024/08/example.txt"), read_file, solve, 1) == 14
    assert puzzle(file("/2024/08/input.txt"), read_file, solve, 1) == 293
    # assert puzzle(file("/2024/08/example.txt"), read_file, solve, 2) == 0
    # assert puzzle(file("/2024/08/input.txt"), read_file, solve, 2) == 0

    time_and_color(start=False)
