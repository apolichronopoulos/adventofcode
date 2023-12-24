import sys
from datetime import datetime
from timeit import default_timer as timer

from colorama import Fore, Back, init

from utils.utils import print_color, replace_char, set_print_color, reset_print_color, add_direction

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
            elif key in outside:
                print_color(c, color=Fore.YELLOW, ending=ending)
            elif key in inside:
                print_color(c, color=Fore.MAGENTA, ending=ending)
            else:
                # print_color('.', color=color, ending=ending)
                print_color(c, color=color, ending=ending)
        print(""),
    print('-------------------------')
    reset_print_color()


path = []
steps = []
tiles = []
matrix = []

total_nodes = 0


def read_file(filename, part=1):
    steps.clear()
    tiles.clear()
    f = open(filename, "r")
    for line in f:
        line = line.strip()
        if line == "":
            continue
        steps.append(line)


def fill_tiles(start=None):
    if start is None:
        start = (0, 0)
    global tiles
    tiles.append('.')
    current_point = start

    for step in steps:
        direction, number, color = step.split()
        print(f"{direction}, {number}, {color}")

        global total_nodes
        total_nodes += int(number)

        for iter in range(int(number)):
            # print_index(tiles, color=Fore.CYAN, ending="")

            i, j = current_point
            tiles[i] = replace_char(tiles[i], '#', j)
            i2, j2 = add_direction(i, j, direction)
            current_point = [i2, j2]
            i, j = current_point

            # indict[f'{i},{j}'] = True
            path.append((i, j))

            if i2 >= len(tiles):
                tiles.append(len(tiles[0]) * '.')
            elif i2 < 0:
                new_tiles = [len(tiles[0]) * '.']
                new_tiles.extend(tiles)
                tiles = new_tiles
                for pi, p in enumerate(path):
                    path[pi] = (p[0] + 1, p[1])
                current_point = [i2 + 1, j2]
            elif j2 >= len(tiles[i]):
                for xi in range(len(tiles)):
                    tiles[xi] += '.'
            elif j2 < 0:
                for xi in range(len(tiles)):
                    tiles[xi] = '.' + tiles[xi]
                for pi, p in enumerate(path):
                    path[pi] = (p[0], p[1] + 1)
                current_point = [i2, j2 + 1]

    if len(tiles) < 100 and len(tiles[0]) < 100:
        print_index(tiles, color=Fore.CYAN, ending="")


def solve(part=1, case=1, start=None):
    tiles.clear()
    path.clear()
    steps.clear()
    matrix.clear()

    if start is None:
        start = [0, 0]
    res = 0
    fill_tiles(start)

    indict = {}
    nodes = []
    #  fill matrix
    for i in range(len(tiles)):
        matrix.append([])
        for j in range(len(tiles[i])):
            matrix[i].append(tiles[i][j])
            if tiles[i][j] == '#':
                nodes.append((i, j))
                indict[f'{i},{j}'] = True

    for i in range(len(tiles)):
        open_row = False
        last_c_row = '.'
        startUp = False
        startDown = False

        for j in range(len(tiles[i])):
            c = tiles[i][j]

            path_current = path.index((i, j)) if (i, j) in path else -1
            path_U = path.index((i - 1, j)) if (i - 1, j) in path else -1
            path_D = path.index((i + 1, j)) if (i + 1, j) in path else -1

            if c == '#' and last_c_row != '#':  # open
                tU = path_current != -1 and path_U != -1 and abs(path_current - path_U) == 1
                tD = path_current != -1 and path_D != -1 and abs(path_current - path_D) == 1
                startUp = tU and not tD
                startDown = tD and not tU
                open_row = not open_row
            elif c == '#':  # close
                if (i, j + 1) not in path:
                    tU = path_current != -1 and path_U != -1 and abs(path_current - path_U) == 1
                    tD = path_current != -1 and path_D != -1 and abs(path_current - path_D) == 1
                    endUp = tU and not tD
                    endDown = tD and not tU
                    if not (startUp and endDown) and not (startDown and endUp):
                        open_row = not open_row
            elif c != '#' and open_row:  # inside
                tiles[i] = replace_char(tiles[i], '*', j)
            last_c_row = c

    for i in range(len(tiles)):
        for j in range(len(tiles[i])):
            if tiles[i][j] == '#' or tiles[i][j] == '*':
                res += 1

    print_index(tiles, edges=indict, color=Fore.CYAN, ending="")
    print_color(f"---------> final result: {res} <---------", Fore.LIGHTRED_EX, Back.LIGHTYELLOW_EX)
    return res


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
    # puzzle1('../puzzles/2023/18/example2.txt')  # result -> 62
    puzzle1('../puzzles/2023/18/input.txt')  # result -> 106459 >>> CORRECT <<<

    # puzzle2('../puzzles/2023/18/example.txt')  # result ->
    # puzzle2('../puzzles/2023/18/input.txt')  # result ->

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print_color(f"End Time = {current_time}", Fore.YELLOW)
