# -*- coding: utf-8 -*-
import sys

from utils.utils import (
    aoc_submit,
    calculate_area,
    custom_args,
    euclidean_distance,
    file,
    puzzle,
    time_and_color,
)

print(sys.getrecursionlimit())
sys.setrecursionlimit(10000)

grid = []
reds = []


def read_file(filename, part=1):
    f = open(filename, "r")
    grid.clear()
    reds.clear()
    for i, line in enumerate(f):
        line = line.strip()
        if line == "":
            continue
        x, y = line.split(",")
        reds.append((int(x), int(y)))


def solve(part=1):
    res = 0

    sizes = {}
    for r1 in reds:
        for r2 in reds:
            if r1 == r2:
                continue

            sizes[(r1, r2)] = calculate_area(r1, r2)

    sizes = sorted(sizes.items(), key=lambda x: -x[1])
    res += sizes[0][1]

    return res


if __name__ == "__main__":
    time_and_color(start=True)
    submit, debug = custom_args().submit, custom_args().debug

    assert puzzle(file("/2025/09/example.txt"), read_file, solve, 1) == 50
    answer1 = puzzle(file("/2025/09/input.txt"), read_file, solve, 1)
    assert answer1 == 4777409595

    if submit:
        aoc_submit("2025", "09", 1, answer1)

    # assert puzzle(file("/2025/09/example.txt"), read_file, solve, 2) == -1
    # answer2 = puzzle(file("/2025/09/input.txt"), read_file, solve, 2)
    # assert answer2 == -1
    #
    # if submit:
    #     aoc_submit("2025", "09", 2, answer2)

    time_and_color(start=False)
