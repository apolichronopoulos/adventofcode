# -*- coding: utf-8 -*-
import sys

from utils.utils import (
    aoc_submit,
    custom_args,
    file,
    get_permutations,
    puzzle,
    time_and_color,
)

print(sys.getrecursionlimit())
sys.setrecursionlimit(10000)

devices = []
outputs = []
dev_positions = {}
END_DEVICE = "out"


def read_file(filename, part=1):
    f = open(filename, "r")
    devices.clear()
    outputs.clear()
    dev_positions.clear()
    for i, line in enumerate(f):
        line = line.strip()
        if line == "":
            continue

        device, output = line.split(":")
        devices.append(device)
        outputs.append([x for x in output.strip().split()])


def solve(part=1):
    res = 0

    for i in range(len(devices)):
        dev_positions[devices[i]] = i

    if part == 1:
        START_DEVICE = "you"
        res += dfs(START_DEVICE, END_DEVICE, {})
    else:
        START_DEVICE = "svr"
        MUST_VISIT = ["dac", "fft"]
        for a, b in get_permutations(MUST_VISIT):
            p1 = dfs(START_DEVICE, a, {})
            p2 = dfs(a, b, {})
            p3 = dfs(b, END_DEVICE, {})
            res += p1 * p2 * p3

    return res


def dfs(start, end, cache={}):
    if start == end:
        return 1
    elif start not in dev_positions:
        return 0
    elif (start, end) in cache:
        return cache[(start, end)]

    paths = 0
    for o in outputs[dev_positions[start]]:
        paths += dfs(o, end, cache)
    cache[(start, end)] = paths

    return paths


if __name__ == "__main__":
    time_and_color(start=True)
    submit, debug = custom_args().submit, custom_args().debug

    assert puzzle(file("/2025/11/example.txt"), read_file, solve, 1) == 5
    answer1 = puzzle(file("/2025/11/input.txt"), read_file, solve, 1)
    assert answer1 == 477

    if submit:
        aoc_submit("2025", "11", 1, answer1)

    assert puzzle(file("/2025/11/example2.txt"), read_file, solve, 2) == 2
    answer2 = puzzle(file("/2025/11/input.txt"), read_file, solve, 2)
    assert answer2 == 383307150903216

    if submit:
        aoc_submit("2025", "11", 2, answer2)

    time_and_color(start=False)
