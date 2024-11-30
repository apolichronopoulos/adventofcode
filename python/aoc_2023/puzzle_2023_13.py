from datetime import datetime
from timeit import default_timer as timer

from colorama import Fore, Back
from numpy import *

from utils.utils import print_index, replace_char, print_color

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


def printx(case, res_rows, res_cols, changed=[]):
    counts, results = [], []
    results.append(changed)
    if res_rows:
        for j in range(len(case[0])):
            counts.append([res_rows - 1, j])
            counts.append([res_rows, j])
        print(f'-------------- index: res_rows {res_rows}')
        print_index(case, counts=counts, results=results)
    if res_cols:
        for i in range(len(case)):
            counts.append([i, res_cols - 1])
            counts.append([i, res_cols])
        print(f'-------------- index: res_cols {res_cols}')
        print_index(case, counts=counts, results=results)


def solve(part=1):
    res = 0
    for c, case in enumerate(gears):
        print_color(f"\n\n--- {c} - case ---\n\n")
        res_rows = check_symmetric_in_rows(case)
        res_cols = check_symmetric_in_cols(case)
        print_color(f"before", color=Fore.YELLOW)
        printx(case, res_rows, res_cols)
        if part == 2:
            #   = res_rows
            # res_cols0 = res_cols
            indexes_rows0 = find_all_indexes(case)
            indexes_cols0 = find_all_indexes(rotate_case(case))
            found_different = False
            if not indexes_rows0 and not indexes_cols0:  # TODO: not sure if this is needed
                continue
            for i in range(0, len(case)):
                if found_different:
                    break
                for j in range(0, len(case[0])):
                    if found_different:
                        break
                    case2 = case.copy()
                    new_c = '#' if case2[i][j] == '.' else '.'
                    case2[i] = replace_char(case2[i], new_c, j)
                    indexes_rows = find_all_indexes(case2)
                    indexes_cols = find_all_indexes(rotate_case(case2))

                    # res_rows = check_symmetric_in_rows(case2)
                    # res_cols = check_symmetric_in_cols(case2)
                    # res_rows = min(indexes_rows) if indexes_rows else 0
                    # res_cols = min(indexes_cols) if indexes_cols else 0

                    for x in indexes_rows:
                        # if indexes_rows0 and x not in indexes_rows0:
                        if x not in indexes_rows0:
                            res_rows = x
                            res_cols = 0
                            found_different = True
                            break
                    for x in indexes_cols:
                        # if indexes_cols0 and x not in indexes_cols0:
                        if x not in indexes_cols0:
                            res_cols = x
                            res_rows = 0
                            found_different = True
                            break
                    if found_different:
                        print_color(f"after", color=Fore.BLUE)
                        printx(case2, res_rows, res_cols, [i, j])
                        break
            if not found_different:
                res_rows = 0
                res_cols = 0
        res += ((res_rows * 100) + res_cols)
    print_color(f"---------> final result: {res} <---------", Fore.LIGHTRED_EX, Back.LIGHTYELLOW_EX)
    return res


def find_all_indexes(rows):
    indexes = []
    i = check_symmetric_in_rows(rows)
    while i != 0:
        indexes.append(i)
        i = check_symmetric_in_rows(rows, i + 1)
    return indexes


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


def rotate_case(rows):
    num_cols = len(rows[0])
    cols = num_cols * ['']
    for i, row in enumerate(rows):
        for j, c in enumerate(row):
            cols[j] += c
    return cols


def puzzle1(filename):
    t_start = timer()
    print(f"\n\npuzzle1: {filename}")
    read_file(filename)
    res = solve()
    t_end = timer()
    print(f"Time elapsed (in seconds): {t_end - t_start}")
    return res


def puzzle2(filename):
    t_start = timer()
    print(f"\n\npuzzle1: {filename}")
    read_file(filename, part=2)
    res = solve(part=2)
    t_end = timer()
    print(f"Time elapsed (in seconds): {t_end - t_start}")
    return res


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Start Time =", current_time)

    # assert puzzle1('../puzzles/2023/13/example.txt') == 405  # result -> 405
    # assert puzzle1('../puzzles/2023/13/example3.txt') == 709  # result -> 709
    # assert puzzle1('../puzzles/2023/13/input.txt') == 30802  # result -> 30802 correct

    assert puzzle2('../../puzzles/2023/13/example.txt') == 400  # result -> should be 400
    assert puzzle2('../../puzzles/2023/13/example3.txt') == 1400  # result -> should be 1400

    final_res = puzzle2('../../puzzles/2023/13/input.txt')  # result ????
    assert 13882 < final_res < 38500
    assert final_res not in (13882, 24900, 25049, 25079, 38500, 38868)  # latest 25079 not working
    assert final_res != 21647
    assert final_res == 37876

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("End Time =", current_time)
