# -*- coding: utf-8 -*-
import sys

from utils.utils import contains_only_digits, puzzle, time_and_color

print(sys.getrecursionlimit())
sys.setrecursionlimit(10000)

lines = []


def read_file(filename):
    f = open(filename, "r")
    lines.clear()
    for i, line in enumerate(f):
        line = line.strip()
        if line == "":
            continue
        # levels = line.split(" ")
        # levels = [int(i) for i in levels]
        # lines.append(levels)
        lines.append(line)


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

    for line in lines:
        items = line.split("mul")
        for item in items:
            if item and item[0] == "(":
                x2 = item.find(")")
                subtext = item[1:x2]
                numbers = subtext.split(",")
                if len(numbers) != 2:
                    continue
                n1 = numbers[0]
                n2 = numbers[1]
                if contains_only_digits(n1) and contains_only_digits(n2):
                    print(f"'{subtext}'")
                    original = f"mul({subtext})"
                    if original in line:
                        res += int(n1) * int(n2)

    return res


if __name__ == "__main__":
    time_and_color(start=True)

    # assert puzzle("../../puzzles/2024/03/example.txt", read_file, solve, 1) == 161
    assert puzzle("../../puzzles/2024/03/input.txt", read_file, solve, 1) < 166914319
    # assert puzzle("../../puzzles/2024/03/example.txt", read_file, solve, 2) == 0
    # assert puzzle("../../puzzles/2024/03/input.txt", read_file, solve, 2) == 0

    time_and_color(start=False)
