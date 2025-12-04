# -*- coding: utf-8 -*-
import sys

from utils.utils import (
    aoc_submit,
    file,
    find_all_neighbors,
    print_index,
    puzzle,
    time_and_color,
)

print(sys.getrecursionlimit())
sys.setrecursionlimit(10000)

grid = []
papers = []
results = []


def read_file(filename, part=1):
    f = open(filename, "r")
    grid.clear()
    papers.clear()
    for i, line in enumerate(f):
        row = []
        line = line.strip()
        if line == "":
            continue
        for j, s in enumerate(line):
            row.append(s)
            if s == "@":
                papers.append((i, j))
        grid.append(row)


def solve(part=1):
    res = 0

    if debug:
        print(f"------------------------------")
        print_index(grid, papers)

    for i, j in papers:
        neighbors = find_all_neighbors(i, j, grid)
        count = 0

        for [x, y] in neighbors:
            if grid[x][y] == "@":
                count += 1

        if count < 4:
            res += 1
            results.append((i, j))

    if debug:
        print(f"------------------------------")
        print_index(grid, tuples=results, tuple_char="x")

    return res


if __name__ == "__main__":
    time_and_color(start=True)
    submit = False  # be careful
    debug = False

    assert puzzle(file("/2025/04/example.txt"), read_file, solve, 1) == 13
    answer1 = puzzle(file("/2025/04/input.txt"), read_file, solve, 1)
    assert answer1 < 2172
    assert answer1 == 1569

    if submit:
        aoc_submit("2025", "04", 1, answer1)

    # assert puzzle(file("/2025/04/example.txt"), read_file, solve, 2) == 43

    # answer2 = puzzle(file("/2025/04/input.txt"), read_file, solve, 2)
    # assert answer2 == 172681562473501

    # if submit:
    #     aoc_submit("2025", "04", 2, answer2)

    time_and_color(start=False)
