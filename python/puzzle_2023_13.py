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
            # g = "?".join(5 * [line[0]])
            temp_gears.append(line)
        temp_gears.append(line)
    if temp_gears:
        gears.append(temp_gears)


def solve():
    # print_index(gears, "\n")
    res = 0
    for c, case in enumerate(gears):
        res_rows = check_symmetric_in_rows(array(case))
        res_cols = check_symmetric_in_cols(array(case))
        print(f"---------> res_cols: {res_cols} <---------")
        print(f"---------> res_rows: {res_rows} <---------")
        res += ((res_rows * 100) + res_cols)
    print(f"---------> final result: {res} <---------")
    return res


def check_symmetric_in_rows(rows):
    size = len(rows) // 2
    odd = len(rows) % 2 == 1
    if odd:
        c1 = check_symmetric_in_rows(array(rows[:-1]))
        c2 = check_symmetric_in_rows(array(rows[1:]))
        return c1 + (c2 + 1 if c2 else 0)
    else:
        for i in range(0, size):
            s1 = i
            s2 = len(rows) - i - 1
            if rows[s1] != rows[s2]:
                return 0
        return size


def check_symmetric_in_cols(rows):
    print(f"-------------")
    num_cols = len(rows[0])

    cols = num_cols * ['']
    for i, row in enumerate(rows):
        for j, c in enumerate(row):
            cols[j] += c

    print_index(cols)
    return check_symmetric_in_rows(cols)


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
    puzzle1('../puzzles/2023/13/example2.txt')  # result -> 700?
    # puzzle1('../puzzles/2023/13/input.txt')  # result -> 716 is not correct
    # puzzle1('../puzzles/2023/13/input.txt')  # result -> 2849 That's not the right answer; your answer is too low.
    # puzzle2('../puzzles/2023/13/example.txt')  # result -> result 6
    # puzzle2('../puzzles/2023/13/input.txt')  # result -> 4546215031609 but won't run // sigkill error

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("End Time =", current_time)
