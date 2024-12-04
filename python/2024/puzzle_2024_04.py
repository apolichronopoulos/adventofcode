# -*- coding: utf-8 -*-
import sys

from utils.utils import puzzle, read_file, time_and_color

sys.setrecursionlimit(10000)

lines = []

word1 = "XMAS"
word2 = "SAMX"


def check_sequence(line):
    res = 0
    res += line.count(word1)
    res += line.count(word2)
    return res


def solve(part=1, elements=None):
    res = 0

    l = len(elements[0])
    h = len(elements)

    for i in range(0, h):
        res += check_sequence("".join(elements[i][:]))

    for j in range(0, l):
        line = ""
        for i in range(0, h):
            line += elements[i][j]
        res += check_sequence(line)

    for i in range(0, j):
        for j in range(0, l):
            if j != 0 and i != 0:
                continue

            line1 = elements[i][j]
            i1, j1 = i, j
            while 1 == 1:
                i1 += 1
                j1 += 1
                if i1 < 0 or j1 < 0 or i1 >= h or j1 >= l:
                    break
                line1 += elements[i1][j1]
            res += check_sequence(line1)

            line2 = elements[i][j]
            i2, j2 = i, j
            while 1 == 1:
                i2 -= 1
                j2 += 1
                if i2 < 0 or j2 < 0 or i2 >= h or j2 >= l:
                    break
                line2 += elements[i2][j2]

            res += check_sequence(line2)

    for j in range(0, l):
        i3, j3 = h - 1, j
        line3 = elements[i3][j3]
        while 1 == 1:
            i3 -= 1
            j3 += 1
            if i3 < 0 or j3 < 0 or i3 >= h or j3 >= l:
                break
            line3 += elements[i3][j3]
        res += check_sequence(line3)

    return res


if __name__ == "__main__":
    time_and_color(start=True)
    debug = False

    assert puzzle("../../puzzles/2024/04/example.txt", read_file, solve, 1) == 18
    assert puzzle("../../puzzles/2024/04/input.txt", read_file, solve, 1) == 2500

    # assert puzzle("../../puzzles/2024/04/example2.txt", read_file, solve, 2) == 0
    # assert puzzle("../../puzzles/2024/04/input.txt", read_file, solve, 2) == 0

    time_and_color(start=False)
