# -*- coding: utf-8 -*-
import os
import sys
from collections import deque
from datetime import datetime
from timeit import default_timer as timer

import networkx as nx
from colorama import Back, Fore, init
from utils.utils import print_color, print_index

print(sys.getrecursionlimit())
sys.setrecursionlimit(10000)


def cls():
    os.system("cls" if os.name == "nt" else "clear")


tiles = []


def read_file(filename, part=1):
    tiles.clear()
    f = open(filename, "r")
    for line in f:
        line = line.strip()
        if line == "":
            continue
        tiles.append(line)


def add_edges(G, x1, y1, x2, y2, rows, cols, visited, target, n_min=1, n_max=4):
    edges = []
    key1 = f"{x1},{y1},{x2},{y2}"

    # dx = x2 - x1
    # dy = y2 - y1
    # k = dx if dx != 0 else dy
    # if any(f'{x1 + k_ * dx},{y1 + k_ + dy},{x2},{y2}' in visited for k_ in range(0, k)):
    #     return edges
    # if any(f'{x1 - k_ * dx},{y1 - k_ * dy},{x2},{y2}' in visited for k_ in range(0, k - 1, - 1)):
    #     return edges
    if key1 in visited:
        return edges
    visited.add(key1)

    vertical = x1 == x2
    if 0 <= x2 < rows and 0 <= y2 < cols:
        temp_c = 0
        for j in range(n_min, n_max):
            x3 = x2 + j if vertical else x2
            y3 = y2 + j if not vertical else y2
            if 0 <= x3 < rows and 0 <= y3 < cols:
                key2 = f"{x2},{y2},{x3},{y3}"
                temp_c += int(tiles[x3][y3])
                G.add_edge(key1, key2, weight=temp_c)
                if key2.endswith(target):
                    G.add_edge(key2, target, weight=temp_c)
                else:
                    edges.append([x2, y2, x3, y3])
        temp_c = 0
        for j in range(n_min, n_max):
            x3 = x2 - j if vertical else x2
            y3 = y2 - j if not vertical else y2
            if 0 <= x3 < rows and 0 <= y3 < cols:
                key2 = f"{x2},{y2},{x3},{y3}"
                temp_c += int(tiles[x3][y3])
                G.add_edge(key1, key2, weight=temp_c)
                if key2.endswith(target):
                    G.add_edge(key2, target, weight=temp_c)
                else:
                    edges.append([x2, y2, x3, y3])
    return edges


def solve(part=1):
    print_index(tiles, color=Fore.CYAN, ending="")
    rows, cols = len(tiles), len(tiles[0])

    if part == 1:
        start = [0, 0]
        end = [rows - 1, cols - 1]
        source = f"{start[0]},{start[1]}"
        target = f"{end[0]},{end[1]}"

        G = nx.DiGraph()
        G.add_node(source)
        G.add_node(target)

        edges = deque()
        x, y = start
        counters = [0, 0, 0, 0]
        for i in range(1, 4):
            for c, node in enumerate([[x + i, y], [x - i, y], [x, y + i], [x, y - i]]):
                x2, y2 = node
                if 0 <= x2 < rows and 0 <= y2 < rows:
                    edges.append([x, y, x2, y2])
                    counters[c] += int(tiles[x2][y2])
                    G.add_edge(source, f"{x},{y},{x2},{y2}", weight=counters[c])

        visited = set()
        while edges:
            x1, y1, x2, y2 = edges.popleft()
            e2 = add_edges(G, x1, y1, x2, y2, rows, cols, visited, target)
            edges.extend(e2)

        path = nx.shortest_path(
            G, source=source, target=target, weight="weight", method="dijkstra"
        )

        print(f"path -> {path}")
        pathmap = []
        for i, node in enumerate(path):
            if len(node.split(",")) < 4:
                x, y = node.split(",")
                x, y = int(x), int(y)
                if [x, y] not in pathmap:
                    pathmap.append([x, y])
                continue
            x, y, x2, y2 = node.split(",")
            x, y, x2, y2 = int(x), int(y), int(x2), int(y2)
            if [x, y] not in pathmap:
                pathmap.append([x, y])
            if x2 != x:
                for x3 in range(min(x, x2), max(x, x2) + 1):
                    if [x3, y] not in pathmap:
                        pathmap.append([x3, y])
            elif y2 != y:
                for y3 in range(min(y, y2), max(y, y2) + 1):
                    if [x, y3] not in pathmap:
                        pathmap.append([x, y3])
        final_path = pathmap

    else:
        start = [0, 0]
        end = [rows - 1, cols - 1]
        source = f"{start[0]},{start[1]}"
        target = f"{end[0]},{end[1]}"

        G = nx.DiGraph()
        G.add_node(source)
        G.add_node(target)

        edges = deque()
        x, y = start
        counters = [0, 0, 0, 0]
        for i in range(4, 11):
            for c, node in enumerate([[x + i, y], [x - i, y], [x, y + i], [x, y - i]]):
                x2, y2 = node
                if 0 <= x2 < rows and 0 <= y2 < rows:
                    edges.append([x, y, x2, y2])
                    counters[c] += int(tiles[x2][y2])
                    G.add_edge(source, f"{x},{y},{x2},{y2}", weight=counters[c])

        visited = set()
        while edges:
            x1, y1, x2, y2 = edges.popleft()
            e2 = add_edges(G, x1, y1, x2, y2, rows, cols, visited, target, 4, 11)
            edges.extend(e2)

        path = nx.shortest_path(
            G, source=source, target=target, weight="weight", method="dijkstra"
        )

        print(f"path -> {path}")
        pathmap = []
        for i, node in enumerate(path):
            if len(node.split(",")) < 4:
                x, y = node.split(",")
                x, y = int(x), int(y)
                if [x, y] not in pathmap:
                    pathmap.append([x, y])
                continue
            x, y, x2, y2 = node.split(",")
            x, y, x2, y2 = int(x), int(y), int(x2), int(y2)
            if [x, y] not in pathmap:
                pathmap.append([x, y])
            if x2 != x:
                for x3 in range(min(x, x2), max(x, x2) + 1):
                    if [x3, y] not in pathmap:
                        pathmap.append([x3, y])
            elif y2 != y:
                for y3 in range(min(y, y2), max(y, y2) + 1):
                    if [x, y3] not in pathmap:
                        pathmap.append([x, y3])
        final_path = pathmap

    res = calculate_heat_loss(final_path)
    print_index(tiles, final_path, ending="")
    print(final_path)
    print_color(
        f"---------> final result: {res} <---------",
        Fore.LIGHTRED_EX,
        Back.LIGHTYELLOW_EX,
    )
    print_color(
        f"---------> final result: {final_path} <---------",
        Fore.LIGHTRED_EX,
        Back.LIGHTYELLOW_EX,
    )

    return res


def calculate_heat_loss(path):
    heat_loss = 0
    for i, p in enumerate(path):
        if i == 0:
            continue
        heat_loss += int(tiles[p[0]][p[1]])
    return heat_loss


def puzzle1(filename):
    t_start = timer()
    print_color(f"puzzle1: {filename}", Fore.MAGENTA)
    read_file(filename)
    res = solve()
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


# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    init()
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print_color(f"Start Time = {current_time}", Fore.YELLOW)

    # assert puzzle1('../../puzzles/2023/17/example.txt') == 102  # result -> 102
    # puzzle1('../../puzzles/2023/17/input.txt')  # result -> 884 too high
    # puzzle1('../../puzzles/2023/17/input.txt')  # result -> 637 too high ?
    # puzzle1('../../puzzles/2023/17/input.txt')  # result -> 636 too high ?
    # assert puzzle1('../../puzzles/2023/17/input.txt') == 635  # result -> 635 correct

    # assert puzzle2('../../puzzles/2023/17/example.txt') == 94
    # assert puzzle2('../../puzzles/2023/17/example2.txt') == 71
    puzzle2("../../puzzles/2023/17/input.txt")  # result -> 1104 too high

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print_color(f"End Time = {current_time}", Fore.YELLOW)
