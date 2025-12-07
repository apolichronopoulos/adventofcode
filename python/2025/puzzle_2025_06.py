# -*- coding: utf-8 -*-
import sys

from utils.utils import aoc_submit, custom_args, file, puzzle, time_and_color

print(sys.getrecursionlimit())
sys.setrecursionlimit(10000)

columns = []


def read_file(filename, part=1):
    f = open(filename, "r")
    columns.clear()
    for i, line in enumerate(f):
        line = line.strip()
        if line == "":
            continue
        items = line.split()
        for index, item in enumerate(items):
            if len(columns) <= index:
                columns.append([])
            columns[index].append(item.strip())


def solve(part=1):
    res = 0

    if part == 1:
        for col in columns:
            operator = col[-1]
            if operator == "+":
                temp = sum(int(x) for x in col[:-1])
            elif operator == "*":
                prod = 1
                for x in col[:-1]:
                    prod *= int(x)
                temp = prod

            if debug:
                print(f"Column: {col} => {temp}")
            res += temp
    return res


if __name__ == "__main__":
    time_and_color(start=True)
    submit, debug = custom_args().submit, custom_args().debug

    assert puzzle(file("/2025/06/example.txt"), read_file, solve, 1) == 4277556
    answer1 = puzzle(file("/2025/06/input.txt"), read_file, solve, 1)
    assert answer1 == 5060053676136

    if submit:
        aoc_submit("2025", "06", 1, answer1)

    # assert puzzle(file("/2025/06/example.txt"), read_file, solve, 2) == -1
    #
    # answer2 = puzzle(file("/2025/06/input.txt"), read_file, solve, 2)
    # assert answer2 == -1
    #
    # if submit:
    #     aoc_submit("2025", "06", 2, answer2)

    time_and_color(start=False)
