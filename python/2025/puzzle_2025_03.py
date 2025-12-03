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

        size = 2 if part == 1 else 12
        position = 0
        total = ""

        for remaining in range(size, 0, -1):
            x, i = find_max(bank, position, remaining)

            total += str(x)
            position = i + 1

        if debug:
            print(f"total: {total}")

        res += int(total)

    return res


def find_max(bank, position, remaining):
    x, i = -1, -1
    for n in range(position, len(bank) - remaining + 1):
        if bank[n] > x:
            x, i = bank[n], n
    return x, i


if __name__ == "__main__":
    time_and_color(start=True)
    submit = False  # be careful
    debug = False

    assert puzzle(file("/2025/03/example.txt"), read_file, solve, 1) == 357
    answer1 = puzzle(file("/2025/03/input.txt"), read_file, solve, 1)
    assert answer1 == 17412

    if submit:
        aoc_submit("2025", "03", 1, answer1)

    assert puzzle(file("/2025/03/example.txt"), read_file, solve, 2) == 3121910778619

    answer2 = puzzle(file("/2025/03/input.txt"), read_file, solve, 2)
    assert answer2 == 172681562473501

    if submit:
        aoc_submit("2025", "03", 2, answer2)

    time_and_color(start=False)
