from datetime import datetime
from functools import lru_cache
from timeit import default_timer as timer

from utils.utils import print_index, split_into_tokens, replace_char, print_color, set_print_color, \
    reset_print_color

from numpy import *

from colorama import Fore, Back, Style, init
from termcolor import colored

platform = []


def read_file(filename, part=1):
    platform.clear()
    f = open(filename, "r")
    for line in f:
        line = line.strip()
        if line == "":
            continue
        platform.append(line)


def solve(part=1):
    print_index(platform, color=Fore.CYAN)
    res = 0

    original_platform = platform.copy()
    move_north(platform)
    res = calculate_damage(platform)

    print_color(f"---------> final result: {res} <---------", Fore.LIGHTRED_EX, Back.LIGHTYELLOW_EX)
    return res


# ↑ north / ← west / → east / ↓ south
def move_north(platform, index=0):
    if index == len(platform) - 1:
        return
    for i, row in enumerate(platform):
        if i == 0:
            continue
        for j, column in enumerate(platform[i]):
            stone = platform[i][j]
            if stone == 'O':
                if platform[i - 1][j] == '.':
                    platform[i - 1] = replace_char(platform[i - 1], stone, j)
                    platform[i] = replace_char(platform[i], '.', j)
    return move_north(platform, index + 1)


def calculate_damage(platform):
    damage = 0
    for i, row in enumerate(platform):
        for j, column in enumerate(platform[i]):
            stone = platform[i][j]
            if stone == 'O':
                damage += len(platform) - i
    return damage


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

    # puzzle1('../puzzles/2023/14/example.txt')  # result -> 136
    puzzle1('../puzzles/2023/14/input.txt')  # result -> 108955
    # puzzle2('../puzzles/2023/14/example.txt')  # result ->
    # puzzle2('../puzzles/2023/14/input.txt')  # result ->

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print_color(f"End Time = {current_time}", Fore.YELLOW)
