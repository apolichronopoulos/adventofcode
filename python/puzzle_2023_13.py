from datetime import datetime
from functools import lru_cache
from timeit import default_timer as timer

from utils.utils import print_index, split_into_tokens, replace_char

from numpy import *

gears = []

global_case = ""
global_combinations = []


def read_file(filename, part=1):
    gears.clear()
    f = open(filename, "r")
    temp_gears = []
    for line in f:
        line = line.strip()
        if line == "":
            gears.append(temp_gears)
            temp_gears = []
            continue
        if part == 2:
            temp_gears.append(line)
        temp_gears.append(line)
    if temp_gears:
        gears.append(temp_gears)


def solve():
    res = 0
    for c, case in enumerate(gears):
        print(f"{c} case")
        res_rows = check_symmetric_in_rows(case)
        res_cols = check_symmetric_in_cols(case)
        if res_rows:
            print(f"---------> res_rows: {res_rows} <---------")
        if res_cols:
            print(f"---------> res_cols: {res_cols} <---------")
        res += ((res_rows * 100) + res_cols)
    print(f"---------> final result: {res} <---------")
    return res


def check_symmetric_in_rows(rows, index=1):
    if len(rows) // 2 < 1 or index > len(rows) - 1:
        return 0
    start = max(0, 2 * index - len(rows))
    for i in range(start, index):
        s1 = i
        s2 = 2 * index - s1 - 1
        r1 = rows[s1]
        r2 = rows[s2]
        if r1 != r2:
            return check_symmetric_in_rows(rows, index + 1)
    return index


def check_symmetric_in_cols(rows, index=1):
    num_cols = len(rows[0])

    cols = num_cols * ['']
    for i, row in enumerate(rows):
        for j, c in enumerate(row):
            cols[j] += c

    # print_index(cols)
    # print(f"-------------")
    return check_symmetric_in_rows(cols, index)


def puzzle1(filename):
    t_start = timer()
    print(f"\n\npuzzle1: {filename}")
    read_file(filename)
    solve()
    t_end = timer()
    print(f"Time elapsed (in seconds): {t_end - t_start}")


def puzzle2(filename):
    t_start = timer()
    print(f"\n\npuzzle1: {filename}")
    read_file(filename, part=2)
    solve()
    t_end = timer()
    print(f"Time elapsed (in seconds): {t_end - t_start}")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Start Time =", current_time)

    # puzzle1('../puzzles/2023/13/example.txt')  # result -> 405
    # puzzle1('../puzzles/2023/13/example2.txt')  # result -> 1200
    # puzzle1('../puzzles/2023/13/example3.txt')  # result -> 709
    puzzle1('../puzzles/2023/13/input.txt')  # result -> 30802 correct
    # puzzle2('../puzzles/2023/13/example.txt')  # result -> ?
    # puzzle2('../puzzles/2023/13/input.txt')  # result -> ?

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("End Time =", current_time)
