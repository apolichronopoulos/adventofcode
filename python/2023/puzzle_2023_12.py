# -*- coding: utf-8 -*-
from datetime import datetime
from functools import lru_cache
from timeit import default_timer as timer

from utils.utils import replace_char

gears = []
gears_numbers = []

global_case = ""
global_combinations = []


def read_file(filename, part=1):
    gears.clear()
    gears_numbers.clear()
    f = open(filename, "r")
    for line in f:
        if line == "":
            continue
        line = line.strip()
        line = line.split()

        if part == 2:
            g = "?".join(5 * [line[0]])
            gn = ",".join(5 * [line[1]])
        else:
            g = line[0]
            gn = line[1]

        gears.append(g)
        gears_numbers.append(gn.split(","))
        # gears_numbers.append(tuple([int(d) for d in gn.split(",")]))


@lru_cache
def find_gears(line: str):
    results = []
    chunks = list(filter(None, line.split(".")))
    for chunk in chunks:
        if "?" in chunk:
            return results
        else:
            results.append(str(len(chunk)))
    return results


def generate_combinations(s, index, current_combination, combinations, case):
    # print(''.join(current_combination))
    if index == len(s):
        combinations.append("".join(current_combination))
        return
    if s[index] == "?":
        current_combination[index] = "."
        generate_combinations(s, index + 1, current_combination, combinations, case)
        current_combination[index] = "#"
        generate_combinations(s, index + 1, current_combination, combinations, case)
        current_combination[index] = "?"  # reset for backtracking
    else:
        cc = "".join(current_combination)

        fg1 = ",".join(find_gears(cc))
        if fg1 != "" and not case.startswith(fg1):
            return

        fg2 = ",".join(find_gears(cc[::-1])[::-1])
        if fg2 != "" and not case.endswith(fg2):
            return

        chunks = list(filter(None, cc.split(".")))
        count = len(chunks)
        for chunk in chunks:
            if "?" in chunk:
                count += chunk.count("?") // 2 + chunk.count("?")
        if count < len(case.split(",")):
            return

        generate_combinations(s, index + 1, current_combination, combinations, case)


@lru_cache
def generate_combinations2(s, index, current_combination):
    global global_combinations, global_case
    if index == len(s):
        global_combinations.append(current_combination)
        return
    if s[index] == "?":
        generate_combinations2(
            s, index + 1, replace_char(current_combination, ".", index)
        )
        generate_combinations2(
            s, index + 1, replace_char(current_combination, "#", index)
        )
    else:
        fgs = ",".join(find_gears("".join(current_combination)))
        if fgs == "" or global_case.startswith(fgs):
            generate_combinations2(s, index + 1, current_combination)


def solve():

    res = 0
    for i, case in enumerate(gears_numbers):
        print(f"{i} - {gears[i]} - {case}")
        case_s = ",".join(case)
        input_string = gears[i]

        # TODO: generate_combinations
        # initial_combination = list(input_string)
        # all_combinations = []
        # generate_combinations(input_string, 0, initial_combination, all_combinations, case_s)

        # TODO: generate_combinations2
        global global_case
        global_case = case_s
        initial_combination = input_string
        global_combinations.clear()
        generate_combinations2(input_string, 0, initial_combination)
        all_combinations = global_combinations

        count = 0
        for combination in all_combinations:
            if find_gears(combination) == case:
                count += 1
        res += count
        print(f"---------> result: {count} <---------")
    print(f"---------> final result: {res} <---------")
    return res


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


if __name__ == "__main__":
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Start Time =", current_time)

    # puzzle1('../../puzzles/2023/12/example.txt')  # result -> 6
    # puzzle1('../../puzzles/2023/12/example2.txt')  # result -> 21
    puzzle1("../../puzzles/2023/12/input.txt")  # result -> 6981

    # puzzle2('../../puzzles/2023/12/example.txt')  # result -> result 6
    # puzzle2('../../puzzles/2023/12/example2.txt')  # result -> should be 525152 ??? won't run // sigkill error
    # puzzle2('../../puzzles/2023/12/input.txt')  # result -> 4546215031609 but won't run // sigkill error

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("End Time =", current_time)
