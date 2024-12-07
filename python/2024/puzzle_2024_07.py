# -*- coding: utf-8 -*-
import itertools
import sys

from utils.utils import file, print_index, puzzle, time_and_color

sys.setrecursionlimit(10000)


def read_file(filename):
    elements = []
    f = open(filename, "r")
    for line in f:
        line = line.strip()
        if line == "":
            continue

        total, amounts = line.split(":")
        amounts = [int(amount.strip()) for amount in amounts.split()]

        elements.append((int(total), amounts))

    return elements


operators = ["+", "*"]


def operation(a, b, operator):
    # print(f"operation: {a} {operator} {b}")
    if operator == "+":
        return a + b
    elif operator == "*":
        return a * b
    else:
        raise f"operator {operator} not supported"


def calculate_total(total, amounts, current=0):
    if len(amounts) > 1:
        for operator in operators:
            current_total = operation(amounts[0], amounts[1], operator)
            current_total = calculate_total(
                total, [current_total] + amounts[2:], current + current_total
            )
            if current_total != 0:
                return current_total
    elif len(amounts) == 1:
        if total == amounts[0]:
            return total
    return 0


def solve(part=1, elements=None):
    res = 0

    matrix = elements
    h, l = len(matrix), len(matrix[0])
    print(f"h: {h}, l: {l}")

    if debug:
        for e in elements:
            print(f"{e[0]} : {e[1]}")
        print("-------------------")

    for total, amounts in elements:
        ct = calculate_total(total, amounts)
        if ct != 0:
            print(f"{total} : {amounts}")

        res += ct

    return res


if __name__ == "__main__":
    time_and_color(start=True)
    debug = True

    assert puzzle(file("/2024/07/example.txt"), read_file, solve, 1) == 3749
    assert puzzle(file("/2024/07/input.txt"), read_file, solve, 1) == 4998764814652
    # assert puzzle(file("/2024/07/example.txt"), read_file, solve, 2) == 0
    # assert puzzle(file("/2024/07/input.txt"), read_file, solve, 2) == 0

    time_and_color(start=False)
