# -*- coding: utf-8 -*-
import sys
from datetime import datetime
from timeit import default_timer as timer

from colorama import Back, Fore, init
from utils.utils import print_color, print_index

print(sys.getrecursionlimit())
sys.setrecursionlimit(10000)

tiles = []
matrix = []


def read_file(filename, part=1):
    tiles.clear()
    matrix.clear()
    f = open(filename, "r")
    for i, line in enumerate(f):
        line = line.strip()
        if line == "":
            continue
        tiles.append(line)
        matrix.append([])
        for j, c in enumerate(line):
            if c == "S":
                global start
                start = (i, j, 0, 0)
            matrix[i].append(c)


def solve(part=1, steps=64):
    global start
    print_index(matrix, color=Fore.CYAN, ending="")

    res = 0
    # print_color(f"---------> final <---------", Fore.LIGHTRED_EX)
    # print_index(matrix, tuples=final_nodes, color=Fore.CYAN, ending="")

    print_color(
        f"---------> final result: {res} <---------",
        Fore.LIGHTRED_EX,
        Back.LIGHTYELLOW_EX,
    )
    return res


def puzzle1(filename):
    t_start = timer()
    print_color(f"puzzle1: {filename}", Fore.MAGENTA)
    read_file(filename)
    res = solve(part=1)
    t_end = timer()
    print_color(f"Time elapsed (in seconds): {t_end - t_start}", Fore.MAGENTA)
    return res


def puzzle2(filename):
    t_start = timer()
    print_color(f"puzzle2: {filename}", Fore.MAGENTA)
    read_file(filename, part=2)
    res = solve(part=2)
    t_end = timer()
    print(f"Time elapsed (in seconds): {t_end - t_start}")
    return res


if __name__ == "__main__":
    init()
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print_color(f"Start Time = {current_time}", Fore.YELLOW)

    assert puzzle1("../../puzzles/2023/23/example.txt") == -1
    assert puzzle1("../../puzzles/2023/23/input.txt") == -1
    assert puzzle2("../../puzzles/2023/23/example.txt") == -1
    assert puzzle2("../../puzzles/2023/23/input.txt") == -1  # won't run

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print_color(f"End Time = {current_time}", Fore.YELLOW)
