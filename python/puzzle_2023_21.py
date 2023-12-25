import sys
from datetime import datetime
from timeit import default_timer as timer

from colorama import Fore, Back, init

# from test4 import is_inside_postgis
from utils.utils import print_color

print(sys.getrecursionlimit())
sys.setrecursionlimit(10000)

tiles = []
matrix = []
start = (-1, -1)

steps = []


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
            if c == 'S':
                global start
                start = (i, j)
            matrix[i].append(c)


def find_neighbors(x, y, matrix):
    all_cases = [(x, y + 1), (x - 1, y), (x + 1, y), (x, y - 1)]
    cases = []
    for i, j in all_cases:
        if i < 0 or j < 0 or i >= len(matrix) or j >= len(matrix[0]):
            continue
        elif matrix[i][j] == '#':
            continue
        cases.append((i, j))
    return cases


def navigate(matrix, nodes, steps):
    # print(f'--------- calculating step {steps} ---------')
    # print_index(matrix, tuples=nodes, color=Fore.CYAN, ending="")
    # print('---------')
    if steps == 0:
        return nodes
    new_nodes = set()
    for i, j in nodes:
        for case in find_neighbors(i, j, matrix):
            new_nodes.add(case)
    return navigate(matrix, new_nodes, steps - 1)


def solve(part=1, steps=64):
    global start
    # print_index(matrix, color=Fore.CYAN, ending="")
    nodes = [start]
    final_nodes = navigate(matrix, nodes, steps)
    # print_color(f"---------> final <---------", Fore.LIGHTRED_EX)
    # print_index(matrix, tuples=final_nodes, color=Fore.CYAN, ending="")
    res = len(final_nodes)
    print_color(f"---------> final result: {res} <---------", Fore.LIGHTRED_EX, Back.LIGHTYELLOW_EX)
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


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    init()
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print_color(f"Start Time = {current_time}", Fore.YELLOW)

    # assert puzzle1('../puzzles/2023/21/example.txt', 6) == 16
    # assert puzzle1('../puzzles/2023/21/example.txt', 64) == 42
    # assert puzzle1('../puzzles/2023/21/input.txt', 64) == 3724

    assert puzzle2('../puzzles/2023/21/example.txt', 6) == 16
    # assert puzzle2('../puzzles/2023/21/example.txt', 10) == 50
    # assert puzzle2('../puzzles/2023/21/example.txt', 50) == 1594
    # assert puzzle2('../puzzles/2023/21/example.txt', 100) == 6536
    # assert puzzle2('../puzzles/2023/21/example.txt', 500) == 167004
    # assert puzzle2('../puzzles/2023/21/example.txt', 1000) == 668697
    # assert puzzle2('../puzzles/2023/21/example.txt', 5000) == 16733044
    # assert puzzle2('../puzzles/2023/21/input.txt', 26501365) == -1

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print_color(f"End Time = {current_time}", Fore.YELLOW)
