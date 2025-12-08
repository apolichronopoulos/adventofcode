# -*- coding: utf-8 -*-
import sys

from utils.utils import (
    aoc_submit,
    custom_args,
    euclidean_distance,
    file,
    puzzle,
    time_and_color,
)

print(sys.getrecursionlimit())
sys.setrecursionlimit(10000)

grid = []
NUMBER_OF_PAIRS = 10
NUMBER_OF_GROUPS = 3


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
    res = 1

    if debug:
        for x, y, z in grid:
            print("X:", x, "Y:", y, "Z:", z)

    distances = {}
    for i, p1 in enumerate(grid):
        for j, p2 in enumerate(grid):
            if i == j or (j, i) in distances or (i, j) in distances:
                continue
            distances[(i, j)] = euclidean_distance(p1, p2)
    distances = sorted(distances.items(), key=lambda x: x[1])

    groups = []
    for d in distances[:NUMBER_OF_PAIRS]:
        # p1, p2 = grid[d[0][0]], grid[d[0][1]] # use points directly
        p1, p2 = d[0]  # use indices to avoid duplicates

        found = False
        for g in groups:
            if p1 in g or p2 in g:
                if not p1 in g:
                    g.append(p1)
                if not p2 in g:
                    g.append(p2)
                found = True
                break
        if not found:
            groups.append([p1, p2])

    groups = sorted(groups, key=lambda x: -len(x))
    if debug:
        print(f"Groups found: {len(groups)}")

    for g in groups[:NUMBER_OF_GROUPS]:
        if debug:
            print(f"Group: {g} - Size: {len(g)}")
        res *= len(g)

    return res


if __name__ == "__main__":
    time_and_color(start=True)
    submit, debug = custom_args().submit, custom_args().debug

    NUMBER_OF_PAIRS = 10 + 1
    assert puzzle(file("/2025/08/example.txt"), read_file, solve, 1) == 40

    # NUMBER_OF_PAIRS = 1000 + 100
    # answer1 = puzzle(file("/2025/08/input.txt"), read_file, solve, 1)
    # assert answer1 != 12
    # assert answer1 > 1331
    # assert answer1 == -1

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
