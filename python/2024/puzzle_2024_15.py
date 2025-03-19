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
    "#": ["#", "#"],
    "@": ["@", "."],
    ".": [".", "."],
    "O": ["[", "]"],
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


def move_robot(x, y, m, h, l):
    x1 = x + moves_forward[m][0]
    y1 = y + moves_forward[m][1]
    if not valid_loc(x1, y1, h, l) or (x1, y1) in walls:
        return False

    elements_bu = [[e for e in row] for row in elements]
    boxes_bu = set(b for b in boxes)
    moved = True
    if (x1, y1) in boxes:
        moved = move_box(x1, y1, m, h, l)
    if moved:
        robot.clear()
        robot.add((x1, y1))
        elements[x][y] = "."
        elements[x1][y1] = "@"
    else:
        elements.clear()
        for row in elements_bu:
            elements.append(row)
        boxes.clear()
        for box in boxes_bu:
            boxes.add(box)

    return moved


def move_box(x, y, m, h, l):
    c = elements[x][y]
    if c == "[":
        xl, yl = x, y
        xr, yr = x, y + 1
    elif c == "]":
        xl, yl = x, y - 1
        xr, yr = x, y
    else:
        raise "error"

    x1 = xl + moves_forward[m][0]
    y1 = yl + moves_forward[m][1]
    x2 = xr + moves_forward[m][0]
    y2 = yr + moves_forward[m][1]

    if (not valid_loc(x1, y1, h, l)) or (x1, y1) in walls:
        return False

    if (not valid_loc(x2, y2, h, l)) or (x2, y2) in walls:
        return False

    moved1, moved2 = True, True

    if m == "<" and (x1, y1) in boxes:
        moved1 = move_box(x1, y1, m, h, l)
    if m == ">" and (x2, y2) in boxes:
        moved1 = move_box(x2, y2, m, h, l)
    if m in ["^", "v"]:
        if (x1, y1) in boxes:
            moved1 = move_box(x1, y1, m, h, l)
        if moved1 and (x2, y2) in boxes:
            moved2 = move_box(x2, y2, m, h, l)

    if moved1 and moved2:
        if (xl, yl) in boxes:
            boxes.remove((xl, yl))
        if (xr, yr) in boxes:
            boxes.remove((xr, yr))
        boxes.add((x1, y1))
        boxes.add((x2, y2))

        elements[xl][yl] = "."
        elements[xr][yr] = "."
        elements[x1][y1] = "["
        elements[x2][y2] = "]"

    return moved1 and moved2


def print_grid():
    print_index(
        elements,
        counts=[[i, j] for i, j in boxes],
        results=[[i, j] for i, j in walls],
        tuples=robot,
        tuple_char="",
        ending="",
    )


def solve(part=1):
    res = 0

    h, l = len(elements), len(elements[0])
    if part == 2:
        for i in range(h):
            row = []
            for j in range(l):
                row.extend(double[elements[i][j]])
            elements[i] = row

    h, l = len(elements), len(elements[0])

    start = (-1, -1)
    for i in range(h):
        for j in range(l):
            c = elements[i][j]
            if c == "@":
                start = (i, j)
            elif c == "#":
                walls.add((i, j))
            elif c in ["O", "[", "]"]:
                boxes.add((i, j))

    robot.clear()
    robot.add(start)

    if debug:
        print_grid()

    for e, m in enumerate(moves):
        r = robot.pop()
        robot.add(r)
        if part == 1:
            moved = move_item(r[0], r[1], m, h, l, box=False)
        else:
            moved = move_robot(r[0], r[1], m, h, l)
            if debug:
                print_grid()

    if part == 1:
        for b in boxes:
            i, j = b
            res += (100 * i) + j
    else:
        box_scores = {}
        for b in boxes:
            i, j = b
            if (i, j) in box_scores:
                continue
            c = elements[i][j]
            if c == "[":
                x1, y1 = i, j
                x2, y2 = i, j + 1
            else:
                x1, y1 = i, j - 1
                x2, y2 = i, j

            box_scores[(x1, y1, x2, y2)] = x1 * 100 + y1

        for k in sorted(list(box_scores)):
            v = box_scores[k]
            if debug:
                print(f"{k[0]} * 100 + {k[1]} = {v}")
            res += v

    return res


if __name__ == "__main__":
    time_and_color(start=True)
    debug = False
    submit = False  # be careful

    assert puzzle(file("/2024/15/example.txt"), read_file, solve, 1) == 2028
    assert puzzle(file("/2024/15/example2.txt"), read_file, solve, 1) == 10092
    answer1 = puzzle(file("/2024/15/input.txt"), read_file, solve, 1)
    assert answer1 == 1492518
    if submit:
        aoc_submit("2024", "15", 1, answer1)

    assert puzzle(file("/2024/15/example3.txt"), read_file, solve, 2) == 618
    assert puzzle(file("/2024/15/example2.txt"), read_file, solve, 2) == 9021
    answer2 = puzzle(file("/2024/15/input.txt"), read_file, solve, 2)
    assert answer2 != 1500827
    assert answer2 == 1512860
    if submit:
        aoc_submit("2024", "15", 2, answer2)

    time_and_color(start=False)
