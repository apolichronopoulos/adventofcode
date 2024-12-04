# -*- coding: utf-8 -*-
import sys

import numpy as np
from utils.utils import file, puzzle, read_file, time_and_color

sys.setrecursionlimit(10000)


def check_sequence(line, words):
    res = 0
    for word in words:
        res += line.count(word)
    return res


def solve(part=1, elements=None):
    res = 0

    matrix = np.array(elements)
    h, l = matrix.shape

    if part == 1:
        words = ["XMAS", "SAMX"]

        # Check horizontal
        res += sum(check_sequence("".join(matrix[i, :]), words) for i in range(h))

        # Check vertical
        res += sum(check_sequence("".join(matrix[:, j]), words) for j in range(l))

        # Diagonals (top-left to bottom-right)
        diagonals_tl_br = [
            "".join(matrix.diagonal(offset)) for offset in range(-(h - 1), l)
        ]
        res += sum(check_sequence(line, words) for line in diagonals_tl_br)

        # Diagonals (top-right to bottom-left)
        flip_matrix = np.fliplr(matrix)
        diagonals_tr_bl = [
            "".join(flip_matrix.diagonal(offset)) for offset in range(-(h - 1), l)
        ]
        res += sum(check_sequence(line, words) for line in diagonals_tr_bl)
    else:
        words = ["MAS", "SAM"]
        for i in range(0, h - 2):
            for j in range(0, l - 2):
                w1 = elements[i][j] + elements[i + 1][j + 1] + elements[i + 2][j + 2]
                w2 = elements[i + 2][j] + elements[i + 1][j + 1] + elements[i][j + 2]
                if w1 in words and w2 in words:
                    res += 1
    return res


if __name__ == "__main__":
    time_and_color(start=True)
    debug = False

    assert puzzle(file("/2024/04/example.txt"), read_file, solve, 1) == 18
    assert puzzle(file("/2024/04/input.txt"), read_file, solve, 1) == 2500
    assert puzzle(file("/2024/04/example.txt"), read_file, solve, 2) == 9
    assert puzzle(file("/2024/04/input.txt"), read_file, solve, 2) == 1933

    time_and_color(start=False)
