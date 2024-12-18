# -*- coding: utf-8 -*-
import math
import sys

import networkx as nx
import sympy as sp
from sympy import Eq, Integer, Mod, Xor
from utils.graph_utils import grid_to_graph
from utils.utils import aoc_submit, file, print_index, puzzle, time_and_color

sys.setrecursionlimit(20000)

falling_bytes = []
fallen_bytes = []
grid = []
global size
global falls


def read_file(filename, separator=","):
    f = open(filename, "r")
    falling_bytes.clear()
    fallen_bytes.clear()
    grid.clear()
    for line in f:
        line = line.strip()
        if line == "":
            continue
        x, y = line.split(separator)
        falling_bytes.append((int(x), int(y)))


def solve(part=1):
    res = 0

    grid = []
    for i in range(size):
        row = []
        for j in range(size):
            row.append(1)
        grid.append(row)

    fallen_bytes.extend(falling_bytes[:falls])
    print_index(grid, tuples=fallen_bytes, tuple_char="#")

    for i, j in fallen_bytes:
        grid[i][j] = 0

    graph = grid_to_graph(grid)
    start = (0, 0)
    end = (size - 1, size - 1)

    path = nx.shortest_path(graph, source=start, target=end)
    print("Shortest Path:", path)
    res = len(path) - 1

    return res


if __name__ == "__main__":
    time_and_color(start=True)
    debug = True
    submit = True  # be careful

    size = 7
    falls = 12
    assert puzzle(file("/2024/18/example.txt"), read_file, solve, 1) == 22
    size = 71
    falls = 1024
    answer1 = puzzle(file("/2024/18/input.txt"), read_file, solve, 1)
    assert answer1 > 22
    if submit:
        aoc_submit("2024", "18", 1, answer1)

    # assert (puzzle(file("/2024/18/example2.txt"), read_file, solve, 2) == 117440)
    # answer2 = puzzle(file("/2024/18/input.txt"), read_file, solve, 2)  # takes > 6 mins
    # assert answer2 > 1249276142
    # if submit:
    #     aoc_submit("2024", "18", 2, answer2)

    time_and_color(start=False)
