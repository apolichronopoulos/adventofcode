import os
import sys
from datetime import datetime
from timeit import default_timer as timer

from colorama import Fore, Back, init
from shapely.geometry import Point, Polygon

# from test4 import is_inside_postgis
from utils.utils import print_color, replace_char, set_print_color, reset_print_color


def is_point_inside_cycle_path(point, cycle_path_coordinates):
    x, y = point
    cycle_path = cycle_path_coordinates
    # Check if the point is inside the cycle path using the ray casting algorithm
    inside = False
    for i in range(len(cycle_path)):
        x1, y1 = cycle_path[i]
        x2, y2 = cycle_path[(i + 1) % len(cycle_path)]
        if ((y1 <= y < y2) or (y2 <= y < y1)) and (x < (x2 - x1) * (y - y1) / (y2 - y1) + x1):
            inside = not inside
    return inside


def flood_fill(matrix, visited, row, col):
    # Check if the current node is within the matrix and hasn't been visited
    if 0 <= row < len(matrix) and 0 <= col < len(matrix[0]) and not visited[row][col] and matrix[row][col] == 1:
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

            # if cycle_polygon.contains(point):
            #     enclosed_nodes_set.add((row, col))
            #     continue

            if point.within(cycle_polygon):
                enclosed_nodes_set.add((row, col))
                continue

            # if is_point_inside_cycle_path((row, col), cycle_path):
            #     enclosed_nodes_set.add((row, col))
            #     continue

    # for row in range(len(matrix)):
    #     for col in range(len(matrix[0])):
    #         point = (row, col)
    #         if is_point_inside_cycle_path(point, cycle_path):
    #             enclosed_nodes_set.add((row, col))

    return enclosed_nodes_set


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


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


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


def solve(part=1, case=1):
    global tiles

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
            path.append((i, j))
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

    if len(tiles) < 100 and len(tiles[0]) < 100:
        print_index(tiles, color=Fore.CYAN, ending="")

    for i in range(len(tiles)):
        matrix.append([])
        for j in range(len(tiles[i])):
            matrix[i].append(tiles[i][j])

    # path.append((0, 0))
    # case = 1  # use 1 for X corners or 2 for all path in polygon - 20949 with or without 0,0
    case = 2  # use 1 for X corners or 2 for all path in polygon - 20949 with or without 0,0
    print(f'case: {case}')
    if case == 1:
        cycle_path = []
        point = (start[0], start[1])
        last_direction = ''
        for p in path:
            if point == p:
                continue
            direction = calculate_direction(point[0], point[1], p[0], p[1])
            if direction != last_direction:
                last_direction = direction
                cycle_path.append(point)
            point = p
        for r in cycle_path:
            tiles[r[0]] = replace_char(tiles[r[0]], 'x', r[1])
    else:
        cycle_path = []
        cycle_path.extend(path)
        cycle_path.append((start[0], start[1]))

    # res = count_enclosed_nodes(matrix, cycle_path)

    result = enclosed_nodes(matrix, cycle_path)

    inside = {}
    for r in result:
        inside[f"{r[0]},{r[1]}"] = True
        if tiles[r[0]][r[1]] == '#': continue
        tiles[r[0]] = replace_char(tiles[r[0]], '*', r[1])

    for i in range(len(tiles)):
        for j in range(len(tiles[i])):
            if tiles[i][j] == '#' or tiles[i][j] == '*' or tiles[i][j] == 'x':
                res += 1

    if len(tiles) < 100 and len(tiles[0]) < 100:
        print_index(tiles, edges=indict, inside=inside, outside=outdict, color=Fore.CYAN, ending="")

    print_color(f"---------> final result: {res} <---------", Fore.LIGHTRED_EX, Back.LIGHTYELLOW_EX)
    # print_color(f"---------> final result: {len(enclosed_nodes)} <---------", Fore.LIGHTRED_EX, Back.LIGHTYELLOW_EX)
    # print_color(f"---------> final result: {len(result) + len(path)} <---------", Fore.LIGHTRED_EX, Back.LIGHTYELLOW_EX)
    return res


def add_direction(i, j, direction):
    if direction == 'R':
        return [i, j + 1]
    elif direction == 'D':
        return [i + 1, j]
    elif direction == 'L':
        return [i, j - 1]
    elif direction == 'U':
        return [i - 1, j]


def calculate_direction(i, j, i2, j2):
    if i2 > i:
        return "D"  # downwards
    elif j2 > j:
        return "R"  # rightwards
    elif i > i2:
        return "U"  # upwards
    elif j > j2:
        return "L"  # rightwards


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
    puzzle1('../puzzles/2023/18/input.txt')  # result -> ? too low ?
    # puzzle1('../puzzles/2023/18/input.txt')  # result -> 6008 too low
    # puzzle1('../puzzles/2023/18/input.txt')  # result -> 17345 too low
    # puzzle1('../puzzles/2023/18/input.txt')  # result -> 22346 too low ?
    # puzzle1('../puzzles/2023/18/input.txt')  # result -> 20949 too low ?
    # puzzle1('../puzzles/2023/18/input.txt')  # result -> 21088 too low ?
    # puzzle1('../puzzles/2023/18/input.txt')  # result -> 21362 too low ?
    # puzzle1('../puzzles/2023/18/input.txt')  # result -> 21267 too low ?

    # puzzle2('../puzzles/2023/18/example.txt')  # result ->
    # puzzle2('../puzzles/2023/18/input.txt')  # result ->

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print_color(f"End Time = {current_time}", Fore.YELLOW)
