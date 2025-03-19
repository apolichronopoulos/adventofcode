# -*- coding: utf-8 -*-
import sys

import networkx as nx
from utils.graph_utils import pos_to_graph
from utils.utils import draw_image_from_text, file, print_index, puzzle, time_and_color

sys.setrecursionlimit(20000)

p = []
v = []


def read_file(filename, separator=","):
    p.clear()
    v.clear()
    f = open(filename, "r")
    for line in f:
        line = line.strip()
        if line == "":
            continue
        else:
            line = line.split(" ")
            p_x, p_y = line[0][2:].split(",")
            v_x, v_y = line[1][2:].split(",")
            p.append((int(p_x), int(p_y)))
            v.append((int(v_x), int(v_y)))


def solve(part=1):
    res = 0

    grid = []
    pos = []
    seconds = 100 if part == 1 else 0

    h, l = 0, 0
    for i in range(len(p)):
        p_x, p_y = p[i][0], p[i][1]
        h = max(h, p_x)
        l = max(l, p_y)

    h, l = h + 1, l + 1
    if debug:
        print(f"h={h}, l={l}")

    for i in range(h):
        row = []
        for j in range(l):
            row.append(" ")
        grid.append(row)

    if part == 1:
        for i in range(len(p)):
            p_x, p_y = p[i][0], p[i][1]
            v_x, v_y = v[i][0], v[i][1]

            x = (p_x + seconds * v_x) % h
            y = (p_y + seconds * v_y) % l
            pos.append((x, y))

        if debug:
            print_index(grid, tuples=pos)

        q = [0, 0, 0, 0]
        for x, y in pos:
            if 0 <= x < (h // 2):
                if 0 <= y < (l // 2):
                    q[0] += 1
                elif (l // 2) < y < l:
                    q[1] += 1
            elif (h // 2) < x < h:
                if 0 <= y < (l // 2):
                    q[2] += 1
                elif (l // 2) < y < l:
                    q[3] += 1

        res += q[0] * q[1] * q[2] * q[3]
    else:
        pos = set()
        for second in range(1, 8000):
            pos.clear()
            for i in range(len(p)):
                p_x, p_y = p[i][0], p[i][1]
                v_x, v_y = v[i][0], v[i][1]
                x = (p_x + second * v_x) % h
                y = (p_y + second * v_y) % l
                pos.add((x, y))

            if debug:
                print(f"---------------------------")
                print_index(grid, tuples=pos, tuple_char="*")
                print(f"---- second = {second}-----")

            text_pattern = "\n".join(
                "".join("x" if (i, j) in pos else " " for j in range(len(grid[i])))
                for i in range(len(grid))
            )

            graph = pos_to_graph(pos, False)
            clusters = list(nx.connected_components(graph))
            largest_cluster = max(clusters, key=len) if clusters else []

            if len(largest_cluster) > 100:
                if debug:
                    draw_image_from_text(text_pattern, f"img/2024_14_{second}", ".png")
                return second

    return res


if __name__ == "__main__":
    time_and_color(start=True)
    debug = False

    assert puzzle(file("/2024/14/example.txt"), read_file, solve, 1) == 12
    answer1 = puzzle(file("/2024/14/input.txt"), read_file, solve, 1)
    assert answer1 == 229980828
    # aoc_submit("2024", "14", 1, answer1)

    answer2 = puzzle(file("/2024/14/input.txt"), read_file, solve, 2)
    assert answer2 == 7132
    # aoc_submit("2024", "14", 2, answer2)

    time_and_color(start=False)
