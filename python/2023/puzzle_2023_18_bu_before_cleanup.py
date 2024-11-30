# -*- coding: utf-8 -*-
import os
import sys
from datetime import datetime
from timeit import default_timer as timer

from colorama import Back, Fore, init
from shapely.geometry import Point, Polygon
from utils.utils import (
    add_direction,
    print_color,
    replace_char,
    reset_print_color,
    set_print_color,
)


def is_point_inside_cycle_path(point, cycle_path_coordinates):
    x, y = point
    cycle_path = cycle_path_coordinates

    # Check if the point is inside the cycle path using the ray casting algorithm
    inside = False
    for i in range(len(cycle_path)):
        x1, y1 = cycle_path[i]
        x2, y2 = cycle_path[(i + 1) % len(cycle_path)]

        if ((y1 <= y < y2) or (y2 <= y < y1)) and (
            x < (x2 - x1) * (y - y1) / (y2 - y1) + x1
        ):
            inside = not inside

    return inside


def enclosed_nodes(matrix, cycle_path):
    # Convert cycle_path to a Shapely Polygon
    cycle_polygon = Polygon(cycle_path)
    enclosed_nodes_set = set()
    # Iterate through all matrix cells
    for row in range(len(matrix)):
        for col in range(len(matrix[0])):
            point = Point(row, col)
            # if cycle_polygon.contains(point):
            #     enclosed_nodes_set.add((row, col))
            if point.within(cycle_polygon):
                enclosed_nodes_set.add((row, col))

    # for row in range(len(matrix)):
    #     for col in range(len(matrix[0])):
    #         point = (col, row)
    #         if is_point_inside_cycle_path(point, cycle_path):
    #             # nodes_in_cycle_path.append(point)
    #             enclosed_nodes_set.add((row, col))

    return enclosed_nodes_set


print(sys.getrecursionlimit())
sys.setrecursionlimit(10000)


def print_index(
    index=[], edges={}, inside={}, outside={}, ending=" ", color=Fore.RESET
):
    set_print_color(color=color)
    print("-------------------------")
    for i in range(0, len(index)):
        for j in range(0, len(index[i])):
            key = f"{i},{j}"
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
    print("-------------------------")
    reset_print_color()


def cls():
    os.system("cls" if os.name == "nt" else "clear")


path = []
steps = []
tiles = []
matrix = []
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

    res = 0

    start = [0, 0]
    tiles.append(".")

    current_point = start

    for step in steps:
        direction, number, color = step.split()
        print(f"{direction}, {number}, {color}")

        for iter in range(int(number)):
            i, j = current_point
            tiles[i] = replace_char(tiles[i], "#", j)
            indict[f"{i},{j}"] = True
            path.append((i, j))
            i2, j2 = add_direction(i, j, direction)
            current_point = [i2, j2]
            if i2 >= len(tiles):
                tiles.append(len(tiles[0]) * ".")
            elif i2 < 0:
                new_tiles = [len(tiles[0]) * "."]
                new_tiles.extend(tiles)
                tiles = new_tiles
            elif j2 >= len(tiles[i]):
                for xi in range(len(tiles)):
                    tiles[xi] += "."
            elif j2 < 0:
                for xi in range(len(tiles)):
                    tiles[xi] = "." + tiles[xi]

    if len(tiles) < 100 and len(tiles[0]) < 100:
        print_index(tiles, color=Fore.CYAN, ending="")

    # graph = nx.Graph()
    # graph = nx.DiGraph()
    # path.append('0,0')

    for i in range(len(tiles)):
        matrix.append([])
        for j in range(len(tiles[i])):
            matrix[i].append(tiles[i][j])
            # for n in find_neighbors(i, j, tiles):
            #     graph.add_edge(f'{i},{j}', f'{n[0]},{n[1]}', weight=0)

    matrix2 = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

    # for i in range(len(path) - 1):
    # node1 = path[i]
    # node2 = path[i + 1]
    # graph.add_edge(node1, node2, weight=1, direction='right')

    # r1 = nx.find_cycle(graph, '0,0', '0,0')
    # r2 = nx.dag_longest_path(graph, )

    # enclosed_nodes = nx.nodes_inside_cycle(graph, path)
    # enclosed_nodes = nx.cycle_basis

    # cycle_path = []
    # point = (start[0], start[1])
    # last_direction = ''
    # for p in path:
    #     if point == p:
    #         continue
    #     direction = calculate_direction(point[0], point[1], p[0], p[1])
    #     if direction != last_direction:
    #         last_direction = direction
    #         cycle_path.append(point)
    #     point = p

    cycle_path = []
    cycle_path.extend(path)
    cycle_path.append((start[0], start[1]))

    result = enclosed_nodes(matrix, cycle_path)

    inside = {}
    for r in result:
        inside[f"{r[0]},{r[1]}"] = True
        if tiles[r[0]][r[1]] == "#":
            continue
        tiles[r[0]] = replace_char(tiles[r[0]], "*", r[1])
    for r in cycle_path:
        # inside[f"{r[0]},{r[1]}"] = True
        tiles[r[0]] = replace_char(tiles[r[0]], "x", r[1])

    for i in range(len(tiles)):
        for j in range(len(tiles[i])):
            if tiles[i][j] == "#" or tiles[i][j] == "*" or tiles[i][j] == "x":
                res += 1

    if len(tiles) < 100 and len(tiles[0]) < 100:
        print_index(
            tiles,
            edges=indict,
            inside=inside,
            outside=outdict,
            color=Fore.CYAN,
            ending="",
        )

    print_color(
        f"---------> final result: {res} <---------",
        Fore.LIGHTRED_EX,
        Back.LIGHTYELLOW_EX,
    )
    # print_color(f"---------> final result: {len(enclosed_nodes)} <---------", Fore.LIGHTRED_EX, Back.LIGHTYELLOW_EX)
    # print_color(f"---------> final result: {len(result) + len(path)} <---------", Fore.LIGHTRED_EX, Back.LIGHTYELLOW_EX)
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
if __name__ == "__main__":
    init()
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print_color(f"Start Time = {current_time}", Fore.YELLOW)

    puzzle1("../../puzzles/2023/18/example.txt")  # result -> 62
    # puzzle1('../../puzzles/2023/18/input.txt')  # result -> 6008 too low
    # puzzle1('../../puzzles/2023/18/input.txt')  # result -> 17345 too low
    # puzzle1('../../puzzles/2023/18/input.txt')  # result -> 22346 too low ?
    # puzzle1('../../puzzles/2023/18/input.txt')  # result -> ? too low ?
    # puzzle2('../../puzzles/2023/18/example.txt')  # result ->
    # puzzle2('../../puzzles/2023/18/input.txt')  # result ->

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print_color(f"End Time = {current_time}", Fore.YELLOW)
