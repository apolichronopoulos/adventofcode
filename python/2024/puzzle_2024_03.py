# -*- coding: utf-8 -*-
import sys

from utils.utils import contains_only_digits, puzzle, time_and_color

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
    enabled = True

    for line in lines:
        if part == 1:

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
                        if debug:
                            print(f"'{subtext}'")
                        original = f"mul({subtext})"
                        if original in line:
                            res += int(n1) * int(n2)
        else:

            do = "do()"
            dont = "don't()"

            items_dont = line.split(dont)
            items1 = []
            if line.startswith(dont):
                items1.append(dont)
            for i in items_dont:
                items1.append(i)
                items1.append(dont)
            items1.pop()

            if debug:
                print("".join(items1))
                print(line)
                assert "".join(items1) == line

            items2 = []
            for item in items1:
                if do in item:
                    items_do = item.split(do)
                    if item.startswith(do):
                        items2.append(do)
                    for j in items_do:
                        items2.append(j)
                        items2.append(do)
                else:
                    items2.append(item)
            if items2[-1] == do:
                items2.pop()

            for item2 in items2:
                if item2 == do:
                    enabled = True
                elif item2 == dont:
                    enabled = False
                if not enabled:
                    continue
                items = item2.split("mul")
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
                            if debug:
                                print(f"'{subtext}'")
                            original = f"mul({subtext})"
                            if original in line:
                                res += int(n1) * int(n2)

    return res


if __name__ == "__main__":
    time_and_color(start=True)
    debug = False

    assert puzzle("../../puzzles/2024/03/example.txt", read_file, solve, 1) == 161
    assert puzzle("../../puzzles/2024/03/input.txt", read_file, solve, 1) == 166630675
    assert puzzle("../../puzzles/2024/03/example2.txt", read_file, solve, 2) == 48
    assert puzzle("../../puzzles/2024/03/input.txt", read_file, solve, 2) == 93465710

    time_and_color(start=False)
