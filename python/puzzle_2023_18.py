import sys
from datetime import datetime
from timeit import default_timer as timer

# import geopandas
# import matplotlib.pyplot as plt
# import momepy
import networkx as nx
from colorama import Fore, Back, init

from utils.utils import print_color, replace_char, set_print_color, reset_print_color, add_direction

# from contextily import add_basemap
# from libpysal import weights

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


def print_index_dummy(index=[]):
    print('-------------------------')
    for i in range(0, len(index)):
        print(index[i])
    print('-------------------------')


path = []
steps = []
tiles = []
matrix = []

vertical = 1
horizontal = 1


def read_file(filename, part=1):
    steps.clear()
    tiles.clear()
    f = open(filename, "r")
    for line in f:
        line = line.strip()
        if line == "":
            continue
        if part == 1:
            steps.append(line)
        else:
            direction, number, color = line.split()
            hex = color[1:-1]
            number = int(hex[1:-1], 16)
            direction = colored_direction[hex[-1:]]
            steps.append(f'{direction} {number} {color}')
            print(f'{direction} {number} {color}')


colored_direction = {
    '0': 'R',
    '1': 'D',
    '2': 'L',
    '3': 'U',
}


def fill_tiles(start=None):
    if start is None:
        start = (0, 0)
    global tiles
    tiles.append('.')
    current_point = start

    for step in steps:
        direction, number, color = step.split()
        print(f" processing step {direction}, {number}, {color}")

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

    print(f'fill_tiles finished')


def fill_tiles2(start=None):
    if start is None:
        start = (0, 0)
    current_point = start
    i, j = current_point
    path.append((i, j))

    global vertical
    global horizontal
    vertical = 1
    horizontal = 1

    for step in steps:
        print_index_dummy(path)
        direction, number, color = step.split()
        print(f" processing step {direction}, {number}, {color}")

        amount = int(number)

        i, j = current_point
        i2, j2 = add_direction(i, j, direction, amount)
        current_point = [i2, j2]
        i, j = current_point
        path.append((i, j))

        if i2 >= vertical:
            print("adding to vertical")
            vertical = i2 + 1
        elif i2 < 0:
            add = abs(i2)
            for pi, p in enumerate(path):
                path[pi] = (p[0] + add, p[1])
            current_point = [i2 + add, j2]
            vertical += add
        elif j2 >= horizontal:
            print("adding to horizontal")
            horizontal = j2 + 1
        elif j2 < 0:
            add = abs(j2)
            for pi, p in enumerate(path):
                path[pi] = (p[0], p[1] + add)
            current_point = [i2, j2 + add]
            horizontal += add

    print_index_dummy(path)

    print(f'fill_tiles finished')


def solve(part=1, case=1, start=None):
    tiles.clear()
    path.clear()
    matrix.clear()

    indict = {}
    nodes = []

    if start is None:
        start = [0, 0]
    res = 0

    if part == 1:
        fill_tiles(start)

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
    else:
        path.clear()
        fill_tiles2()
        print_index_dummy(path)
        min_i, min_j, max_i, max_j = sys.maxsize, sys.maxsize, - sys.maxsize, - sys.maxsize
        min_i_per_j = {}
        max_i_per_j = {}
        min_j_per_i = {}
        max_j_per_i = {}
        for i, j in path:
            min_j_per_i[i] = min(min_j_per_i[i] if i in min_j_per_i else sys.maxsize, j)
            max_j_per_i[i] = max(max_j_per_i[i] if i in max_j_per_i else - sys.maxsize, j)
            min_i_per_j[j] = min(min_i_per_j[j] if j in min_i_per_j else sys.maxsize, i)
            max_i_per_j[j] = max(max_i_per_j[j] if j in max_i_per_j else - sys.maxsize, i)
            min_i = min(i, min_i)
            min_j = min(j, min_j)
            max_i = max(i, max_i)
            max_j = max(j, max_j)

        print(f'min_i: {min_i}, min_j: {min_j}, max_i: {max_i}, max_j: {max_j}')
        print(f'vertical: {vertical}, horizontal: {horizontal}, top size: {vertical * horizontal}')

        res2 = vertical * horizontal
        # for j, items in min_i_per_j.values():

        G = nx.MultiGraph()
        for i, j in path:
            G.add_edge(i, j)
        print(G)
        d = nx.to_dict_of_dicts(G)
        print(d)

        import matplotlib.pyplot as plt
        fig, ax = plt.subplots()
        edge_collection = nx.draw_networkx_edges(G, pos=nx.circular_layout(G), ax=ax)
        self_loop_fap = ax.patches[0]
        # A = np.array([[1, 1], [2, 1]])
        # G = nx.from_numpy_array(A)
        # G.edges(data=True)

        edges = nx.draw_networkx_edges(G, pos=nx.spring_layout(G))




    print_index(tiles, edges=indict, color=Fore.CYAN, ending="")
    print_color(f"---------> final result: {res} <---------", Fore.LIGHTRED_EX, Back.LIGHTYELLOW_EX)
    return res


def puzzle1(filename):
    t_start = timer()
    print_color(f"puzzle1: {filename}", Fore.MAGENTA)
    read_file(filename)
    res = solve()
    t_end = timer()
    print_color(f"Time elapsed (in seconds): {t_end - t_start}", Fore.MAGENTA)
    return res


def puzzle2(filename):
    t_start = timer()
    print_color(f"puzzle2: {filename}", Fore.MAGENTA)
    read_file(filename, part=2)
    res = solve(part=2)
    t_end = timer()
    print(f"Time elapsed (in seconds): {t_end - t_start}")
    return res


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    init()
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print_color(f"Start Time = {current_time}", Fore.YELLOW)

    # puzzle1('../puzzles/2023/18/example.txt')  # result -> 62
    # puzzle1('../puzzles/2023/18/example2.txt')  # result -> 62
    # puzzle1('../puzzles/2023/18/input.txt')  # result -> 106459 >>> CORRECT <<<

    assert puzzle2('../puzzles/2023/18/example.txt') != 1407376496241  # result -> 952408144115 ???
    # assert puzzle2('../puzzles/2023/18/example.txt') ==  952408144115  # result -> 952408144115 ???
    # puzzle2('../puzzles/2023/18/input.txt')  # result ->

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print_color(f"End Time = {current_time}", Fore.YELLOW)
