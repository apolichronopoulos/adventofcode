# -*- coding: utf-8 -*-
def puzzle1(filename):
    f = open(filename, "r")
    res = 0
    for line in f:
        t1 = ""
        t2 = ""
        for c in line:
            if c.isdigit():
                t2 = c
                if t1 == "":
                    t1 = c
        res += int(t1 + t2)
    print(f"result: {res}")
    return res


numbers = {
    "zero": "0",
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}


def puzzle2(filename):
    f = open(filename, "r")
    res = 0
    for line in f:
        line = line.strip()
        s = len(line)
        t1 = ""
        t2 = ""
        i = 0
        for c in line:
            if c.isdigit():
                t2 = c
                if t1 == "":
                    t1 = c
            else:
                for number in numbers:
                    n = len(number)
                    if line[i : min(i + n, s)] == number:
                        t2 = numbers[number]
                        if t1 == "":
                            t1 = numbers[number]
            i += 1
        res += int(t1 + t2)
    print(f"result: {res}")
    return res


if __name__ == "__main__":
    assert puzzle1("../../puzzles/2023/01/example.txt") == 142
    assert puzzle1("../../puzzles/2023/01/input.txt") == 55108

    assert puzzle2("../../puzzles/2023/01/example2.txt") == 281
    assert puzzle2("../../puzzles/2023/01/input.txt") == 56324
