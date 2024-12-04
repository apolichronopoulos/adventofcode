# -*- coding: utf-8 -*-
import sys

from utils.utils import puzzle, read_file, time_and_color

sys.setrecursionlimit(10000)


def check_sequence(line, words):
    res = 0
    for word in words:
        res += line.count(word)
    return res


def solve(part=1, elements=None):
    res = 0

    l = len(elements[0])
    h = len(elements)

    if part == 1:
        words = ["XMAS", "SAMX"]

        # Check horizontal
        for i in range(0, h):
            res += check_sequence("".join(elements[i][:]), words)

        # Check vertical
        for j in range(0, l):
            line = ""
            for i in range(0, h):
                line += elements[i][j]
            res += check_sequence(line, words)

        # Check diagonals part 1
        for i in range(0, h):
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
                res += check_sequence(line1, words)

                line2 = elements[i][j]
                i2, j2 = i, j
                while 1 == 1:
                    i2 -= 1
                    j2 += 1
                    if i2 < 0 or j2 < 0 or i2 >= h or j2 >= l:
                        break
                    line2 += elements[i2][j2]

                res += check_sequence(line2, words)

        # Check diagonals part 2
        for j in range(1, l):
            i3, j3 = h - 1, j
            line3 = elements[i3][j3]
            while 1 == 1:
                i3 -= 1
                j3 += 1
                if i3 < 0 or j3 < 0 or i3 >= h or j3 >= l:
                    break
                line3 += elements[i3][j3]
            res += check_sequence(line3, words)

    else:
        words = ["MAS", "SAM"]
        for i in range(0, h - 2):
            for j in range(0, l - 2):
                w1 = elements[i][j] + elements[i + 1][j + 1] + elements[i + 2][j + 2]
                w2 = elements[i + 2][j] + elements[i + 1][j + 1] + elements[i][j + 2]
                if w1 in words and w2 in words:
                    res += 1

    return res


if __name__ == "__main__":
    time_and_color(start=True)
    debug = False

    assert puzzle("../../puzzles/2024/04/example.txt", read_file, solve, 1) == 18
    assert puzzle("../../puzzles/2024/04/input.txt", read_file, solve, 1) == 2500

    assert puzzle("../../puzzles/2024/04/example.txt", read_file, solve, 2) == 9
    assert puzzle("../../puzzles/2024/04/input.txt", read_file, solve, 2) == 1933

    time_and_color(start=False)
