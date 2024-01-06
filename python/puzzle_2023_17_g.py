import os
import sys
from datetime import datetime
from timeit import default_timer as timer

import networkx as nx
from colorama import Fore, Back, init

from utils.utils import print_index, print_color, calculate_direction

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


def solve(part=1):
    print_index(tiles, color=Fore.CYAN, ending="")
    rows, cols = len(tiles), len(tiles[0])

    if part == 1:
        start = [0, 0]
        end = [rows - 1, cols - 1]

        source = f'{start[0]},{start[1]}'
        target = f'{end[0]},{end[1]}'

        G = nx.Graph()
        for x in range(rows):
            for y in range(cols):
                key = f"{x},{y}"

                xv_plus = 0
                xv_minus = 0
                yv_plus = 0
                yv_minus = 0
                for i in range(1, 4):
                    x2 = x + i
                    if 0 < x2 < rows:
                        xv_plus += int(tiles[x2][y])
                        G.add_edge(key, f"{x2},{y}", weight=xv_plus)
                    x2 = x - i
                    if 0 < x2 < rows:
                        xv_minus += int(tiles[x2][y])
                        G.add_edge(key, f"{x2},{y}", weight=xv_minus)
                    y2 = y + i
                    if 0 < y2 < cols:
                        yv_plus += int(tiles[x][y2])
                        G.add_edge(key, f"{x},{y2}", weight=yv_plus)
                    y2 = y - i
                    if 0 < y2 < cols:
                        yv_minus += int(tiles[x][y2])
                        G.add_edge(key, f"{x},{y2}", weight=yv_minus)

        # paths = nx.all_shortest_paths(G, source=source, target=target, weight='weight', method='dijkstra')
        # paths = nx.all_shortest_paths(G, source=source, target=target, weight=wfunction, method='dijkstra')
        path = nx.shortest_path(G, source=source, target=target, weight='weight', method='dijkstra')

        # min_heat = sys.maxsize
        final_path = []
        # for path in paths:
        pathmap = []
        for i, node in enumerate(path):
            x, y = node.split(',')
            x, y = int(x), int(y)
            if i > 0:
                x2, y2 = path[i - 1].split(',')
                x2, y2 = int(x2), int(y2)
                if x2 != x:
                    for x3 in range(min(x, x2) + 1, max(x, x2)):
                        pathmap.append([x3, y])
                elif y2 != y:
                    for y3 in range(min(y, y2) + 1, max(y, y2)):
                        pathmap.append([x, y3])
            pathmap.append([x, y])

        # heat_loss = calculate_heat_loss(pathmap)
        # if heat_loss > min_heat:
        #     continue
        # final_paths.append(pathmap)

        final_path = pathmap

        # if heat_loss < min_heat:
        #     final_path = pathmap
        #     print(f'path length {len(path)}')
        #     print(f'min heat {heat_loss}')
        # print_index(tiles, pathmap)



    else:
        #  todo
        max_res = 0
        res = max_res

    # res = min_heat
    res = calculate_heat_loss(final_path)

    print_index(tiles, final_path)
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


def find_cases(x, y, previous_x=-1, previous_y=-1, path=[]):
    all_cases = []

    direction_counters = {'R': 0, 'D': 0, 'L': 0, 'U': 0}
    last_n = len(path) - 1
    check_counter = 3
    for n in range(last_n, last_n - check_counter, -1):
        if n - 1 < 0:
            continue
        p1 = path[n - 1]
        p2 = path[n]
        d = calculate_direction(p1[0], p1[1], p2[0], p2[1])
        direction_counters[d] = direction_counters[d] + 1

    if direction_counters['R'] < check_counter:
        all_cases.append([x, y + 1])  # go R
    if direction_counters['U'] < check_counter:
        all_cases.append([x - 1, y])  # go U
    if direction_counters['D'] < check_counter:
        all_cases.append([x + 1, y])  # go D
    if direction_counters['L'] < check_counter:
        all_cases.append([x, y - 1])  # go L

    cases = []
    # print(f'case {x}, {y}, {previous_x}, {previous_y}')

    for case in all_cases:
        if case[0] < 0 or case[1] < 0 or case[0] >= len(tiles) or case[1] >= len(tiles[0]):
            continue
        elif case[0] == previous_x and case[1] == previous_y:
            continue
        elif case in path:
            continue
        # else:
        #     find_neighbors(case)
        cases.append(case)

    return cases


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

    puzzle1('../puzzles/2023/17/example.txt')  # result -> 102
    # puzzle1('../puzzles/2023/17/input.txt')  # result ->
    # puzzle2('../puzzles/2023/17/example.txt')  # result ->
    # puzzle2('../puzzles/2023/17/input.txt')  # result ->

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print_color(f"End Time = {current_time}", Fore.YELLOW)
