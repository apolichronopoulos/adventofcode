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
tachyons = []
beams = []
start = []


def read_file(filename, part=1):
    f = open(filename, "r")
    grid.clear()
    tachyons.clear()
    beams.clear()
    start.clear()
    for i, line in enumerate(f):
        row = []
        line = line.strip()
        if line == "":
            continue
        for j, s in enumerate(line):
            row.append(s)
            if s == "^":
                tachyons.append((i, j))
            elif s == "S":
                start.append((i, j))
        grid.append(row)


def solve(part=1):
    res = 0

    if part == 1:
        if debug:
            print_index(
                grid, results=start, counts=tachyons, tuples=beams, tuple_char="|"
            )

        while len(start) > 0:

            if debug:
                print(f"--- New iteration ---")
                print_index(
                    grid, results=start, counts=tachyons, tuples=beams, tuple_char="|"
                )

            i, j = start.pop(0)

            x, y = (i + 1, j)
            while (x, y) not in tachyons:
                if x > len(grid) - 1 or (x, y) in beams:
                    break
                beams.append((x, y))
                x += 1
            if (x, y) in tachyons:
                res += 1
                for n in [-1, 1]:
                    if are_coordinates_inside_grid(x + 1, y + n, grid):
                        if (x + 1, y + n) not in beams:
                            beams.append((x + 1, y + n))
                            start.append((x + 1, y + n))

    return res


if __name__ == "__main__":
    time_and_color(start=True)
    submit, debug = custom_args().submit, custom_args().debug

    assert puzzle(file("/2025/07/example.txt"), read_file, solve, 1) == 21
    answer1 = puzzle(file("/2025/07/input.txt"), read_file, solve, 1)
    assert answer1 == 1656

    if submit:
        aoc_submit("2025", "07", 1, answer1)

    # assert puzzle(file("/2025/07/example.txt"), read_file, solve, 2) == -1
    #
    # answer2 = puzzle(file("/2025/07/input.txt"), read_file, solve, 2)
    # assert answer2 == -1
    #
    # if submit:
    #     aoc_submit("2025", "07", 2, answer2)

    time_and_color(start=False)
