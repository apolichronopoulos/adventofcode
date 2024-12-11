# -*- coding: utf-8 -*-
import sys
from collections import Counter, defaultdict
from functools import cache

from utils.utils import file, print_index, puzzle, time_and_color

sys.setrecursionlimit(20000)


@cache
def split_number(n):
    if n == 0:
        return [1]
    elif len(str(n)) % 2 == 0:
        n = str(n)
        half = len(n) // 2
        return [int(n[:half]), int(n[half:])]
    else:
        return [2024 * n]


def count_numbers(numbers, blink):
    counts = Counter(numbers)
    for i in range(blink):
        if debug:
            print(f"blink {i}")
        temp = defaultdict(int)
        for n, c in counts.items():
            for n2 in split_number(n):
                temp[n2] += c
        counts = temp
    return sum(counts.values())


def split_numbers(numbers, blink):
    if debug:
        print(f"blink {blink}")
    if blink == 0:
        return numbers
    numbers2 = []
    for n in numbers:
        numbers2.extend(split_number(n))
    return split_numbers(numbers2, blink - 1)


def read_file(filename, separator=" "):
    elements = []
    f = open(filename, "r")
    for line in f:
        elements_i = []
        if line == "":
            continue
        if separator == "":
            line = line.strip()
        else:
            line = line.split(separator)
        for c in line:
            elements_i.append(c)
        elements.append(elements_i)

    return elements


def solve(part=1, elements=None):
    res = 0

    h, l = len(elements), len(elements[0])
    if debug:
        print(f"h{h}, l={l}")
        print_index(elements)

    for i in range(h):
        numbers = [int(x) for x in elements[i]]
        if part == 1:
            res += len(split_numbers(numbers, BLINK_TIMES))
        else:
            res += count_numbers(numbers, BLINK_TIMES)

    return res


if __name__ == "__main__":
    time_and_color(start=True)
    debug = False

    BLINK_TIMES = 1
    assert puzzle(file("/2024/11/example.txt"), read_file, solve, 1) == 7
    BLINK_TIMES = 6
    assert puzzle(file("/2024/11/example2.txt"), read_file, solve, 1) == 22
    BLINK_TIMES = 25
    assert puzzle(file("/2024/11/example2.txt"), read_file, solve, 1) == 55312
    assert puzzle(file("/2024/11/input.txt"), read_file, solve, 1) == 233050
    BLINK_TIMES = 75
    assert puzzle(file("/2024/11/input.txt"), read_file, solve, 2) == 276661131175807

    time_and_color(start=False)
