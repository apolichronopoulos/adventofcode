from timeit import default_timer as timer
from datetime import datetime
import numpy as np
import itertools

universe = []

max_size = 0
start = [-1, -1]


def read_file(filename, part=1):
    global start
    global max_size
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


def expand_universe():
    expand_rows = []
    for i in range(0, len(universe)):
        empty_row = True
        for j in range(0, len(universe[0])):
            c = universe[i][j]
            if c != '.':
                empty_row = False
        if empty_row:
            expand_rows.append(i)

    expand_cols = []
    for j in range(0, len(universe[0])):
        empty_col = True
        for i in range(0, len(universe)):
            c = universe[i][j]
            if c != '.':
                empty_col = False
        if empty_col:
            expand_cols.append(j)

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


def get_combinations(my_list):  # creating a user-defined method
    my_result = []
    for i in range(0, len(my_list)):
        for j in range(i, len(my_list)):
            if i != j:
                my_result.append((my_list[i], my_list[j]))
    return my_result


def solve(part=1):
    expanded_universe = expand_universe()

    print("---------------------")
    print_index(expanded_universe)
    print("---------------------")

    galaxies = []
    for i in range(0, len(expanded_universe)):
        for j in range(0, len(expanded_universe[i])):
            c = expanded_universe[i][j]
            if c == '#':
                galaxies.append([i, j])

    all_combinations = get_combinations(galaxies)  # method call

    count = 0
    res = 0
    for combination in all_combinations:
        p1 = combination[0]
        p2 = combination[1]
        min_distance = abs(p2[0] - p1[0]) + abs(p2[1] - p1[1])
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
    print_index(universe)
    solve()
    t_end = timer()
    print(f"Time elapsed (in seconds): {t_end - t_start}")


def puzzle2(filename):
    t_start = timer()
    print(f"\n\npuzzle2: {filename}")
    read_file(filename)
    solve(2)
    t_end = timer()
    print(f"Time elapsed (in seconds): {t_end - t_start}")


def print_index(index=[]):
    for i in range(0, len(index)):
        for j in range(0, len(index[i])):
            c = index[i][j]
            print(c, end=" ")
        print(""),


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Start Time =", current_time)
    # puzzle1('../puzzles/2023/11/example.txt')  # result -> 374
    puzzle1('../puzzles/2023/11/input.txt')  # result -> 9957702
    # puzzle2('../puzzles/2023/11/example.txt', 1)  # result -> should be 374
    # puzzle2('../puzzles/2023/11/example.txt', 1000)  # result -> should be 1030
    # puzzle2('../puzzles/2023/11/input.txt', 1000000)  # result -> ?
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("End Time =", current_time)
