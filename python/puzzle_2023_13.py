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
        temp_gears.append(line)
    if temp_gears:
        gears.append(temp_gears)


def solve(part=1):
    res = 0
    for c, case in enumerate(gears):
        res_rows = check_symmetric_in_rows(case)
        res_cols = check_symmetric_in_cols(case)
        res_rows0 = res_rows
        res_cols0 = res_cols
        if part == 2:
            for i in range(0, len(case)):
                if res_rows0 != res_rows or res_cols0 != res_cols:
                    break
                for j in range(0, len(case[0])):
                    if res_rows0 != res_rows or res_cols0 != res_cols:
                        break
                    case2 = case.copy()
                    new_c = '#' if case2[i][j] == '.' else '.'
                    case2[i] = replace_char(case2[i], new_c, j)
                    res_rows2 = check_symmetric_in_rows(case2)
                    res_cols2 = check_symmetric_in_cols(case2)
                    if 0 < res_rows2 != res_rows0:
                        res_rows = res_rows2
                        break  # do we want to skip the other ?
                    if 0 < res_cols2 != res_cols0:
                        res_cols = res_cols2
                        break  # do we want to skip the other ?
            if res_rows0 == res_rows:
                res_rows = 0
            if res_cols0 == res_cols:
                res_cols = 0
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
    solve(part=2)
    t_end = timer()
    print(f"Time elapsed (in seconds): {t_end - t_start}")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Start Time =", current_time)

    # puzzle1('../puzzles/2023/13/example.txt')  # result -> 405
    # puzzle1('../puzzles/2023/13/example3.txt')  # result -> 709
    # puzzle1('../puzzles/2023/13/input.txt')  # result -> 30802 correct

    puzzle2('../puzzles/2023/13/example.txt')  # result -> should be 400
    puzzle2('../puzzles/2023/13/example3.txt')  # result -> should be 1400
    # puzzle2('../puzzles/2023/13/input.txt')  # result -> 13882 That's not the right answer; your answer is too low
    # puzzle2('../puzzles/2023/13/input.txt')  # result -> 24900 wrong
    # puzzle2('../puzzles/2023/13/input.txt')  # result -> 25049 wrong
    # puzzle2('../puzzles/2023/13/input.txt')  # result -> 25079 wrong wrong wrong wrong
    puzzle2('../puzzles/2023/13/input.txt')  # result ????
    # puzzle2('../puzzles/2023/13/input.txt')  # result -> 38500 That's not the right answer; your answer is too high
    # puzzle2('../puzzles/2023/13/input.txt')  # result -> 38868 That's not the right answer; your answer is too high

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("End Time =", current_time)
