# -*- coding: utf-8 -*-
from datetime import datetime
from timeit import default_timer as timer

import numpy as np
from utils.utils import time_and_color

steps = []
nodes = {}
guide = {
    "L": 0,
    "R": 1,
}


def read_file(filename, part=1):
    steps.clear()
    nodes.clear()
    f = open(filename, "r")

    index = 0
    for line in f:
        line = line.strip()
        if line == "":
            continue
        if index == 0:
            steps.extend([*line])
        else:
            x = line.split("=")
            key = x[0].strip()
            value = x[1].strip()
            value = value[1 : len(value) - 1].split(",")
            l = value[0].strip()
            r = value[1].strip()
            nodes[key] = [l, r]
        index += 1


def solve_brute_force(part=1):
    start = "AAA"
    end = "ZZZ"
    step_count = 0

    positions = [start]
    if part == 2:
        start = "A"
        end = "Z"
        positions.clear()
        for node in nodes:
            if node.endswith("A"):
                positions.append(node)

    iterations = 0
    finished = False
    while not finished:
        iterations += 1

        for step in steps:
            if finished:
                break
            g = guide[step]
            step_count += 1

            z = 0
            for i in range(0, len(positions)):
                positions[i] = (nodes[positions[i]])[g]
                if positions[i].endswith(end):
                    z += 1

            if z == len(positions):
                finished = True
                break

    res = step_count
    print(f"res: {res}")


def solve_smart(part=1):
    start = "AAA"
    end = "ZZZ"

    positions = [start]
    if part == 2:
        start = "A"
        end = "Z"
        positions.clear()
        for node in nodes:
            if node.endswith("A"):
                positions.append(node)

    final_nodes_all = []

    for i in range(0, len(positions)):

        current_node = positions[i]

        step_i = 0
        final_nodes = {}
        visited = {}
        looped = False

        while True:
            if looped:
                break
            for step in steps:
                path = guide[step]

                visit = f"{current_node}_{step}_{step_i % len(steps)}"
                if visit in visited:
                    looped = True
                    break
                else:
                    visited[visit] = step_i

                if current_node.endswith(end):
                    final_nodes[current_node] = step_i

                current_node = (nodes[current_node])[path]
                step_i += 1

        print(f"finished {i} path")
        final_nodes_all.append(final_nodes)

    fn = []
    for i in range(0, len(final_nodes_all)):
        final_node_steps = final_nodes_all[i].popitem()[1]
        fn.append(final_node_steps)

    print(f"fn: {fn}")

    arr = np.array(fn)
    x = np.lcm.reduce(arr)
    print(x)


def puzzle1(filename):
    start = timer()
    print(f"\n\npuzzle1: {filename}")
    read_file(filename)
    solve_brute_force()
    end = timer()
    print(f"Time elapsed (in seconds): {end - start}")


def puzzle2(filename, brute=True):
    start = timer()
    print(f"\n\npuzzle2: {filename}")
    read_file(filename, 2)
    if brute:
        solve_brute_force(2)
    else:
        solve_smart(2)
    end = timer()
    print(f"Time elapsed (in seconds): {end - start}")


# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    time_and_color(start=True)

    # puzzle1('../../puzzles/2023/08/example.txt')  # result -> 6
    # puzzle1('../../puzzles/2023/08/input.txt')  # result -> 19637
    # puzzle2('../../puzzles/2023/08/example2.txt')  # result -> 6
    # puzzle2('../../puzzles/2023/08/example2.txt', False)  # result -> 6
    puzzle2("../../puzzles/2023/08/input.txt", False)  # result -> 8811050362409

    time_and_color(start=False)
