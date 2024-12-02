# -*- coding: utf-8 -*-
def check_adjustment_cells(grid, i, j, m, n, distance=1):
    i_from = min(max(0, i - distance), m)
    i_to = min(max(0, i + distance + 1), m)
    j_from = min(max(0, j - distance), n)
    j_to = min(max(0, j + distance + 1), n)
    for h in range(i_from, i_to):
        for f in range(j_from, j_to):
            cell = grid[h][f]
            if (not cell.isdigit()) and (cell != "."):
                return True
    return False


def check_adjustment_gear(grid, i, j, m, n, distance=1):
    i_from = min(max(0, i - distance), m)
    i_to = min(max(0, i + distance + 1), m)
    j_from = min(max(0, j - distance), n)
    j_to = min(max(0, j + distance + 1), n)
    for h in range(i_from, i_to):
        for f in range(j_from, j_to):
            cell = grid[h][f]
            if cell == "*":
                return [h, f]
    return [-1, -1]


def puzzle1(filename):
    grid = []
    with open(filename, "r") as f:
        for line in f.readlines():
            array_line = []
            for c in line.strip():
                array_line.append(c)
            grid.append(array_line)
    res = 0
    m = len(grid)
    n = len(grid[0])
    i = 0
    while i < m:
        j = 0
        number = ""
        while j < n:
            check_number = False
            if grid[i][j].isdigit():
                number += grid[i][j]
                if j == n - 1:
                    check_number = True
            elif number != "":
                check_number = True
            if check_number:
                for x in range(j - len(number), j):
                    if check_adjustment_cells(grid, i, x, m, n):
                        res += int(number)
                        break
                number = ""
            j += 1
        i += 1
    print(f"result: {res}")
    return res


def puzzle2(filename):
    grid = []
    with open(filename, "r") as f:
        for line in f.readlines():
            array_line = []
            for c in line.strip():
                array_line.append(c)
            grid.append(array_line)
    res = 0
    gears = {}
    m = len(grid)
    n = len(grid[0])
    i = 0
    while i < m:
        j = 0
        number = ""
        while j < n:
            check_number = False
            if grid[i][j].isdigit():
                number += grid[i][j]
                if j == n - 1:
                    check_number = True
            elif number != "":
                check_number = True
            if check_number:
                for x in range(j - len(number), j):
                    gear = check_adjustment_gear(grid, i, x, m, n)
                    if gear[0] != -1:
                        key = str(f"{gear[0]}:{gear[1]}")
                        if key not in gears:
                            gears[str(f"{gear[0]}:{gear[1]}")] = []
                        gears[str(f"{gear[0]}:{gear[1]}")].append(int(number))
                        break
                number = ""
            j += 1
        i += 1
    for g in gears:
        if len(gears[g]) == 2:
            res += gears[g][0] * gears[g][1]
    print(f"result: {res}")
    return res


if __name__ == "__main__":
    assert puzzle1("../../puzzles/2023/03/example.txt") == 4361
    assert puzzle1("../../puzzles/2023/03/input.txt") == 526404
    assert puzzle2("../../puzzles/2023/03/example.txt") == 467835
    assert puzzle2("../../puzzles/2023/03/input.txt") == 84399773
