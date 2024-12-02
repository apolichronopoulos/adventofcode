# -*- coding: utf-8 -*-
import sys
from datetime import datetime
from timeit import default_timer as timer

from colorama import Back, Fore, init
from shapely.geometry import Point, Polygon

# from test4 import is_inside_postgis
from utils.utils import add_direction, print_color, print_index, replace_char


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


def flood_fill(matrix, visited, row, col):
    # Check if the current node is within the matrix and hasn't been visited
    if (
        0 <= row < len(matrix)
        and 0 <= col < len(matrix[0])
        and not visited[row][col]
        and matrix[row][col] == 1
    ):
        # Mark the current node as visited
        visited[row][col] = True

        # Recursively perform flood-fill in all four directions
        flood_fill(matrix, visited, row + 1, col)
        flood_fill(matrix, visited, row - 1, col)
        flood_fill(matrix, visited, row, col + 1)
        flood_fill(matrix, visited, row, col - 1)


def count_enclosed_nodes(matrix, cycle_path_coordinates):
    # Initialize a 2D array to keep track of visited nodes
    visited = [[False for _ in range(len(matrix[0]))] for _ in range(len(matrix))]

    # Iterate through the cycle path coordinates and find a seed point inside the cyclic path
    seed_point = None
    for row, col in cycle_path_coordinates:
        if matrix[row][col] == 1:
            seed_point = (row, col)
            break

    # If a seed point is found, perform flood-fill starting from that point
    if seed_point:
        row, col = seed_point
        flood_fill(matrix, visited, row, col)

    # Count the number of visited nodes (enclosed nodes within the cyclic path)
    enclosed_node_count = sum(row.count(True) for row in visited)

    return enclosed_node_count


def enclosed_nodes(matrix, cycle_path):
    # Convert cycle_path to a Shapely Polygon
    cycle_polygon = Polygon(cycle_path)
    enclosed_nodes_set = set()
    # Iterate through all matrix cells
    for row in range(len(matrix)):
        for col in range(len(matrix[0])):
            point = Point(row, col)

            if cycle_polygon.contains(point):
                enclosed_nodes_set.add((row, col))
                continue

            if point.within(cycle_polygon):
                enclosed_nodes_set.add((row, col))
                continue

            if is_point_inside_cycle_path((row, col), cycle_path):
                enclosed_nodes_set.add((row, col))
                continue

    return enclosed_nodes_set


print(sys.getrecursionlimit())
sys.setrecursionlimit(10000)

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


def fill_tiles(start=None):
    if start is None:
        start = [0, 0]
    global tiles
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


def solve(part=1, case=1, start=None):
    if start is None:
        start = [0, 0]
    res = 0
    fill_tiles()

    #  fill matrix
    for i in range(len(tiles)):
        matrix.append([])
        for j in range(len(tiles[i])):
            matrix[i].append(tiles[i][j])

    for i in range(len(tiles)):
        open_row = False
        last_c_row = "."
        for j in range(len(tiles[i])):
            c = tiles[i][j]
            if c == "#" and last_c_row != "#":
                open_row = not open_row
            elif c != "#" and open_row:
                tiles[i] = replace_char(tiles[i], "*", j)
            last_c_row = c

    for i in range(len(tiles)):
        for j in range(len(tiles[i])):
            if tiles[i][j] == "#" or tiles[i][j] == "*":
                res += 1

    # if len(tiles) < 100 and len(tiles[0]) < 100:
    print_index(tiles, edges=indict, outside=outdict, color=Fore.CYAN, ending="")

    print_color(
        f"---------> final result: {res} <---------",
        Fore.LIGHTRED_EX,
        Back.LIGHTYELLOW_EX,
    )
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


if __name__ == "__main__":
    init()
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print_color(f"Start Time = {current_time}", Fore.YELLOW)

    puzzle1("../../puzzles/2023/19/example.txt")  # result -> 62
    # puzzle1('../../puzzles/2023/19/input.txt')  # result -> ? too low ?
    # puzzle2('../../puzzles/2023/19/example.txt')  # result ->
    # puzzle2('../../puzzles/2023/19/input.txt')  # result ->

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print_color(f"End Time = {current_time}", Fore.YELLOW)
