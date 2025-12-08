# -*- coding: utf-8 -*-
import argparse
import subprocess
import sys
from datetime import datetime
from functools import lru_cache
from timeit import default_timer as timer

import numpy as np
from colorama import Back, Fore, init


def file(filename):
    puzzle_folder = custom_args().puzzles
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
    elements = read(filename, part)
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
    index=[],
    counts=[],
    results=[],
    tuples=[],
    ending=" ",
    color=Fore.RESET,
    tuple_char="0",
):
    set_print_color(color=color)
    for i in range(0, len(index)):
        for j in range(0, len(index[i])):
            c = index[i][j]
            if (i, j) in tuples or [i, j] in tuples:
                c2 = c if tuple_char == "" else tuple_char
                print_color(c2, color=Fore.CYAN, ending=ending)
            elif [i, j] in results or (i, j) in results:
                print_color(c, color=Fore.MAGENTA, ending=ending)
            elif [i, j] in counts or (i, j) in counts:
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
    print(color + background + str(s) + Fore.RESET + Back.RESET, end=ending)


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


def find_all_neighbors(x, y, tiles):
    all_cases = [
        [x, y + 1],
        [x - 1, y],
        [x + 1, y],
        [x, y - 1],
        [x + 1, y + 1],
        [x - 1, y - 1],
        [x + 1, y - 1],
        [x - 1, y + 1],
    ]
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


@lru_cache
def valid_loc(i, j, h, l):
    return 0 <= i < h and 0 <= j < l


def aoc_submit(year, day, part, answer):
    command = ["aoc", "submit", "-y", str(year), "-d", str(day), str(part), str(answer)]
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"Command ran successfully:\n{result.stdout}")
    else:
        print(f"Error: {result.stderr}")


def draw_image_from_text(text_pattern, filename, suffix=".png"):
    from PIL import Image, ImageDraw

    lines = text_pattern.strip().split("\n")
    points = []
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == "x":
                points.append((x, y))

    width = max(len(line) for line in lines)
    height = len(lines)
    scale = 10  # Scale for better

    image = Image.new("RGB", (width * scale, height * scale), "black")
    draw = ImageDraw.Draw(image)

    for x, y in points:
        draw.rectangle(
            [x * scale, y * scale, (x + 1) * scale - 1, (y + 1) * scale - 1],
            fill="white",
        )

    image.save(f"{filename}{suffix}")


def ranges_overlap(r1, r2):
    s1, e1 = r1
    s2, e2 = r2
    return (s1 <= s2 <= e1) or (s1 <= e2 <= e1) or (s2 <= s1 <= e2) or (s2 <= e1 <= e2)


def custom_args():
    parser = argparse.ArgumentParser()

    # Check if argv[1] exists and is not an option
    puzzles = "../../puzzles"
    argv = sys.argv[1:]
    if argv and not argv[0].startswith("--"):
        puzzles = argv[0]
        argv = argv[1:]

    parser.add_argument("--submit", action="store_true", help="Submit the answer")
    parser.add_argument("--debug", action="store_true", help="Enable debug output")
    args = parser.parse_args(argv)
    args.puzzles = puzzles
    return args


def are_coordinates_inside_grid(i, j, grid):
    return 0 <= i < len(grid) and 0 <= j < len(grid[0])


def euclidean_distance(p1, p2, dimensions=3):
    if dimensions == 1:
        return abs(p1[0] - p2[0])
    elif dimensions == 2:
        return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5
    elif dimensions == 3:
        return (
            (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2 + (p1[2] - p2[2]) ** 2
        ) ** 0.5

    return 0
