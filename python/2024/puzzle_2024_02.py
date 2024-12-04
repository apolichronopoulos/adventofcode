# -*- coding: utf-8 -*-
import sys

from utils.utils import file, puzzle, time_and_color

print(sys.getrecursionlimit())
sys.setrecursionlimit(10000)

reports = []


def read_file(filename):
    f = open(filename, "r")
    reports.clear()
    for i, line in enumerate(f):
        line = line.strip()
        if line == "":
            continue
        levels = line.split(" ")
        levels = [int(i) for i in levels]
        reports.append(levels)


def check_report(report, ignore_errors=True):
    safe = True
    last = report[0]
    asc = report[0] < report[1]
    for i in range(1, len(report)):
        level = report[i]
        asc2 = last < level
        if abs(level - last) not in [1, 2, 3] or asc != asc2:
            safe = False
            if ignore_errors:
                for x in range(len(report)):
                    report2 = report.copy()
                    del report2[x]
                    safe2 = check_report(report2, False)
                    if safe2:
                        return safe2
        last = level
    return safe


def solve(part=1):
    res = 0

    for report in reports:
        ignore_errors = part == 2
        safe = check_report(report, ignore_errors)
        if safe:
            res += 1

    return res


if __name__ == "__main__":
    time_and_color(start=True)

    assert puzzle(file("/2024/02/example.txt"), read_file, solve, 1) == 2
    assert puzzle(file("/2024/02/input.txt"), read_file, solve, 1) == 299

    assert puzzle(file("/2024/02/example.txt"), read_file, solve, 2) == 4
    assert puzzle(file("/2024/02/input.txt"), read_file, solve, 2) == 364

    time_and_color(start=False)
