# -*- coding: utf-8 -*-
import sys

from utils.utils import (
    contains_only_digits,
    puzzle,
    split_lines_in_items,
    time_and_color,
)

sys.setrecursionlimit(10000)

lines = []


def read_file(filename):
    f = open(filename, "r")
    lines.clear()
    for i, line in enumerate(f):
        line = line.strip()
        if line == "":
            continue
        lines.append(line)


def calculate_actions(line):
    res = 0
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
    return res


def solve(part=1):
    res = 0
    enabled = True

    for line in lines:
        if part == 1:
            res += calculate_actions(line)
        else:
            do = "do()"
            dont = "don't()"
            items1 = split_lines_in_items([line], dont)
            if debug:
                print("".join(items1))
                print(line)
                assert "".join(items1) == line
            items2 = split_lines_in_items(items1, do)
            for item2 in items2:
                if item2 == do:
                    enabled = True
                elif item2 == dont:
                    enabled = False
                if not enabled:
                    continue
                res += calculate_actions(item2)
    return res


if __name__ == "__main__":
    time_and_color(start=True)
    debug = False

    assert puzzle("../../puzzles/2024/03/example.txt", read_file, solve, 1) == 161
    assert puzzle("../../puzzles/2024/03/input.txt", read_file, solve, 1) == 166630675
    assert puzzle("../../puzzles/2024/03/example2.txt", read_file, solve, 2) == 48
    assert puzzle("../../puzzles/2024/03/input.txt", read_file, solve, 2) == 93465710

    time_and_color(start=False)
