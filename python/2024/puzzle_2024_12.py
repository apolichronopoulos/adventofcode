# -*- coding: utf-8 -*-
import sys
from functools import cache

from utils.utils import file, print_index, puzzle, read_file, time_and_color, valid_loc

sys.setrecursionlimit(20000)

regions = []
found = set()
grid = []


def solve(part=1, elements=None):
    res = 0

    regions.clear()
    found.clear()
    grid.clear()
    grid.extend(elements)

    h, l = len(grid), len(grid[0])
    if debug:
        print(f"h{h}, l={l}")
        print_index(grid)

    for i in range(h):
        for j in range(l):
            if (i, j) in found:
                continue
            region = []
            check = [(i, j)]
            while len(check) > 0:
                x, y = check.pop()
                region.append((x, y))
                found.add((x, y))
                next_plots = add_next(x, y, h, l)
                check.extend(next_plots)
            regions.append([x for x in region])
            region.clear()

    for region in regions:
        plot = grid[region[0][0]][region[0][1]]
        area = len(region)
        if debug:
            print("-----------")
            print_index(
                grid, tuples=region, tuple_char=grid[region[0][0]][region[0][1]]
            )
            print("-----------")

        if part == 1:
            perimeter = calc_perimeter(region)
            score = area * perimeter
            if debug:
                print(
                    f"A region of {plot} plants with price {area} * {perimeter} = {score}"
                )
        else:
            sides = calc_sides(region)
            score = area * sides
            if debug:
                print(
                    f"A region of {plot} plants with price {area} * {sides} = {score}"
                )

        res += score

    return res


def calc_perimeter(region):
    count = 0
    for x, y in region:
        for i, j in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
            x2, y2 = x + i, y + j
            if (x2, y2) not in region:
                count += 1
    return count


def calc_sides(region):
    count = 0
    borders = []
    counts = []

    for x, y in sorted(region):
        for i, j in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            x2, y2 = x + i, y + j
            if (x2, y2) not in region:
                is_horizontal = i != 0
                borders.append((x2, y2, is_horizontal, i if is_horizontal else j))
                if i != 0:
                    if (x2, y2 - 1, True, i) in borders or (
                        x2,
                        y2 + 1,
                        True,
                        i,
                    ) in borders:
                        continue
                if j != 0:
                    if (x2 - 1, y2, False, j) in borders or (
                        x2 + 1,
                        y2,
                        False,
                        j,
                    ) in borders:
                        continue

                counts.append((x2, y2, is_horizontal, i if is_horizontal else j))
                count += 1

    return count


@cache
def add_next(x, y, h, l):
    plot = grid[x][y]
    plots = []
    for i, j in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
        x2, y2 = x + i, y + j
        if valid_loc(x2, y2, h, l):
            if grid[x2][y2] == plot and ((x2, y2) not in found):
                plots.append((x2, y2))
                found.add((x2, y2))
    return plots


if __name__ == "__main__":
    time_and_color(start=True)
    debug = False

    assert puzzle(file("/2024/12/example.txt"), read_file, solve, 1) == 140
    assert puzzle(file("/2024/12/example2.txt"), read_file, solve, 1) == 1930
    assert puzzle(file("/2024/12/input.txt"), read_file, solve, 1) == 1437300

    assert puzzle(file("/2024/12/example.txt"), read_file, solve, 2) == 80
    assert puzzle(file("/2024/12/example2.txt"), read_file, solve, 2) == 1206
    assert puzzle(file("/2024/12/input.txt"), read_file, solve, 2) == 849332

    time_and_color(start=False)
