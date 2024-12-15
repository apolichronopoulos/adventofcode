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


def move_robot(x, y, m, h, l, part=1):
    x1 = x + moves_forward[m][0]
    y1 = y + moves_forward[m][1]
    if not valid_loc(x1, y1, h, l) or (x1, y1) in walls:
        return False

    moved = True
    if (x1, y1) in boxes:
        moved = move_box(x1, y1, m, h, l, part)

    if moved:
        robot.clear()
        robot.add((x1, y1))

    return moved


def move_box(x, y, m, h, l, part=1):
    c = elements[x][y]
    dy = 1 if c == "[" else -1
    x0, y0 = x, y + dy

    if c == "[":
        xl, yl = x, y
        xr, yr = x0, y0
        x1 = x + moves_forward[m][0]
        y1 = y + moves_forward[m][1]
        x2 = x + moves_forward[m][0]
        y2 = y + 1 + moves_forward[m][1]
    elif c == "]":
        xl, yl = x0, y0
        xr, yr = x, y
        x1 = x + moves_forward[m][0]
        y1 = y - 1 + moves_forward[m][1]
        x2 = x + moves_forward[m][0]
        y2 = y + moves_forward[m][1]
    else:
        raise "error"

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
        i, j = moves_forward[m]
        if (x1, y1) in boxes:
            moved1 = move_box(x1, y1, m, h, l)
        if (x2, y2) in boxes:
            moved2 = move_box(x2, y2, m, h, l)

        c1 = elements[x1][y1]
        c2 = elements[x2][y2]
        if c1 != "." and c2 != ".":
            if moved1 and not moved2:
                move_back(x1 + i, y1 + j, m)
            if not moved1 and moved2:
                move_back(x2 + i, y2 + j, m)

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


def move_back(x, y, m):
    if debug:
        print_index(elements)

    c = elements[x][y]
    if c == "[":
        x1, y1 = x, y
        x2, y2 = x, y + 1
    else:
        x1, y1 = x, y - 1
        x2, y2 = x, y

    i, j = moves_forward[m]
    i, j = -i, -j

    if (x1, y1) not in boxes or (x2, y2) not in boxes:
        return

    boxes.remove((x1, y1))
    boxes.remove((x2, y2))
    boxes.add((x1 + i, y1 + j))
    boxes.add((x2 + i, y2 + j))

    elements[x1][y1] = "."
    elements[x2][y2] = "."
    elements[x1 + i][y1 + j] = "["
    elements[x2 + i][y2 + j] = "]"

    if debug:
        print_index(elements)


def print_grid(h, l):
    for i in range(h):
        for j in range(l):
            if (i, j) in boxes:
                a = 1
            elif (i, j) in walls:
                elements[i][j] = "#"
            elif (i, j) in robot:
                elements[i][j] = "@"
            else:
                elements[i][j] = "."
    print_index(
        elements,
        counts=[[i, j] for i, j in boxes],
        results=[[i, j] for i, j in walls],
        tuples=robot,
        tuple_char="@",
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
        print_grid(h, l)

    for m in moves:
        r = robot.pop()
        robot.add(r)
        if part == 1:
            moved = move_item(r[0], r[1], m, h, l, box=False)
        else:
            moved = move_robot(r[0], r[1], m, h, l)
            if debug and moved:
                print(f"\nMove: {m}")
                r = robot.pop()
                robot.add(r)
                print_grid(h, l)

    if part == 1:
        for b in boxes:
            i, j = b
            res += (100 * i) + j
    else:
        box_scores = {}
        for b in boxes:
            i, j = b
            c = elements[i][j]
            if c == "[":
                x1, y1 = i, j
                x2, y2 = i, j + 1
            else:
                x1, y1 = i, j - 1
                x2, y2 = i, j

            score = x1 * 100 + y1
            box_scores[(x1, y1, x2, y2)] = score

        for k in box_scores:
            v = box_scores[k]
            if debug:
                print(f"{k} --> {v}")
            res += v

    return res


if __name__ == "__main__":
    time_and_color(start=True)
    debug = False

    # assert puzzle(file("/2024/15/example.txt"), read_file, solve, 1) == 2028
    # assert puzzle(file("/2024/15/example2.txt"), read_file, solve, 1) == 10092
    # answer1 = puzzle(file("/2024/15/input.txt"), read_file, solve, 1)
    # assert answer1 == 1492518
    # aoc_submit("2024", "15", 1, answer1)

    # debug = True
    # assert puzzle(file("/2024/15/example3.txt"), read_file, solve, 2) == 618
    assert puzzle(file("/2024/15/example2.txt"), read_file, solve, 2) == 9021
    answer2 = puzzle(file("/2024/15/input.txt"), read_file, solve, 2)
    assert answer2 > 1500827
    # aoc_submit("2024", "15", 2, answer2)

    time_and_color(start=False)
