# -*- coding: utf-8 -*-
import sys
from timeit import default_timer as timer

from colorama import Back, Fore
from utils.utils import print_color, time_and_color

print(sys.getrecursionlimit())
sys.setrecursionlimit(10000)

reports = []


def read_file(filename, part=1):
    f = open(filename, "r")
    reports.clear()
    for i, line in enumerate(f):
        line = line.strip()
        if line == "":
            continue
        levels = line.split(" ")
        levels = [int(i) for i in levels]
        reports.append(levels)


def check_report(report, errors=0):
    safe = True
    last = report[0]
    asc = report[0] < report[1]
    for i in range(1, len(report)):
        level = report[i]
        asc2 = last < level
        if abs(level - last) not in [1, 2, 3] or asc != asc2:
            safe = False
            if errors == 0:
                for x in range(len(report)):
                    report2 = report.copy()
                    del report2[x]
                    safe2 = check_report(report2, 1)
                    if safe2:
                        return safe2
        last = level
    return safe


def solve(part2=False):
    res = 0

    if not part2:
        for report in reports:
            safe = True
            last = report[0]
            asc = report[0] < report[1]
            for i in range(1, len(report)):
                level = report[i]
                asc2 = last < level
                if abs(level - last) not in [1, 2, 3] or asc != asc2:
                    safe = False
                    break
                last = level

            if safe:
                res += 1

    else:

        for report in reports:
            safe = check_report(report)
            if safe:
                res += 1

    print_color(
        f"---------> final result: {res} <---------",
        Fore.LIGHTRED_EX,
        Back.LIGHTYELLOW_EX,
    )
    return res


def puzzle1(filename):
    t_start = timer()
    print_color(f"puzzle1: {filename}", Fore.MAGENTA)
    read_file(filename)
    res = solve()
    t_end = timer()
    print_color(f"Time elapsed (in seconds): {t_end - t_start}", Fore.MAGENTA)
    return res


def puzzle2(filename):
    t_start = timer()
    print_color(f"puzzle1: {filename}", Fore.MAGENTA)
    read_file(filename)
    res = solve(part2=True)
    t_end = timer()
    print_color(f"Time elapsed (in seconds): {t_end - t_start}", Fore.MAGENTA)
    return res


if __name__ == "__main__":
    time_and_color(start=True)

    assert puzzle1("../../puzzles/2024/02/example.txt") == 2
    assert puzzle1("../../puzzles/2024/02/input.txt") == 299
    assert puzzle2("../../puzzles/2024/02/example.txt") == 4
    assert puzzle2("../../puzzles/2024/02/input.txt") == 364

    time_and_color(start=False)
