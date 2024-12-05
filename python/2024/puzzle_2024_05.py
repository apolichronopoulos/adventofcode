# -*- coding: utf-8 -*-
import sys

import numpy as np
from utils.utils import file, puzzle, time_and_color

sys.setrecursionlimit(10000)

orders = []
updates = []
correct_updates = []
incorrect_updates = []


def read_file(filename):
    orders.clear()
    updates.clear()
    correct_updates.clear()
    incorrect_updates.clear()
    f = open(filename, "r")
    section = 1
    for line in f:
        line = line.strip()
        if line == "":
            section = 2
            continue
        if section == 1:
            items = line.split("|")
            orders.append([int(item) for item in items])
        else:
            items = line.split(",")
            updates.append([int(item) for item in items])


def check_order(update):
    error = False
    for i in range(len(update)):
        n1 = update[i]
        if error:
            break
        for j in range(i + 1, len(update)):
            n2 = update[j]
            if [n2, n1] in orders:
                error = True
                break
    return error


def solve(part=1):
    res = 0

    for update in updates:
        error = check_order(update)
        if not error:
            correct_updates.append(update)
        else:
            incorrect_updates.append(update)

    if part == 1:
        for update in correct_updates:
            arr = np.array(update)
            center = np.take(arr, arr.size // 2)
            res += center
    else:
        for update in incorrect_updates:
            for j in range(len(update) - 1):
                for i in range(len(update) - 1 - j):
                    n1 = update[i]
                    n2 = update[i + 1]
                    if [n2, n1] in orders:
                        update[i], update[i + 1] = update[i + 1], update[i]
            arr = np.array(update)
            center = np.take(arr, arr.size // 2)
            res += center
    return res


if __name__ == "__main__":
    time_and_color(start=True)
    debug = False

    assert puzzle(file("/2024/05/example.txt"), read_file, solve, 1) == 143
    assert puzzle(file("/2024/05/input.txt"), read_file, solve, 1) == 6384
    assert puzzle(file("/2024/05/example.txt"), read_file, solve, 2) == 123
    assert puzzle(file("/2024/05/input.txt"), read_file, solve, 2) == 5353

    time_and_color(start=False)
