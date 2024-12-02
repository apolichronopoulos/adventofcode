# -*- coding: utf-8 -*-
import sys
from datetime import datetime
from functools import lru_cache
from timeit import default_timer as timer

from colorama import Back, Fore, init
from utils.utils import print_color

print(sys.getrecursionlimit())
sys.setrecursionlimit(10000)

tiles = []
matrix = []
start = (-1, -1, 0, 0)

steps = []
visited = {}


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


@lru_cache
def find_neighbors(x, y, loop_i=0, loop_j=0, part=1):
    if (x, y, loop_i, loop_j) in visited:
        return visited[(x, y, loop_i, loop_j)]
    all_cases = [(x, y + 1), (x - 1, y), (x + 1, y), (x, y - 1)]
    cases = []
    for i, j in all_cases:
        li = loop_i
        lj = loop_j
        if part == 1 and (i < 0 or j < 0 or i >= len(matrix) or j >= len(matrix[0])):
            continue
        if part == 2:
            if i < 0:
                i = len(matrix) - 1
                li -= 1
            if j < 0:
                j = len(matrix[0]) - 1
                lj -= 1
            if i >= len(matrix):
                i = 0
                li += 1
            if j >= len(matrix[0]):
                j = 0
                lj += 1
        if matrix[i][j] == "#":
            continue
        cases.append((i, j, li, lj))

    if (x, y, loop_i, loop_j) not in visited:
        visited[(x, y, loop_i, loop_j)] = cases
    return cases


# @lru_cache
def navigate(nodes, steps, part=1):
    if steps == 0:
        return nodes
    new_nodes = set()
    for i, j, loop_i, loop_j in nodes:
        for case in find_neighbors(i, j, loop_i, loop_j, part=part):
            new_nodes.add(case)
    return navigate(new_nodes, steps - 1, part)


def solve(part=1, steps=64):
    global start
    # print_index(matrix, color=Fore.CYAN, ending="")
    if part == 1:
        visited.clear()
    nodes = [start]
    final_nodes = navigate(nodes, steps, part)
    # print_index_dummy(final_nodes)

    # print_color(f"---------> final <---------", Fore.LIGHTRED_EX)
    # print_index(matrix, tuples=final_nodes, color=Fore.CYAN, ending="")
    res = len(final_nodes)
    print_color(
        f"---------> final result: {res} <---------",
        Fore.LIGHTRED_EX,
        Back.LIGHTYELLOW_EX,
    )
    return res


def puzzle1(filename, steps=64):
    t_start = timer()
    print_color(f"puzzle1: {filename}", Fore.MAGENTA)
    read_file(filename)
    res = solve(part=1, steps=steps)
    t_end = timer()
    print_color(f"Time elapsed (in seconds): {t_end - t_start}", Fore.MAGENTA)
    return res


def puzzle2(filename, steps=64):
    t_start = timer()
    print_color(f"puzzle2: {filename}", Fore.MAGENTA)
    read_file(filename, part=2)
    res = solve(part=2, steps=steps)
    t_end = timer()
    print(f"Time elapsed (in seconds): {t_end - t_start}")
    return res


if __name__ == "__main__":
    init()
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print_color(f"Start Time = {current_time}", Fore.YELLOW)

    # assert puzzle1('../../puzzles/2023/21/example.txt', 6) == 16
    # assert puzzle1('../../puzzles/2023/21/example.txt', 64) == 42
    # assert puzzle1('../../puzzles/2023/21/input.txt', 64) == 3724

    assert puzzle2("../../puzzles/2023/21/example.txt", 6) == 16
    assert puzzle2("../../puzzles/2023/21/example.txt", 10) == 50
    assert puzzle2("../../puzzles/2023/21/example.txt", 50) == 1594
    assert puzzle2("../../puzzles/2023/21/example.txt", 100) == 6536
    assert puzzle2("../../puzzles/2023/21/example.txt", 500) == 167004
    # assert puzzle2('../../puzzles/2023/21/example.txt', 1000) == 668697  # won't run
    # assert puzzle2('../../puzzles/2023/21/example.txt', 5000) == 16733044  # won't run
    # assert puzzle2('../../puzzles/2023/21/input.txt', 26501365) == -1  # won't run

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print_color(f"End Time = {current_time}", Fore.YELLOW)
