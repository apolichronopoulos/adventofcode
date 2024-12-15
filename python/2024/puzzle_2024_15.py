# -*- coding: utf-8 -*-
import sys

from utils.utils import aoc_submit, file, print_index, puzzle, time_and_color, valid_loc

sys.setrecursionlimit(20000)

elements = []
moves = []
robot = set()
walls = set()
boxes = set()

moves_forward = {
    "^": (-1, 0),
    ">": (0, 1),
    "v": (1, 0),
    "<": (0, -1),
}


double = {
    "#": ["[", "]"],
    "@": ["@", "."],
    ".": [".", "."],
}


def read_file(filename, separator=""):
    f = open(filename, "r")
    elements.clear()
    moves.clear()
    walls.clear()
    boxes.clear()
    robot.clear()

    for line in f:
        elements_i = []
        line = line.strip()
        if line == "":
            continue
        if separator != "":
            line = line.split(separator)
        for c in line:
            elements_i.append(c)
        if elements_i[0] == "#":
            elements.append(elements_i)
        else:
            moves.extend(elements_i)


def move_item(x, y, m, h, l, box=False):
    x1 = x + moves_forward[m][0]
    y1 = y + moves_forward[m][1]
    if not valid_loc(x1, y1, h, l) or (x1, y1) in walls:
        return False
    moved = True
    if (x1, y1) in boxes:
        moved = move_item(x1, y1, m, h, l, box=True)
    if moved:
        if not box:
            robot.clear()
            robot.add((x1, y1))
        else:
            boxes.remove((x, y))
            boxes.add((x1, y1))
        return True


def solve(part=1):
    res = 0

    grid = elements.copy()

    h, l = len(elements), len(elements[0])
    if debug:
        print_index(elements)
        print(f"h={h}, l={l}")
        for i in range(len(moves)):
            print(i)

    start = (-1, -1)
    for i in range(h):
        for j in range(l):
            c = grid[i][j]
            if c == "@":
                start = (i, j)
            elif c == "#":
                walls.add((i, j))
            elif c == "O":
                boxes.add((i, j))

    if debug:
        print_index(grid, tuples=boxes)

    robot.clear()
    robot.add(start)
    for m in moves:
        r = robot.pop()
        robot.add(r)
        moved = move_item(r[0], r[1], m, h, l, box=False)
        if debug:
            print_index(grid, tuples=boxes)

    for b in boxes:
        i, j = b
        res += (100 * i) + j

    if part == 1:
        print(f"part = {part}")
    else:
        print(f"part = {part}")

    return res


if __name__ == "__main__":
    time_and_color(start=True)
    debug = False

    assert puzzle(file("/2024/15/example.txt"), read_file, solve, 1) == 2028
    assert puzzle(file("/2024/15/example2.txt"), read_file, solve, 1) == 10092
    answer1 = puzzle(file("/2024/15/input.txt"), read_file, solve, 1)
    assert answer1 == 1492518
    # aoc_submit("2024", "15", 1, answer1)

    assert puzzle(file("/2024/15/example.txt"), read_file, solve, 2) == 9021
    # answer2 = puzzle(file("/2024/15/input.txt"), read_file, solve, 2)
    # assert answer2 == 0
    # aoc_submit("2024", "15", 2, answer2)

    time_and_color(start=False)
