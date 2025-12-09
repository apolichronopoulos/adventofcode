# -*- coding: utf-8 -*-
import sys

from shapely.geometry import Polygon, box
from utils.utils import (
    aoc_submit,
    calculate_area,
    custom_args,
    file,
    get_combinations,
    print_index,
    puzzle,
    time_and_color,
)

print(sys.getrecursionlimit())
sys.setrecursionlimit(10000)

grid = []
reds = []
greens = []


def read_file(filename, part=1):
    f = open(filename, "r")
    grid.clear()
    reds.clear()
    greens.clear()
    for i, line in enumerate(f):
        line = line.strip()
        if line == "":
            continue
        y, x = line.split(",")
        reds.append((int(x), int(y)))

    if debug:
        max_i = max(x for x, y in reds) + 2
        max_j = max(y for x, y in reds) + 3

        for i in range(max_i):
            row = []
            for j in range(max_j):
                row.append("#" if (i, j) in reds else ".")
            grid.append(row)


def solve(part=1):
    res = 0

    if debug:
        print_index(grid, reds)
        print("--------------------")

    if part == 1:
        res += find_max_area(reds)
    else:
        if debug:
            greens_x = set()
            greens_y = set()

            for r1, r2 in get_combinations(reds):
                x1, y1 = r1
                x2, y2 = r2
                if x1 == x2:
                    greens_x.add((x1, min(y1, y2), max(y1, y2)))
                if y1 == y2:
                    greens_y.add((y1, min(x1, x2), max(x1, x2)))

            for x, y1, y2 in greens_x:
                for y in range(y1 + 1, y2):
                    g = (x, y)
                    if g not in reds:
                        greens.append(g)
            for y, x1, x2 in greens_y:
                for x in range(x1 + 1, x2):
                    g = (x, y)
                    if g not in reds:
                        greens.append(g)

            print(f"Initialized greens: {len(greens)}")
            print_index(grid, reds, tuples=greens, tuple_char="X")
            print("--------------------")
            print(f"Running final area check")

        wall = Polygon(reds)

        res = find_max_area2(reds, wall)

    return res


def find_max_area(points, extra_points=[]):
    sizes = {}

    for p1, p2 in get_combinations(points):
        sizes[(p1, p2)] = calculate_area(p1, p2)

    sizes = sorted(sizes.items(), key=lambda x: -x[1])

    if extra_points:
        for s in sizes:
            p1, p2 = s[0]
            size = s[1]
            valid = True
            for x in range(min(p1[0], p2[0]), max(p1[0], p2[0]) + 1):
                for y in range(min(p1[1], p2[1]), max(p1[1], p2[1]) + 1):
                    if (x, y) not in extra_points:
                        valid = False
                        break
                if not valid:
                    break
            if valid:
                return size

    return sizes[0][1]


def find_max_area2(points, wall):
    sizes = {}
    for p1, p2 in get_combinations(points):
        sizes[(p1, p2)] = calculate_area(p1, p2)

    sizes = sorted(sizes.items(), key=lambda x: -x[1])
    for s in sizes:
        p1, p2 = s[0]
        size = s[1]

        rect_min_x, rect_min_y = min(p1[0], p2[0]), min(p1[1], p2[1])
        rect_max_x, rect_max_y = max(p1[0], p2[0]), max(p1[1], p2[1])
        rectangle = box(rect_min_x, rect_min_y, rect_max_x, rect_max_y)

        if rectangle.within(wall):  # True if inside or touching the boundary
            return size

    return -1


if __name__ == "__main__":
    time_and_color(start=True)
    submit, debug = custom_args().submit, custom_args().debug

    assert puzzle(file("/2025/09/example.txt"), read_file, solve, 1) == 50
    answer1 = puzzle(file("/2025/09/input.txt"), read_file, solve, 1)
    assert answer1 == 4777409595

    if submit:
        aoc_submit("2025", "09", 1, answer1)

    assert puzzle(file("/2025/09/example.txt"), read_file, solve, 2) == 24
    answer2 = puzzle(file("/2025/09/input.txt"), read_file, solve, 2)
    assert answer2 == 1473551379

    if submit:
        aoc_submit("2025", "09", 2, answer2)

    time_and_color(start=False)
