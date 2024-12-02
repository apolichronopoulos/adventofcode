# -*- coding: utf-8 -*-
def puzzle1(filename, max_colors):
    f = open(filename, "r")
    res = 0
    for line in f:
        print(line)
        x = line.split(":")
        game = int(x[0].strip().split()[1])
        possible = True
        for round in x[1].split(";"):
            for color in round.split(","):
                n = int(color.strip().split()[0])
                c = color.strip().split()[1][0]
                if max_colors[c] < n:
                    possible = False
        if possible:
            res += game

    print(f"result: {res}")
    return res


def puzzle2(filename):
    f = open(filename, "r")
    res = 0
    for line in f:
        print(line)
        x = line.split(":")
        max_colors = {"r": 0, "g": 0, "b": 0}
        for round in x[1].split(";"):
            for color in round.split(","):
                n = int(color.strip().split()[0])
                c = color.strip().split()[1][0]
                if max_colors[c] < n:
                    max_colors[c] = n
        power = (
            max(max_colors["r"], 1) * max(max_colors["g"], 1) * max(max_colors["b"], 1)
        )
        print(f"max_colors {max_colors}\n")
        print(f"power {power}\n")
        res += power

    print(f"result: {res}")
    return res


if __name__ == "__main__":
    max_colors = {"r": 12, "g": 13, "b": 14}
    assert puzzle1("../../puzzles/2023/02/example.txt", max_colors) == 8
    assert puzzle1("../../puzzles/2023/02/input.txt", max_colors) == 2169
    assert puzzle2("../../puzzles/2023/02/example.txt") == 2286
    assert puzzle2("../../puzzles/2023/02/input.txt") == 60948
