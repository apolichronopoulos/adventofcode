# -*- coding: utf-8 -*-
import sys

import sympy as sp
from sympy import Integer
from utils.utils import aoc_submit, file, puzzle, time_and_color

sys.setrecursionlimit(20000)

buttons_a = []
buttons_b = []
prizes = []


def read_file(filename, separator=":"):
    buttons_a.clear()
    buttons_b.clear()
    prizes.clear()
    f = open(filename, "r")
    for line in f:
        line = line.strip()
        if line == "":
            continue
        else:
            line = line.split(separator)
            numbers = line[1].strip().split(",")
            x, y = int((numbers[0]).strip()[2:]), int(numbers[1].strip()[2:])
            if line[0].lower() == "button a":
                buttons_a.append((x, y))
            elif line[0].lower() == "button b":
                buttons_b.append((x, y))
            else:
                prizes.append((x, y))


def solve(part=1):
    res = 0

    for i in range(len(prizes)):

        x, y = prizes[i][0], prizes[i][1]
        a_x, a_y = buttons_a[i][0], buttons_a[i][1]
        b_x, b_y = buttons_b[i][0], buttons_b[i][1]

        if part == 2:
            x += 10000000000000
            y += 10000000000000

        if debug:
            print(f"Button A: X+{a_x}, Y+{a_y}")
            print(f"Button B: X+{b_x}, Y+{b_y}")
            print(f"Prize: X={x}, Y={y}")
            print("")

        unknowns = sp.symbols("a b")
        a, b = unknowns

        equations = []  # build system of 2 equations with 2 unknowns
        equations.append(sp.Eq(a * a_x + b * b_x, x))
        equations.append(sp.Eq(a * a_y + b * b_y, y))

        solutions = sp.solve(equations, unknowns)
        a = solutions[a]
        b = solutions[b]

        if part == 1:
            if not (0 <= a <= 100 and 0 <= b <= 100):
                continue

        if isinstance(a, Integer) and isinstance(b, Integer):
            tokens = a * 3 + b
            if debug:
                print(f"Prize {i}: {a} * 3 + {b} = {tokens}")
            res += tokens

    return res


if __name__ == "__main__":
    time_and_color(start=True)
    debug = False

    assert puzzle(file("/2024/13/example.txt"), read_file, solve, 1) == 480
    answer1 = puzzle(file("/2024/13/input.txt"), read_file, solve, 1)
    assert answer1 == 29436
    # aoc_submit("2024", "13", 1, answer1)

    assert puzzle(file("/2024/13/example.txt"), read_file, solve, 2) == 875318608908
    answer2 = puzzle(file("/2024/13/input.txt"), read_file, solve, 2)
    assert answer2 == 103729094227877
    # aoc_submit("2024", "13", 2, answer2)

    time_and_color(start=False)
