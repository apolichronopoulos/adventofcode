# -*- coding: utf-8 -*-
import os
import sys
from datetime import datetime
from timeit import default_timer as timer

from colorama import Back, Fore, init
from utils.utils import add_direction, calculate_direction, print_color, print_index

print(sys.getrecursionlimit())
sys.setrecursionlimit(10000)


def cls():
    os.system("cls" if os.name == "nt" else "clear")


tiles = []
illuminated = {}


def read_file(filename, part=1):
    tiles.clear()
    f = open(filename, "r")
    for line in f:
        line = line.strip()
        if line == "":
            continue
        tiles.append(line)


def solve(part=1):
    print(f"-------- part {part} --------")
    print_index(tiles, color=Fore.CYAN, ending="")
    res = 0
    if part == 1:
        move(0, 0, 0, 1)
        print(f"-------- part 1 solution --------")
        results = []
        for i in illuminated:
            parts = i.split(",")
            results.append([int(parts[0]), int(parts[1])])
        print_index(tiles, results=results, color=Fore.CYAN, ending="")

        myset = {x[:-2] for x in illuminated}  # count only uniques
        res = len(myset)
    else:
        max_res = 0
        for i in range(len(tiles)):
            for j in range(len(tiles[0])):
                if i != 0 and i != len(tiles) - 1 and j != 0 and j != len(tiles[0]) - 1:
                    continue
                for case in [
                    [i, j + 1],
                    [i, j - 1],
                    [i - 1, j],
                    [i + 1, j],
                ]:
                    illuminated.clear()
                    move(i, j, case[0], case[1])
                    r = len({x[:-2] for x in illuminated})
                    if r > max_res:
                        print(f"max res -> {max_res}")
                        max_res = r
        res = max_res

    print_color(
        f"---------> final result: {res} <---------",
        Fore.LIGHTRED_EX,
        Back.LIGHTYELLOW_EX,
    )
    return res


def move(i, j, i2, j2):
    # print("----------------")
    # print_index(tiles, counts=[[i, j], [i2, j2]], color=Fore.CYAN, ending="")

    direction = calculate_direction(i, j, i2, j2)
    start = ",".join([str(i), str(j), direction])
    if start in illuminated:
        return
    illuminated[start] = 1
    if j2 < 0 or i2 < 0 or i2 >= len(tiles) or j2 >= len(tiles[0]):
        return
    directions = next_directions(i2, j2, direction)
    for d in directions:
        move(i2, j2, d[0], d[1])


#   Upon closer inspection, the contraption appears to be a flat, two-dimensional square grid
#   containing empty space (.), mirrors (/ and \), and splitters (| and -).
def next_directions(i, j, direction):
    directions = []
    c = tiles[i][j]

    d = add_direction(i, j, direction)
    if c == ".":
        directions.append(d)
    elif c == "-" and direction in ["L", "R"]:
        directions.append(d)
    elif c == "-" and direction == "U":
        directions.append([i, j - 1])
        directions.append([i, j + 1])
    elif c == "-" and direction == "D":
        directions.append([i, j - 1])
        directions.append([i, j + 1])
    elif c == "|" and direction in ["U", "D"]:
        directions.append(d)
    elif c == "|" and direction in ["L", "R"]:
        directions.append([i - 1, j])
        directions.append([i + 1, j])
    elif c == "/" and direction == "L":
        directions.append([i + 1, j])
    elif c == "/" and direction == "R":
        directions.append([i - 1, j])
    elif c == "/" and direction == "D":
        directions.append([i, j - 1])
    elif c == "/" and direction == "U":
        directions.append([i, j + 1])
    elif c == "\\" and direction == "L":
        directions.append([i - 1, j])
    elif c == "\\" and direction == "R":
        directions.append([i + 1, j])
    elif c == "\\" and direction == "D":
        directions.append([i, j + 1])
    elif c == "\\" and direction == "U":
        directions.append([i, j - 1])

    return directions


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
if __name__ == "__main__":
    init()
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print_color(f"Start Time = {current_time}", Fore.YELLOW)

    # puzzle1('../../puzzles/2023/16/example.txt')  # result -> 46
    # puzzle1('../../puzzles/2023/16/input.txt')  # result -> 7046
    # puzzle2('../../puzzles/2023/16/example.txt')  # result -> 51
    puzzle2("../../puzzles/2023/16/input.txt")  # result -> 7313

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print_color(f"End Time = {current_time}", Fore.YELLOW)
