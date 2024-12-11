# -*- coding: utf-8 -*-
import sys

import numpy as np
from utils.utils import file, print_index, puzzle, time_and_color, valid_loc

sys.setrecursionlimit(20000)

BLINK_TIMES = 25


def split_numbers(numbers, blink):

    if debug:
        print(numbers)

    if blink == 0:
        return numbers

    numbers2 = []
    for n in numbers:
        num = str(n)
        if n == 0:
            numbers2.append(1)
        elif len(num) % 2 == 0:
            half = int(len(num) / 2)
            numbers2.append(int(num[:half]))
            numbers2.append(int(num[half:]))
        else:
            numbers2.append(2024 * n)

    return split_numbers(numbers2, blink - 1)


def read_file(filename, separator=" "):
    elements = []
    f = open(filename, "r")
    for line in f:
        elements_i = []
        if line == "":
            continue
        if separator == "":
            line = line.strip()
        else:
            line = line.split(separator)
        for c in line:
            elements_i.append(c)
        elements.append(elements_i)

    return elements


def solve(part=1, elements=None):
    res = 0

    matrix = np.array(elements)
    h, l = matrix.shape
    if debug:
        print(f"h{h}, l={l}")
        print_index(matrix)

    for i in range(h):
        numbers = [int(x) for x in elements[i]]
        numbers = split_numbers(numbers, BLINK_TIMES)
        res += len(numbers)

    return res


if __name__ == "__main__":
    time_and_color(start=True)
    debug = False

    # BLINK_TIMES = 1
    # assert puzzle(file("/2024/11/example.txt"), read_file, solve, 1) == 7
    # BLINK_TIMES = 6
    # assert puzzle(file("/2024/11/example2.txt"), read_file, solve, 1) == 22
    # BLINK_TIMES = 25
    # assert puzzle(file("/2024/11/input.txt"), read_file, solve, 1) == 233050
    BLINK_TIMES = 75
    assert puzzle(file("/2024/11/input.txt"), read_file, solve, 2) > 233050

    time_and_color(start=False)
