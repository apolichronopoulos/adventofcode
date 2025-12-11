# -*- coding: utf-8 -*-
import sys

from utils.utils import (
    aoc_submit,
    custom_args,
    file,
    puzzle,
    substring_between,
    time_and_color,
)

print(sys.getrecursionlimit())
sys.setrecursionlimit(10000)

devices = []
outputs = []
dev_positions = {}
START_DEVICE = "you"
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

    if debug:
        for i in range(len(devices)):
            print("Device:", devices[i], "Output:", outputs[i])


def solve(part=1):
    res = 0

    for i in range(len(devices)):
        dev_positions[devices[i]] = i

    if part == 1:
        paths = travel([[dev_positions[START_DEVICE]]], [])
        if debug:
            for p in paths:
                print(f"Path: {p}")
        res += len(paths)

    return res


def travel(paths=[], end_paths=[]):
    if len(paths) == 0:
        return []

    new_paths = []
    while len(paths) > 0:
        path = paths.pop(0)
        pos = path[-1]
        for o in outputs[pos]:
            if o == END_DEVICE:
                path.append(END_DEVICE)
                end_paths.append(path)
            else:
                new_pos = dev_positions[o]
                if new_pos not in path:
                    new_paths.append(path + [new_pos])

    return travel(new_paths, end_paths) if len(new_paths) > 0 else end_paths


if __name__ == "__main__":
    time_and_color(start=True)
    submit, debug = custom_args().submit, custom_args().debug

    assert puzzle(file("/2025/11/example.txt"), read_file, solve, 1) == 5
    answer1 = puzzle(file("/2025/11/input.txt"), read_file, solve, 1)
    assert answer1 == 477

    if submit:
        aoc_submit("2025", "11", 1, answer1)

    # assert puzzle(file("/2025/11/example.txt"), read_file, solve, 2) == -1
    # answer2 = puzzle(file("/2025/11/input.txt"), read_file, solve, 2)
    # assert answer2 == -1
    #
    # if submit:
    #     aoc_submit("2025", "11", 2, answer2)

    time_and_color(start=False)
