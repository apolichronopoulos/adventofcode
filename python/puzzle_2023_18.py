import os
import sys
from datetime import datetime
from timeit import default_timer as timer

from colorama import Fore, Back, init

from utils.utils import print_color, replace_char, find_neighbors, set_print_color, reset_print_color

print(sys.getrecursionlimit())
sys.setrecursionlimit(10000)


def print_index(index=[], edges={}, inside={}, outside={}, ending=" ", color=Fore.RESET):
    set_print_color(color=color)
    print('-------------------------')
    for i in range(0, len(index)):
        for j in range(0, len(index[i])):
            key = f'{i},{j}'
            c = index[i][j]
            if key in edges:
                print_color(c, color=Fore.RED, ending=ending)
            elif key in inside:
                print_color(c, color=Fore.MAGENTA, ending=ending)
            elif key in outside:
                print_color(c, color=Fore.YELLOW, ending=ending)
            else:
                # print_color('.', color=color, ending=ending)
                print_color(c, color=color, ending=ending)
        print(""),
    print('-------------------------')
    reset_print_color()


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


steps = []
tiles = []
# inside = []
# outside = []

indict = {}
outdict = {}


def read_file(filename, part=1):
    steps.clear()
    tiles.clear()
    f = open(filename, "r")
    for line in f:
        line = line.strip()
        if line == "":
            continue
        steps.append(line)


def solve(part=1):
    global tiles

    # print_index(tiles, color=Fore.CYAN, ending="")
    res = 0

    start = [0, 0]
    tiles.append('.')

    current_point = start

    for step in steps:
        direction, number, color = step.split()
        print(f"{direction}, {number}, {color}")

        for iter in range(int(number)):
            i, j = current_point
            tiles[i] = replace_char(tiles[i], '#', j)
            indict[f'{i},{j}'] = True
            i2, j2 = add_direction(i, j, direction)
            current_point = [i2, j2]
            if i2 >= len(tiles):
                tiles.append(len(tiles[0]) * '.')
            elif i2 < 0:
                new_tiles = [len(tiles[0]) * '.']
                new_tiles.extend(tiles)
                tiles = new_tiles
            elif j2 >= len(tiles[i]):
                for xi in range(len(tiles)):
                    tiles[xi] += '.'
            elif j2 < 0:
                for xi in range(len(tiles)):
                    tiles[xi] = '.' + tiles[xi]

    # print_index(tiles, inside=indict, outside=outdict, color=Fore.CYAN, ending="")
    print(f'tiles: {len(tiles)} rows, {len(tiles[0])} cols')

    find_outside_then_inside()

    print_index(tiles, inside=indict, outside=outdict, color=Fore.CYAN, ending="")

    for i in range(len(tiles)):
        for j in range(len(tiles[i])):
            if tiles[i][j] == '#':
                res += 1

    print_color(f"---------> final result: {res} <---------", Fore.LIGHTRED_EX, Back.LIGHTYELLOW_EX)
    return res


def find_outside_then_inside():
    rows = len(tiles)
    cols = len(tiles[0])

    # find outside step 1

    for i in range(rows):
        for j in range(cols):

            if tiles[i][j] == '#':
                continue
            elif f'{i},{j}' in outdict:
                continue

            tL, tR, tU, tD = True, True, True, True
            for xj in range(j, -1, -1):
                if tiles[i][xj] != '.':
                    tL = False
                    break
                elif f'{i},{xj}' in outdict:
                    break
            if not tL:
                for xj in range(j + 1, len(tiles[0])):
                    if tiles[i][xj] != '.':
                        tR = False
                        break
                    elif f'{i},{xj}' in outdict:
                        break
                if not tR:
                    for xi in range(i, -1, -1):
                        if tiles[xi][j] != '.':
                            tU = False
                            break
                        elif f'{xi},{j}' in outdict:
                            break
                    if not tU:
                        for xi in range(i + 1, len(tiles)):
                            if tiles[xi][j] != '.':
                                tD = False
                                break
                            elif f'{xi},{j}' in outdict:
                                break

            if tL or tR or tD or tU:
                outdict[f'{i},{j}'] = True

    # find outside step 2

    for i in range(len(tiles)):
        for j in range(len(tiles[i])):
            key = f'{i},{j}'
            if tiles[i][j] == '#' or key in indict or key in outdict:
                continue
            neighbours = find_neighbors(i, j, tiles)
            n_out = len([n for n in neighbours if f'{n[0]},{n[1]}' in outdict])
            if n_out:
                outdict[key] = True

    # find outside step 3

    for i in range(len(tiles) - 1, -1, -1):
        for j in range(len(tiles[i]) - 1, -1, -1):
            key = f'{i},{j}'
            if tiles[i][j] == '#' or key in indict or key in outdict:
                continue
            neighbours = find_neighbors(i, j, tiles)
            n_out = len([n for n in neighbours if f'{n[0]},{n[1]}' in outdict])
            if n_out:
                outdict[key] = True

    # find inside

    for i in range(len(tiles)):
        for j in range(len(tiles[i])):
            key = f'{i},{j}'
            if tiles[i][j] == '#' or key in indict or key in outdict:
                continue

            # neighbours = find_neighbors(i, j, tiles)

            # n_inside = len([n for n in neighbours if f'{n[0]},{n[1]}' in indict])
            # n_ = len([n for n in neighbours if f'{n[0]},{n[1]}' in outdict])

            # TODO: if it's not outside, it's probably inside
            indict[f'{i},{j}'] = True
            tiles[i] = replace_char(tiles[i], '#', j)
            # TODO: if it's not outside, it's probably inside

    return


def add_direction(i, j, direction):
    if direction == 'R':
        return [i, j + 1]
    elif direction == 'D':
        return [i + 1, j]
    elif direction == 'L':
        return [i, j - 1]
    elif direction == 'U':
        return [i - 1, j]


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

    # puzzle1('../puzzles/2023/18/example.txt')  # result -> 62
    # puzzle1('../puzzles/2023/18/input.txt')  # result -> 6008 too low
    # puzzle1('../puzzles/2023/18/input.txt')  # result -> 17345 too low
    puzzle1('../puzzles/2023/18/input.txt')  # result -> ???
    # puzzle2('../puzzles/2023/18/example.txt')  # result ->
    # puzzle2('../puzzles/2023/18/input.txt')  # result ->

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print_color(f"End Time = {current_time}", Fore.YELLOW)
