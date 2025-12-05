# -*- coding: utf-8 -*-
import sys

from utils.utils import (
    aoc_submit,
    custom_args,
    file,
    find_all_neighbors,
    print_index,
    puzzle,
    ranges_overlap,
    time_and_color,
)

print(sys.getrecursionlimit())
sys.setrecursionlimit(10000)

ranges = []
ingredients = []


def read_file(filename, part=1):
    f = open(filename, "r")
    ranges.clear()
    ingredients.clear()
    for i, line in enumerate(f):
        line = line.strip()
        if line == "":
            continue
        elif "-" in line:
            s, e = line.split("-")
            ranges.append((int(s), int(e)))
        else:
            ingredients.append(int(line))


def solve(part=1):
    res = 0

    if part == 1:
        for ingredient in ingredients:
            for s, e in ranges:
                if s <= ingredient <= e:
                    res += 1
                    break
    else:
        fresh = list(set(ranges))
        changes = True
        while changes:
            changes = False
            for s, e in fresh:
                for fs, fe in fresh:
                    if ranges_overlap((s, e), (fs, fe)):
                        if (s, e) != (fs, fe):
                            changes = True
                            fresh.remove((s, e))
                            fresh.remove((fs, fe))
                            fresh.append((min(s, fs), max(e, fe)))
                            break
                if changes:
                    break

        for fs, fe in fresh:
            res += fe - fs + 1

    return res


if __name__ == "__main__":
    time_and_color(start=True)
    submit, debug = custom_args().submit, custom_args().debug

    assert puzzle(file("/2025/05/example.txt"), read_file, solve, 1) == 3
    answer1 = puzzle(file("/2025/05/input.txt"), read_file, solve, 1)
    assert answer1 == 529

    if submit:
        aoc_submit("2025", "05", 1, answer1)

    assert puzzle(file("/2025/05/example.txt"), read_file, solve, 2) == 14

    answer2 = puzzle(file("/2025/05/input.txt"), read_file, solve, 2)
    assert answer2 == 344260049617193

    if submit:
        aoc_submit("2025", "05", 2, answer2)

    time_and_color(start=False)
