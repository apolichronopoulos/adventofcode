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
        ranges = line.split(",")
        for r in ranges:
            first, last = r.strip().split("-")
            list_a.append(int(first))
            list_b.append(int(last))


def solve(part=1):
    res = 0
    for i in range(len(list_a)):
        first, last = list_a[i], list_b[i]
        if debug:
            print(f"first: {first} - last: {last}")
        if part == 1:
            for n in range(first, last + 1):
                text_n = str(n)
                if len(text_n) % 2 == 1:
                    continue
                if text_n[: len(text_n) // 2] == text_n[len(text_n) // 2 :]:
                    res += n
                    if debug:
                        print(f"  found invalid ID: {n}")
        else:
            for n in range(first, last + 1):
                text_n = str(n)
                for c in range(1, (len(text_n) // 2) + 1):
                    splits = split_text(text_n, c)
                    if splits and all(s == splits[0] for s in splits):
                        res += n
                        if debug:
                            print(f"  found invalid ID: {n}")
                            print(f" text: {text_n} -> splits: {splits}")
                        break
    return res


def split_text(text_n, c):
    splits = []
    if len(text_n) % c != 0 or len(text_n) // c < 2:
        return splits
    for i in range(0, len(text_n), c):
        splits.append(text_n[i : i + c])
    return splits


def test_split_text():
    assert split_text("123456", 1) == ["1", "2", "3", "4", "5", "6"]
    assert split_text("123456", 2) == ["12", "34", "56"]
    assert split_text("123456", 3) == ["123", "456"]
    assert split_text("123456", 4) == []
    assert split_text("123456", 5) == []
    assert split_text("123456", 6) == []
    assert split_text("123123123", 2) == []
    assert split_text("12121212", 2) == ["12", "12", "12", "12"]
    assert split_text("12121212", 4) == ["1212", "1212"]
    assert split_text("123123123", 3) == ["123", "123", "123"]


if __name__ == "__main__":
    time_and_color(start=True)
    submit = False  # be careful
    debug = False

    assert puzzle(file("/2025/02/example.txt"), read_file, solve, 1) == 1227775554
    answer1 = puzzle(file("/2025/02/input.txt"), read_file, solve, 1)
    assert answer1 == 35367539282

    if submit:
        aoc_submit("2025", "02", 1, answer1)

    if debug:
        test_split_text()

    assert puzzle(file("/2025/02/example.txt"), read_file, solve, 2) == 4174379265

    answer2 = puzzle(file("/2025/02/input.txt"), read_file, solve, 2)
    assert answer2 == 45814076230

    if submit:
        aoc_submit("2025", "02", 2, answer2)

    time_and_color(start=False)
