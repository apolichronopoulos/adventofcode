# -*- coding: utf-8 -*-
import sys
from timeit import default_timer as timer

from colorama import Back, Fore
from utils.utils import print_color, puzzle, time_and_color

print(sys.getrecursionlimit())
sys.setrecursionlimit(10000)

list_a = []
list_b = []


def read_file(filename, part=1):
    f = open(filename, "r")
    list_a.clear()
    list_b.clear()
    for i, line in enumerate(f):
        line = line.strip()
        if line == "":
            continue
        first, second = line.split("   ")
        list_a.append(int(first))
        list_b.append(int(second))


def solve(part=1):
    res = 0

    if part == 1:
        list_a_sorted = sorted(list_a)
        list_b_sorted = sorted(list_b)
        for i in range(len(list_a_sorted)):
            res += abs(list_a_sorted[i] - list_b_sorted[i])
    else:
        for i in list_a:
            c = list_b.count(i)
            res += c * i

    return res


if __name__ == "__main__":
    time_and_color(start=True)

    assert puzzle("../../puzzles/2024/01/example.txt", read_file, solve, 1) == 11
    assert puzzle("../../puzzles/2024/01/input.txt", read_file, solve, 1) == 2580760

    assert puzzle("../../puzzles/2024/01/example.txt", read_file, solve, 2) == 31
    assert puzzle("../../puzzles/2024/01/input.txt", read_file, solve, 2) == 25358365

    time_and_color(start=False)
