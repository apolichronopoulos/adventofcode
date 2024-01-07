import os
import sys
from collections import deque
from datetime import datetime
from timeit import default_timer as timer

import networkx as nx
from colorama import Fore, Back, init

from utils.utils import print_index, print_color

print(sys.getrecursionlimit())
sys.setrecursionlimit(10000)


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


tiles = []


def read_file(filename, part=1):
    tiles.clear()
    f = open(filename, "r")
    for line in f:
        line = line.strip()
        if line == "":
            continue
        tiles.append(line)


def add_edges(G, x1, y1, x2, y2, rows, cols, visited, target):
    edges = []
    key1 = f'{x1},{y1},{x2},{y2}'
    if key1 in visited:
        return edges
    visited.add(key1)
    vertical = x1 == x2
    if 0 <= x2 < rows and 0 <= y2 < cols:
        temp_c = 0
        for j in range(1, 4):
            x3 = x2 + j if vertical else x2
            y3 = y2 + j if not vertical else y2
            if 0 <= x3 < rows and 0 <= y3 < cols:
                key2 = f'{x2},{y2},{x3},{y3}'
                temp_c += int(tiles[x3][y3])
                G.add_edge(key1, key2, weight=temp_c)
                if key2.endswith(target):
                    G.add_edge(key2, target, weight=temp_c)
                else:
                    edges.append([x2, y2, x3, y3])
        temp_c = 0
        for j in range(1, 4):
            x3 = x2 - j if vertical else x2
            y3 = y2 - j if not vertical else y2
            if 0 <= x3 < rows and 0 <= y3 < cols:
                key2 = f'{x2},{y2},{x3},{y3}'
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
        source = f'{start[0]},{start[1]}'
        target = f'{end[0]},{end[1]}'

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
                    G.add_edge(source, f'{x},{y},{x2},{y2}', weight=counters[c])

        visited = set()
        while edges:
            x1, y1, x2, y2 = edges.popleft()
            e2 = add_edges(G, x1, y1, x2, y2, rows, cols, visited, target)
            edges.extend(e2)

        path = nx.shortest_path(G, source=source, target=target, weight='weight', method='dijkstra')

        print(f'path -> {path}')
        pathmap = []
        for i, node in enumerate(path):
            if len(node.split(',')) < 4:
                x, y = node.split(',')
                x, y = int(x), int(y)
                if [x, y] not in pathmap:
                    pathmap.append([x, y])
                continue
            x, y, x2, y2 = node.split(',')
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
        #  todo
        max_res = 0
        res = max_res

    # res = min_heat
    # final_path = list(set(final_path))
    res = calculate_heat_loss(final_path)
    print_index(tiles, final_path)
    print(final_path)
    print_color(f"---------> final result: {res} <---------", Fore.LIGHTRED_EX, Back.LIGHTYELLOW_EX)
    print_color(f"---------> final result: {final_path} <---------", Fore.LIGHTRED_EX, Back.LIGHTYELLOW_EX)
    return res


def move(i, j, i2, j2, path):
    print("----------------")
    print_index(tiles, counts=path, color=Fore.CYAN, ending="")


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
    solve()
    t_end = timer()
    print_color(f"Time elapsed (in seconds): {t_end - t_start}", Fore.MAGENTA)


def puzzle2(filename):
    t_start = timer()
    print_color(f"puzzle2: {filename}", Fore.MAGENTA)
    read_file(filename, part=2)
    solve(part=2)
    t_end = timer()
    print(f"Time elapsed (in seconds): {t_end - t_start}")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    init()
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print_color(f"Start Time = {current_time}", Fore.YELLOW)

    # assert puzzle1('../puzzles/2023/17/example.txt') == 102  # result -> 102
    # puzzle1('../puzzles/2023/17/input.txt')  # result -> 884 too high
    # puzzle1('../puzzles/2023/17/input.txt')  # result -> 637 too high
    assert puzzle1('../puzzles/2023/17/input.txt') == 635  # result -> 635 correct
    # puzzle2('../puzzles/2023/17/example.txt')  # result ->
    # puzzle2('../puzzles/2023/17/input.txt')  # result ->

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print_color(f"End Time = {current_time}", Fore.YELLOW)
