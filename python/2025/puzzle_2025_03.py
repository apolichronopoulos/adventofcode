# -*- coding: utf-8 -*-
import sys

from utils.utils import aoc_submit, file, puzzle, time_and_color

print(sys.getrecursionlimit())
sys.setrecursionlimit(10000)

batteries = []


def read_file(filename, part=1):
    f = open(filename, "r")
    batteries.clear()
    for i, line in enumerate(f):
        bank = []
        line = line.strip()
        if line == "":
            continue
        for s in line:
            bank.append(int(s))
        batteries.append(bank)


def solve(part=1):
    res = 0
    for i in range(len(batteries)):
        bank = batteries[i]
        if debug:
            print(f"bank: {bank}")
        if part == 1:
            max1, max1_i = -1, -1
            for n in range(len(bank) - 1):
                if bank[n] > max1:
                    max1, max1_i = bank[n], n

            max2, max2_i = -1, -1
            for n in range(max1_i + 1, len(bank)):
                if bank[n] > max2:
                    max2, max2_i = bank[n], n

            if debug:
                print(f"max1: {max1}, max2: {max2}")
            res += int(str(max1) + str(max2))

    return res


if __name__ == "__main__":
    time_and_color(start=True)
    submit = True  # be careful
    debug = True

    assert puzzle(file("/2025/03/example.txt"), read_file, solve, 1) == 357
    answer1 = puzzle(file("/2025/03/input.txt"), read_file, solve, 1)
    assert answer1 == 17412

    if submit:
        aoc_submit("2025", "03", 1, answer1)

    # if debug:
    #     test_split_text()

    # assert puzzle(file("/2025/03/example.txt"), read_file, solve, 2) == -1

    # answer2 = puzzle(file("/2025/03/input.txt"), read_file, solve, 2)
    # assert answer2 == -1

    # if submit:
    #     aoc_submit("2025", "03", 2, answer2)

    time_and_color(start=False)
