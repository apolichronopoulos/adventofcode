# -*- coding: utf-8 -*-
import os
import sys
from collections import deque
from datetime import datetime
from timeit import default_timer as timer

from colorama import Back, Fore, init
from utils.utils import print_color, print_index, time_and_color

print(sys.getrecursionlimit())
sys.setrecursionlimit(10000)


def cls():
    os.system("cls" if os.name == "nt" else "clear")


tiles = []
visited = {}
visited_len = {}


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

        paths = deque()
        heats = deque()
        paths.append([start])
        heats.append(0)

        final_path = []
        final_paths = []

        min_heat_loss = sys.maxsize
        print(f"min heat loss: {min_heat_loss}")
        while len(paths) >= 1:

            path = paths.popleft()
            heat_loss = heats.popleft()
            if heat_loss > min_heat_loss:
                continue

            # max_size = 35
            if len(path) > 1 and path[len(path) - 1] == end:
                if min_heat_loss > heat_loss:
                    final_paths.clear()
                    final_paths.append(path)
                    final_path = path
                    min_heat_loss = heat_loss
                    print(f"min heat loss: {min_heat_loss}")
                elif min_heat_loss == heat_loss:
                    final_paths.append(path)
                continue
            # elif len(path) > max_size:
            #     continue

            cases = find_cases(path)
            last_n = len(path) - 1
            x = path[last_n][0]
            y = path[last_n][1]
            p_x = path[last_n - 1][0] if last_n > 0 else -1
            p_y = path[last_n - 1][1] if last_n > 0 else -1
            key = f"{x},{y},{p_x},{p_y}"
            if key in visited:
                last_heat_loss = visited[key]
                # if last_heat_loss - heat_loss < -2:
                #     continue
                if last_heat_loss < heat_loss:
                    continue
            visited[key] = heat_loss

            for case in cases:
                path2 = []
                path2.extend(path)
                path2.append(case)
                paths.append(path2)
                heats.append(heat_loss + int(tiles[case[0]][case[1]]))
    else:
        #  todo
        max_res = 0
        res = max_res

    res = min_heat_loss
    print_index(tiles, final_path)
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


def find_cases(path=[]):
    last_n = len(path) - 1
    x = path[last_n][0]
    y = path[last_n][1]
    p_x = path[last_n - 1][0] if last_n > 0 else -1
    p_y = path[last_n - 1][1] if last_n > 0 else -1
    all_cases = []
    check_counter = 3

    counterx = 0
    for i in range(x - check_counter, x + check_counter + 1):
        if i < 0 or i > len(tiles) or [i, y] not in path:
            counterx = 0
            continue
        counterx += 1
        if counterx >= 4:
            break

    countery = 0
    for j in range(y - check_counter, y + check_counter + 1):
        if j < 0 or j > len(tiles[0]) or [x, j] not in path:
            countery = 0
            continue
        countery += 1
        if countery >= 4:
            break

    if counterx < 4:
        all_cases.append([x - 1, y])  # go U
        all_cases.append([x + 1, y])  # go D

    if countery < 4:
        all_cases.append([x, y + 1])  # go R
        all_cases.append([x, y - 1])  # go L

    cases = []
    # print(f'case {x}, {y}, {p_x}, {p_y}')

    for case in all_cases:
        if (
            case[0] < 0
            or case[1] < 0
            or case[0] >= len(tiles)
            or case[1] >= len(tiles[0])
        ):
            continue
        elif case[0] == p_x and case[1] == p_y:
            continue
        elif case in path:
            continue
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


if __name__ == "__main__":
    time_and_color(start=True)

    assert puzzle1("../../puzzles/2023/17/example.txt") == 102  # result -> 102
    # puzzle1("../../puzzles/2023/17/input.txt")  # result -> 884 too high
    # puzzle2('../../puzzles/2023/17/example.txt')  # result ->
    # puzzle2('../../puzzles/2023/17/input.txt')  # result ->

    time_and_color(start=False)
