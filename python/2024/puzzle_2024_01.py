# -*- coding: utf-8 -*-
import sys
from timeit import default_timer as timer

from colorama import Back, Fore
from utils.utils import print_color, time_and_color

print(sys.getrecursionlimit())
sys.setrecursionlimit(10000)


def read_file(filename, part=1):
    f = open(filename, "r")
    list_a = []
    list_b = []
    for i, line in enumerate(f):
        line = line.strip()
        if line == "":
            continue
        first, second = line.split("   ")
        list_a.append(int(first))
        list_b.append(int(second))

    return list_a, list_b


def solve(list_a, list_b, part2=False):
    res = 0

    if not part2:
        list_a = sorted(list_a)
        list_b = sorted(list_b)
        for i in range(len(list_a)):
            res += abs(list_a[i] - list_b[i])
    else:
        for i in list_a:
            c = list_b.count(i)
            # print(f"{i} - {c}")
            res += c * i

    print_color(
        f"---------> final result: {res} <---------",
        Fore.LIGHTRED_EX,
        Back.LIGHTYELLOW_EX,
    )
    return res


def puzzle1(filename):
    t_start = timer()
    print_color(f"puzzle1: {filename}", Fore.MAGENTA)
    list_a, list_b = read_file(filename)
    res = solve(list_a, list_b)
    t_end = timer()
    print_color(f"Time elapsed (in seconds): {t_end - t_start}", Fore.MAGENTA)
    return res


def puzzle2(filename):
    t_start = timer()
    print_color(f"puzzle1: {filename}", Fore.MAGENTA)
    list_a, list_b = read_file(filename)
    res = solve(list_a, list_b, part2=True)
    t_end = timer()
    print_color(f"Time elapsed (in seconds): {t_end - t_start}", Fore.MAGENTA)
    return res


# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    time_and_color(start=True)

    assert puzzle1("../../puzzles/2024/01/example.txt") == 11
    assert puzzle1("../../puzzles/2024/01/input.txt") == 2580760

    assert puzzle2("../../puzzles/2024/01/example.txt") == 31
    assert puzzle2("../../puzzles/2024/01/input.txt") == 25358365

    time_and_color(start=False)
