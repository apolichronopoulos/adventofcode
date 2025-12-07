# -*- coding: utf-8 -*-
import sys

from utils.utils import aoc_submit, custom_args, file, puzzle, time_and_color

print(sys.getrecursionlimit())
sys.setrecursionlimit(10000)

columns = []
max_j = 0


def read_file(filename, part=1):
    f = open(filename, "r")
    columns.clear()
    for i, line in enumerate(f):
        line = line.strip() if part == 1 else line
        if line == "":
            continue
        items = line.split() if part == 1 else [s for s in line]
        global max_j
        if len(items) > max_j:
            max_j = len(items)
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
    else:
        temp = []
        global max_j
        for j in range(max_j - 1, -1, -1):
            num = ""
            for c in columns[j]:
                if c == "+":
                    temp.append(num)
                    num = ""
                    if debug:
                        print(f"Column: {j} => {c} with temp {temp}")
                    for n in temp:
                        res += int(n)
                    temp.clear()
                elif c == "*":
                    temp.append(num)
                    num = ""
                    if debug:
                        print(f"Column: {j} => {c} with temp {temp}")
                    prod = 1
                    for c in temp:
                        prod *= int(c)
                    res += prod
                    temp.clear()
                else:
                    num = num + str(c)
            if num.strip() != "":
                temp.append(num)

    return res


if __name__ == "__main__":
    time_and_color(start=True)
    submit, debug = custom_args().submit, custom_args().debug

    assert puzzle(file("/2025/06/example.txt"), read_file, solve, 1) == 4277556
    answer1 = puzzle(file("/2025/06/input.txt"), read_file, solve, 1)
    assert answer1 == 5060053676136

    if submit:
        aoc_submit("2025", "06", 1, answer1)

    assert puzzle(file("/2025/06/example.txt"), read_file, solve, 2) == 3263827

    answer2 = puzzle(file("/2025/06/input.txt"), read_file, solve, 2)
    assert answer2 == 9695042567249

    if submit:
        aoc_submit("2025", "06", 2, answer2)

    time_and_color(start=False)
