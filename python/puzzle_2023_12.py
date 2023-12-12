from functools import lru_cache

import numpy as np
import itertools
from timeit import default_timer as timer
from datetime import datetime
from functools import lru_cache

from numpy.core._multiarray_umath import array

from utils.utils import print_index, get_combinations

gears = []
gears_numbers = []


def read_file(filename):
    gears.clear()
    f = open(filename, "r")
    for line in f:
        if line == "":
            continue
        line = line.strip()
        line = line.split()
        gears.append([*line[0]])
        gears_numbers.append(line[1].split(","))


@lru_cache(maxsize=None)
def find_gears(line):
    results = []
    count = 0
    # chunks = list(filter(None, line.split(".")))
    # has_qm = "?" in line
    for i, c in enumerate(line):
        if c == '#':
            count += 1
        elif c == '?':
            return results
        elif count > 0:
            results.append(str(count))
            count = 0
    if count > 0:
        results.append(str(count))
    return results


def solve(part=1):
    print_index(gears)
    print_index(gears_numbers)

    res = 0
    for i, case in enumerate(gears_numbers):
        case_s = ",".join(case)
        print(f"{i} - {case} - {gears[i]}")
        works = []
        lines = ["".join(gears[i])]
        while lines:
            line = lines[len(lines) - 1]
            del lines[len(lines) - 1]
            if '?' in line:
                for j, c in enumerate(line):
                    if c == '?':
                        for new_c in ['.', '#']:
                            line1 = line[:j] + new_c + line[j + 1:]
                            # lines.append(line1)
                            fgs = ",".join(find_gears(line1))
                            if fgs == '' or case_s.startswith(fgs):
                                lines.append(line1)
                            # else:
                            #     print(f"ignore {line1}")
            else:
                if find_gears(line) == case:
                    # if line not in works:
                    works.append(line)
        res += len(set(works))
        print(f"---------> result: {len(set(works))} <---------")

    print(f"---------> final result: {res} <---------")
    return res


def puzzle1(filename):
    t_start = timer()
    print(f"\n\npuzzle1: {filename}")
    read_file(filename)
    solve()
    t_end = timer()
    print(f"Time elapsed (in seconds): {t_end - t_start}")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Start Time =", current_time)
    # puzzle1('../puzzles/2023/12/example.txt')  # result -> 6
    puzzle1('../puzzles/2023/12/example2.txt')  # result -> 21
    # puzzle1('../puzzles/2023/12/input.txt')  # result -> ?
    # puzzle2('../puzzles/2023/12/example.txt', 1)  # result -> should be ?
    # puzzle2('../puzzles/2023/12/example.txt', 10)  # result -> should be ?
    # puzzle2('../puzzles/2023/12/input.txt', 1000000)  # result -> ?
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("End Time =", current_time)
