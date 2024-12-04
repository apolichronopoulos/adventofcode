# -*- coding: utf-8 -*-
import sys
from datetime import datetime
from timeit import default_timer as timer

import numpy as np
from colorama import Back, Fore, init


def file(filename):
    puzzle_folder = sys.argv[1] if len(sys.argv) > 1 else "../../puzzles"
    return f"{puzzle_folder}/{filename}".replace("//", "/")


def read_file(filename, separator=""):
    elements = []
    f = open(filename, "r")
    for line in f:
        elements_i = []
        if line == "":
            continue
        if separator == "":
            line = line.strip()
        else:
            line = line.split(separator)
        for c in line:
            elements_i.append(c)
        elements.append(elements_i)

    return elements


def puzzle(filename, read, solve, part=1):
    t_start = timer()
    print_color(f"puzzle{part}: {filename}", Fore.MAGENTA)
    elements = read(filename)
    if elements:
        res = solve(part, elements)
    else:
        res = solve(part)
    t_end = timer()
    print_color(f"Time elapsed (in seconds): {t_end - t_start}", Fore.MAGENTA)
    print_color(
        f"---------> final result: {res} <---------",
        Fore.LIGHTRED_EX,
        Back.LIGHTYELLOW_EX,
    )
    return res


def print_index(
    index=[], counts=[], results=[], tuples=[], ending=" ", color=Fore.RESET
):
    set_print_color(color=color)
    for i in range(0, len(index)):
        for j in range(0, len(index[i])):
            c = index[i][j]
            if (i, j) in tuples:
                print_color("O", color=Fore.RED, ending=ending)
            elif [i, j] in results:
                print_color(c, color=Fore.MAGENTA, ending=ending)
            elif [i, j] in counts:
                print_color(c, color=Fore.RED, ending=ending)
            else:
                print_color(c, color=color, ending=ending)
        print(""),
    reset_print_color()


def get_combinations(my_list):  # creating a user-defined method
    my_result = []
    for i in range(0, len(my_list)):
        for j in range(i, len(my_list)):
            if i != j:
                my_result.append((my_list[i], my_list[j]))
    return my_result


def split_into_tokens(s, token_size):
    return [s[i : i + token_size] for i in range(0, len(s), token_size)]


def replace_char(s, c, i):
    return s[:i] + c + s[i + 1 :]


def print_color(s, color=Fore.RED, background=Back.RESET, ending="\n"):
    print(color + background + s + Fore.RESET + Back.RESET, end=ending)


def set_print_color(color=Fore.RED, background=Back.RESET):
    print(color + background, end="")


def reset_print_color():
    print(Fore.RESET + Back.RESET, end="")


def flip_and_rotate_grid(grid, index=1):
    num_cols = len(grid[0])
    rotated = num_cols * [""]
    for i, row in enumerate(grid):
        for j, c in enumerate(row):
            rotated[j] += c
    grid.clear()
    grid.extend(rotated)
    if index == 0:
        return grid
    else:
        return rotate_grid(grid, index - 1)


# Clockwise rotation
def rotate_grid(grid, index=1):
    num_cols = len(grid[0])
    rotated = num_cols * [""]
    for i, row in enumerate(grid):
        for j, c in enumerate(row):
            rotated[j] = c + rotated[j]
    grid.clear()
    grid.extend(rotated)
    if index == 0:
        return grid
    else:
        return rotate_grid(grid, index - 1)


def find_neighbors(x, y, tiles):
    all_cases = [[x, y + 1], [x - 1, y], [x + 1, y], [x, y - 1]]
    cases = []
    for case in all_cases:
        if (
            case[0] < 0
            or case[1] < 0
            or case[0] >= len(tiles)
            or case[1] >= len(tiles[0])
        ):
            continue
        cases.append(case)
    return cases


def calculate_direction(i, j, i2, j2):
    if i2 > i:
        return "D"  # downwards
    elif j2 > j:
        return "R"  # rightwards
    elif i > i2:
        return "U"  # upwards
    elif j > j2:
        return "L"  # rightwards


def add_direction(i, j, direction, amount=1):
    if direction == "R":
        return [i, j + amount]
    elif direction == "D":
        return [i + amount, j]
    elif direction == "L":
        return [i, j - amount]
    elif direction == "U":
        return [i - amount, j]


def print_index_dummy(index=[]):
    print("-------------------------")
    for i in index:
        print(i)
    print("-------------------------")


def pos_to_char(pos):
    return str(chr(pos + 97)).upper()


# def compute_lcm(x, y):
#     # choose the greater number
#     if x > y:
#         greater = x
#     else:
#         greater = y
#
#     while (True):
#         if ((greater % x == 0) and (greater % y == 0)):
#             lcm = greater
#             break
#         greater += 1
#
#     return lcm


def compute_lcm(arr):
    return np.lcm.reduce(arr)


def compute_gcd(arr):
    return np.gcd.reduce(arr)


def time_and_color(start=True):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    if start:
        init()
        print_color(f"Start Time = {current_time}", Fore.YELLOW)
    else:
        print_color(f"End Time = {current_time}", Fore.YELLOW)
    return current_time


def contains_only_digits(str):
    digits = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    for c in str:
        if c not in digits:
            return False
    return True


def split_lines_in_items(lines, token):
    items = []
    for line in lines:
        if token in line:
            temp_items = line.split(token)
            if line.startswith(token):
                items.append(token)
            for i in temp_items:
                items.append(i)
                items.append(token)
            items.pop()
        else:
            items.append(line)
    if items[-1] == token:
        items.pop()
    return items
