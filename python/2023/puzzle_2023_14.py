# -*- coding: utf-8 -*-
from datetime import datetime
from timeit import default_timer as timer

from colorama import Back, Fore, init
from utils.utils import print_color, print_index, replace_char

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
    print_index(platform, color=Fore.CYAN, ending="")

    res = 0
    if part == 1:
        move_north(platform)
        print_index(platform, color=Fore.RED, ending="")
        res = calculate_damage(platform)
    else:
        cycles = 1000000000
        # cycles = 3
        # cycles = 1000
        results = []
        repeating = []
        prefix_numbers = []
        for cycle in range(1, cycles + 1):
            print(f"cycle: {cycle}")
            move_north(platform)
            move_west(platform)
            move_south(platform)
            move_east(platform)
            results.append(str(calculate_damage(platform)))

            # prework = 2 steps
            # cyclic repeat loop  every 7 steps
            # '87,69,69,69,65,64,65,63,68,69,69,65,64,65,63,68,69,69,65,64,65,63,68,69,69,65,64,65,63,68'
            #        69,69,65,64,65,63,68

            found_cycle = False
            cycle_numbers = []
            for cycle_size in range(3, len(results) // 2):
                if found_cycle:
                    break
                counter = 1
                last_numbers = results[-cycle_size:]
                previous_numbers = results[:-cycle_size]
                while len(previous_numbers) >= cycle_size:
                    last_numbers2 = previous_numbers[-cycle_size:]
                    previous_numbers2 = previous_numbers[:-cycle_size]
                    if last_numbers == last_numbers2:
                        counter += 1
                        previous_numbers = previous_numbers2
                        if counter >= 4:
                            found_cycle = True
                            cycle_numbers.extend(last_numbers)
                            break
                    else:
                        break

            if found_cycle:
                print(f"found_cycle: {cycle_numbers}")
                repeating.extend(cycle_numbers)
                prefix_numbers = results[: -4 * len(cycle_numbers)]
                break
        if repeating:
            required = cycles - len(prefix_numbers)
            target = required % len(repeating)
            res = repeating[target - 1]
    print_color(
        f"---------> final result: {res} <---------",
        Fore.LIGHTRED_EX,
        Back.LIGHTYELLOW_EX,
    )
    return res


# / ↑ north / ← west / ↓ south / → east /
def move_north(platform, index=0):
    if index == len(platform) - 1:
        return
    for i, row in enumerate(platform):
        if i == 0:
            continue
        for j, column in enumerate(platform[i]):
            stone = platform[i][j]
            if stone == "O":
                if platform[i - 1][j] == ".":
                    platform[i - 1] = replace_char(platform[i - 1], stone, j)
                    platform[i] = replace_char(platform[i], ".", j)
    return move_north(platform, index + 1)


# / ↑ north / ← west / ↓ south / → east /
def move_west(platform, index=0):
    if index == len(platform[0]) - 1:
        return
    for j in range(0, len(platform[0])):
        if j == 0:
            continue
        next_j = j - 1
        for i, row in enumerate(platform):
            stone = platform[i][j]
            if stone == "O":
                if platform[i][next_j] == ".":
                    platform[i] = replace_char(platform[i], stone, next_j)
                    platform[i] = replace_char(platform[i], ".", j)
    return move_west(platform, index + 1)


# / ↑ north / ← west / ↓ south / → east /
def move_south(platform, index=0):
    if index == len(platform) - 1:
        return
    for i in range(len(platform) - 2, -1, -1):
        next_i = i + 1
        for j, column in enumerate(platform[i]):
            stone = platform[i][j]
            if stone == "O":
                if platform[next_i][j] == ".":
                    platform[next_i] = replace_char(platform[next_i], stone, j)
                    platform[i] = replace_char(platform[i], ".", j)
    return move_south(platform, index + 1)


# / ↑ north / ← west / ↓ south / → east /
def move_east(platform, index=0):
    if index == len(platform[0]) - 1:
        return
    for j in range(len(platform[0]) - 2, -1, -1):
        next_j = j + 1
        for i, row in enumerate(platform):
            stone = platform[i][j]
            if stone == "O":
                if platform[i][next_j] == ".":
                    platform[i] = replace_char(platform[i], stone, next_j)
                    platform[i] = replace_char(platform[i], ".", j)
    return move_east(platform, index + 1)


def calculate_damage(platform):
    damage = 0
    for i, row in enumerate(platform):
        for j, column in enumerate(platform[i]):
            stone = platform[i][j]
            if stone == "O":
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
if __name__ == "__main__":
    init()
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print_color(f"Start Time = {current_time}", Fore.YELLOW)

    # puzzle1('../puzzles/2023/14/example.txt')  # result -> 136
    # puzzle1('../puzzles/2023/14/input.txt')  # result -> 108955
    # puzzle2('../puzzles/2023/14/example.txt')  # result -> 64 ? 1000000000 cycles
    puzzle2("../../puzzles/2023/14/input.txt")  # result -> 106689 ? 1000000000 cycles

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print_color(f"End Time = {current_time}", Fore.YELLOW)
