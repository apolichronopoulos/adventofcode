# -*- coding: utf-8 -*-
import sys

from utils.utils import aoc_submit, file, puzzle, time_and_color

print(sys.getrecursionlimit())
sys.setrecursionlimit(10000)

list_a = []
list_b = []


def read_file(filename, part=1):
    f = open(filename, "r")
    list_a.clear()
    list_b.clear()
    for i, line in enumerate(f):
        line = line.strip()
        if line == "":
            continue
        rotation, number = line[0], line[1:]
        list_a.append(rotation)
        list_b.append(int(number))


def solve(part=1):
    res, index = 0, 50
    for i in range(len(list_a)):
        index, count = calculate_new_index(index, list_a[i], list_b[i], part)
        res += count

    return res


def calculate_new_index(index, r, n, part=1):
    count = 0
    target = index - n if r == "L" else index + n
    new_index = target % 100  # index should be between 0 and 99

    if part == 1:
        return new_index, 1 if new_index == 0 else 0

    clicks_to_zero = index if r == "L" and index != 0 else (100 - index)

    if n >= clicks_to_zero:
        count += 1
        n -= clicks_to_zero
        full_cycles = n // 100
        count += full_cycles

    if debug:
        print(
            f"Running calculate for ({index}, {r}, {n}) - new index: {new_index}, count: {count}"
        )

    return new_index, count


def test_case(index, r, n, expected, part=2):
    new_index, count = calculate_new_index(index, r, n, part)
    assert count == expected, f"Test failed: got {count}, expected {expected}"


def run_tests():
    test_case(97, "L", 3, 0)
    test_case(97, "R", 3, 1)
    test_case(97, "L", 103, 1)
    test_case(97, "R", 103, 2)
    test_case(97, "R", 104, 2)
    test_case(0, "R", 99, 0)
    test_case(0, "R", 100, 1)


if __name__ == "__main__":
    time_and_color(start=True)
    submit = False  # be careful
    debug = False

    assert puzzle(file("/2025/01/example.txt"), read_file, solve, 1) == 3
    answer1 = puzzle(file("/2025/01/input.txt"), read_file, solve, 1)
    assert answer1 == 999

    if submit:
        aoc_submit("2025", "01", 1, answer1)

    if debug:
        run_tests()

    assert puzzle(file("/2025/01/example.txt"), read_file, solve, 2) == 6

    answer2 = puzzle(file("/2025/01/input.txt"), read_file, solve, 2)
    assert answer2 == 6099

    if submit:
        aoc_submit("2025", "01", 2, answer2)

    time_and_color(start=False)
