# -*- coding: utf-8 -*-
import sys

from utils.utils import (
    aoc_submit,
    are_coordinates_inside_grid,
    custom_args,
    file,
    print_index,
    puzzle,
    time_and_color,
)

print(sys.getrecursionlimit())
sys.setrecursionlimit(10000)

grid = []


def read_file(filename, part=1):
    f = open(filename, "r")
    grid.clear()
    for i, line in enumerate(f):
        line = line.strip()
        if line == "":
            continue
        x, y, z = line.split(",")
        grid.append((int(x), int(y), int(z)))


def solve(part=1):
    res = 0

    for x, y, z in grid:
        if part == 1:
            print("X:", x, "Y:", y, "Z:", z)

    return res


if __name__ == "__main__":
    time_and_color(start=True)
    submit, debug = custom_args().submit, custom_args().debug

    assert puzzle(file("/2025/08/example.txt"), read_file, solve, 1) == -1
    # answer1 = puzzle(file("/2025/08/input.txt"), read_file, solve, 1)
    # assert answer1 == -1
    #
    # if submit:
    #     aoc_submit("2025", "08", 1, answer1)
    #
    # assert puzzle(file("/2025/08/example.txt"), read_file, solve, 2) == -1
    # answer2 = puzzle(file("/2025/08/input.txt"), read_file, solve, 2)
    # assert answer2 == -1
    #
    # if submit:
    #     aoc_submit("2025", "08", 2, answer2)

    time_and_color(start=False)
