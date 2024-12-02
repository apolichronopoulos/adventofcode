# -*- coding: utf-8 -*-
from datetime import datetime
from timeit import default_timer as timer

from utils.utils import get_combinations, print_index

universe = []
expand_cols = []
expand_rows = []
expand_size = 0


def read_file(filename, part=1):
    universe.clear()
    f = open(filename, "r")
    for line in f:
        elements_i = []
        line = line.strip()
        if line == "":
            continue
        for c in line:
            elements_i.append(c)
        universe.append(elements_i)

    expand_rows.clear()
    for i in range(0, len(universe)):
        empty_row = True
        for j in range(0, len(universe[0])):
            c = universe[i][j]
            if c != ".":
                empty_row = False
        if empty_row:
            expand_rows.append(i)

    expand_cols.clear()
    for j in range(0, len(universe[0])):
        empty_col = True
        for i in range(0, len(universe)):
            c = universe[i][j]
            if c != ".":
                empty_col = False
        if empty_col:
            expand_cols.append(j)


def expand_universe():
    expanded_universe = []
    for i in range(len(universe) - 1, -1, -1):
        row = []
        for j in range(len(universe[0]) - 1, -1, -1):
            c = universe[i][j]
            if j in expand_cols:
                row.append(".")
            row.append(c)
        row.reverse()
        expanded_universe.append(row)
        if i in expand_rows:
            expanded_universe.append(row)

    # print("---------------------")
    # print_index(expanded_universe)

    expanded_universe.reverse()

    # print("---------------------")
    # print_index(expanded_universe)

    return expanded_universe


def solve(part=1):
    if part == 1:
        expanded_universe = expand_universe()
        universe.clear()
        universe.extend(expanded_universe)

    print("---------------------")
    print_index(universe)
    print("---------------------")

    galaxies = []
    for i in range(0, len(universe)):
        for j in range(0, len(universe[i])):
            c = universe[i][j]
            if c == "#":
                galaxies.append([i, j])

    all_combinations = get_combinations(galaxies)  # method call

    count = 0
    res = 0
    for combination in all_combinations:
        p1 = combination[0]
        p2 = combination[1]
        x1 = min(p1[0], p2[0])
        x2 = max(p1[0], p2[0])
        y1 = min(p1[1], p2[1])
        y2 = max(p1[1], p2[1])

        x_plus = 0
        for i in range(x1 + 1, x2):
            if i in expand_rows:
                x_plus += expand_size - 1
        y_plus = 0
        for j in range(y1 + 1, y2):
            if j in expand_cols:
                y_plus += expand_size - 1

        min_distance = abs(x2 - x1) + x_plus + abs(y2 - y1) + y_plus
        res += min_distance
        print(f"distance between {p1} and {p2} is {min_distance}")
        count += 1

    if part == 1:
        print(f"---------> result: {res} <---------")
    else:
        print(f"---------> result: {res} <---------")

    return res


def puzzle1(filename):
    t_start = timer()
    print(f"\n\npuzzle1: {filename}")
    read_file(filename)
    # print_index(universe)
    solve()
    t_end = timer()
    print(f"Time elapsed (in seconds): {t_end - t_start}")


def puzzle2(filename, expand_number=1):
    t_start = timer()
    print(f"\n\npuzzle2: {filename}")
    read_file(filename)
    global expand_size
    expand_size = expand_number
    solve(2)
    t_end = timer()
    print(f"Time elapsed (in seconds): {t_end - t_start}")


if __name__ == "__main__":
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Start Time =", current_time)
    # puzzle1('../../puzzles/2023/11/example.txt')  # result -> 374
    # puzzle1('../../puzzles/2023/11/input.txt')  # result -> 9957702
    # puzzle2('../../puzzles/2023/11/example.txt', 1)  # result -> should be 374
    # puzzle2('../../puzzles/2023/11/example.txt', 10)  # result -> should be 1030
    puzzle2("../../puzzles/2023/11/input.txt", 1000000)  # result -> 512240933238
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("End Time =", current_time)
