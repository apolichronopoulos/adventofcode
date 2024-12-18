# -*- coding: utf-8 -*-

import sys

import networkx as nx
from utils.graph_utils import grid_to_graph
from utils.utils import aoc_submit, file, print_index, puzzle, time_and_color

sys.setrecursionlimit(20000)

falling_bytes = []
fallen_bytes = []
global size
global falls


def read_file(filename, separator=","):
    f = open(filename, "r")
    falling_bytes.clear()
    fallen_bytes.clear()
    for line in f:
        line = line.strip()
        if line == "":
            continue
        x, y = line.split(separator)
        falling_bytes.append((int(x), int(y)))


def init_grid(s, empty=1):
    g = []
    for i in range(s):
        row = []
        for j in range(s):
            row.append(empty)
        g.append(row)
    return g


def solve(part=1):
    res = 0
    start = (0, 0)
    end = (size - 1, size - 1)

    if part == 1:
        grid = init_grid(size)
        fallen_bytes.extend(falling_bytes[:falls])
        if debug:
            print_index(grid, tuples=fallen_bytes, tuple_char="#")
        for i, j in fallen_bytes:
            grid[i][j] = 0
        graph = grid_to_graph(grid)
        path = nx.shortest_path(graph, source=start, target=end)
        res = len(path) - 1
    else:
        for b in range(falls, len(falling_bytes)):
            grid = init_grid(size)
            fallen_bytes.clear()
            fallen_bytes.extend(falling_bytes[:b])
            for i, j in fallen_bytes:
                grid[i][j] = 0

            graph = grid_to_graph(grid)
            try:
                path = nx.shortest_path(graph, source=start, target=end)
                if debug:
                    print(f"Found path found on {b} falls")
            except nx.NetworkXNoPath:
                x, y = fallen_bytes[-1]
                res = f"{x},{y}"
                if debug:
                    print(f"No path found on {b} falls: {res}")
                break

    return res


if __name__ == "__main__":
    time_and_color(start=True)
    debug = True
    submit = False  # be careful

    size = 7
    falls = 12
    assert puzzle(file("/2024/18/example.txt"), read_file, solve, 1) == 22
    size = 71
    falls = 1024
    answer1 = puzzle(file("/2024/18/input.txt"), read_file, solve, 1)
    assert answer1 == 296
    if submit:
        aoc_submit("2024", "18", 1, answer1)

    size = 7
    falls = 12
    assert puzzle(file("/2024/18/example.txt"), read_file, solve, 2) == "6,1"
    size = 71
    falls = 1024
    answer2 = puzzle(file("/2024/18/input.txt"), read_file, solve, 2)
    assert answer2 == "28,44"
    if submit:
        aoc_submit("2024", "18", 2, answer2)

    time_and_color(start=False)
