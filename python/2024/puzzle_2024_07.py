# -*- coding: utf-8 -*-
import sys

from utils.utils import file, puzzle, time_and_color

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


operators = {"+", "*"}


def operation(a, b, operator):
    if operator == "+":
        return a + b
    elif operator == "*":
        return a * b
    elif operator == "||":
        return int(f"{a}{b}")
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
    if debug:
        for e in elements:
            print(f"{e[0]} : {e[1]}")
        print("-------------------")
    if part == 2:
        operators.add("||")
    for total, amounts in elements:
        res += calculate_total(total, amounts)
    return res


if __name__ == "__main__":
    time_and_color(start=True)
    debug = False

    assert puzzle(file("/2024/07/example.txt"), read_file, solve, 1) == 3749
    assert puzzle(file("/2024/07/input.txt"), read_file, solve, 1) == 4998764814652
    assert puzzle(file("/2024/07/example.txt"), read_file, solve, 2) == 11387
    assert puzzle(file("/2024/07/input.txt"), read_file, solve, 2) == 37598910447546

    time_and_color(start=False)
