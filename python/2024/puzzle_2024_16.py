# -*- coding: utf-8 -*-
import sys

from utils.utils import aoc_submit, file, print_index, puzzle, time_and_color, valid_loc

sys.setrecursionlimit(20000)

elements = []
walls = set()
visited = set()
visited2 = {}
best_score = -1
best_path = set()
start = [-1, -1]
end = [-1, -1]

directions = {
    "^": [
        (-1, 0, "^", 1),
        (0, -1, "<", 1001),
        (0, 1, ">", 1001),
    ],
    ">": [
        (-1, 0, "^", 1001),
        (0, 1, ">", 1),
        (1, 0, "v", 1001),
    ],
    "v": [
        (0, 1, ">", 1001),
        (1, 0, "v", 1),
        (0, -1, "<", 1001),
    ],
    "<": [
        (-1, 0, "^", 1001),
        (1, 0, "v", 1001),
        (0, -1, "<", 1),
    ],
}


def read_file(filename, separator=""):
    f = open(filename, "r")
    elements.clear()
    walls.clear()
    visited.clear()
    visited2.clear()
    best_path.clear()
    global best_score
    best_score = -1

    for line in f:
        elements_i = []
        line = line.strip()
        if line == "":
            continue
        if separator != "":
            line = line.split(separator)
        for c in line:
            elements_i.append(c)
        elements.append(elements_i)


def move(x, y, d, score=0, path=[]):
    if (x, y) in walls:
        return -1, path
    if (x, y) in path:
        return -1, path

    current_path = path.copy()
    current_path.append((x, y))

    if elements[x][y] in ["E"]:
        global best_score
        if score <= best_score or best_score == -1:
            if score < best_score:
                best_path.clear()
            best_score = score
            for p in current_path:
                best_path.add(p)

        return score, current_path

    if (x, y, d) in visited2:
        if visited2[(x, y, d)] < score:
            return -1, path

    visited2[(x, y, d)] = score

    min_path = []
    min_score = -1
    options = directions[d]
    for i, j, d2, s in options:
        temp_score, temp_path = move(x + i, y + j, d2, score + s, current_path)
        if temp_score != -1:
            if temp_score <= min_score or min_score == -1:
                min_score = temp_score
                min_path = temp_path

    if min_score == -1:
        visited.add((x, y, d))

    return min_score, min_path


def solve(part=1):
    res = 0

    h, l = len(elements), len(elements[0])

    for i in range(h):
        for j in range(l):
            c = elements[i][j]
            if c == "#":
                walls.add((i, j))
            elif c == "S":
                start[0], start[1] = i, j
            elif c == "E":
                end[0], end[1] = i, j

    if debug:
        print_index(elements, results=[start, end])
        print("\n------\n")

    res, path = move(start[0], start[1], d=">", score=0)

    if part == 1:
        if debug:
            print_index(
                elements, results=[start, end], counts=[[i, j] for i, j in path]
            )
    else:
        if debug:
            print_index(elements, tuples=[(i, j) for i, j in best_path], tuple_char="0")
        res = len(best_path)

    return res


if __name__ == "__main__":
    time_and_color(start=True)
    debug = False
    submit = False  # be careful

    assert puzzle(file("/2024/16/example.txt"), read_file, solve, 1) == 7036
    assert puzzle(file("/2024/16/example2.txt"), read_file, solve, 1) == 11048
    answer1 = puzzle(file("/2024/16/input.txt"), read_file, solve, 1)
    assert answer1 == 109496
    if submit:
        aoc_submit("2024", "16", 1, answer1)

    assert puzzle(file("/2024/16/example.txt"), read_file, solve, 2) == 45
    assert puzzle(file("/2024/16/example2.txt"), read_file, solve, 2) == 64
    answer2 = puzzle(file("/2024/16/input.txt"), read_file, solve, 2)
    assert answer2 == 551
    if submit:
        aoc_submit("2024", "16", 2, answer2)

    time_and_color(start=False)
