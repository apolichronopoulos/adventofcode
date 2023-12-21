import os
import sys
from datetime import datetime
from timeit import default_timer as timer

from colorama import Fore, Back, init

from utils.utils import print_index, print_color, calculate_direction

print(sys.getrecursionlimit())
sys.setrecursionlimit(10000)


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


tiles = []
visited = {}


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
        paths = [[start]]
        final_paths = []

        min_heat_loss = 9 * cols * rows
        print(f'min heat loss: {min_heat_loss}')
        while paths:
            new_paths = []
            for i in range(len(paths) - 1, -1, -1):
                path = paths[i]
                heat_loss = calculate_heat_loss(path)
                if heat_loss > min_heat_loss:
                    continue
                if len(path) > 1 and path[len(path) - 1] == end:
                    if path in final_paths:
                        print(f"wtf my friend")
                        continue
                    final_paths.append(path)
                    if min_heat_loss > heat_loss:
                        min_heat_loss = heat_loss
                        print(f'min heat loss: {min_heat_loss}')
                    continue

                current_size = len(path)
                x = path[current_size - 1][0]
                y = path[current_size - 1][1]
                p_x = path[current_size - 2][0] if current_size > 1 else -1
                p_y = path[current_size - 2][1] if current_size > 1 else -1
                cases = find_cases(x, y, p_x, p_y, path)

                key = f"{x},{y}"
                if key in visited:
                    last_heat_loss = visited[key]
                    if last_heat_loss - heat_loss < -2:
                        continue
                visited[key] = heat_loss

                for case in cases:
                    path2 = []
                    path2.extend(path)
                    path2.append(case)
                    new_paths.append(path2)
            paths = new_paths
    else:
        #  todo
        max_res = 0
        res = max_res

    final_path = final_paths[0]
    res = calculate_heat_loss(final_paths[0])

    for i, fp in enumerate(final_paths):
        r = calculate_heat_loss(fp)
        print(f'final path {i}: {final_path}')
        print(f'final heat {i}: {r}')
        if r < res:
            res = r
            final_path = fp

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


def find_cases(x, y, previous_x, previous_y, path=[]):
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

    # puzzle1('../puzzles/2023/17/example.txt')  # result -> 102
    puzzle1('../puzzles/2023/17/input.txt')  # result ->
    # puzzle2('../puzzles/2023/17/example.txt')  # result ->
    # puzzle2('../puzzles/2023/17/input.txt')  # result ->

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print_color(f"End Time = {current_time}", Fore.YELLOW)
