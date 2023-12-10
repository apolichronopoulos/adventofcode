from timeit import default_timer as timer
from datetime import datetime
import numpy as np

elements = []
max_size = 0
start = [-1, -1]


def read_file(filename, part=1):
    global start
    global max_size
    elements.clear()
    f = open(filename, "r")
    for line in f:
        elements_i = []
        line = line.strip()
        if line == "":
            continue
        for c in line:
            if c == "S":
                start = [len(elements), len(elements_i)]
            elements_i.append(c)
        elements.append(elements_i)


def solve_recursive(part=1):
    res = 0
    path = [start]
    path = navigate(path)

    print(f"path: {path}")
    print(np.matrix(path))
    res = len(path) // 2
    print(f"res: {res}")


def solve(part=1):
    final_paths = []
    paths = [[start]]
    while paths:
        new_paths = []
        for i in range(0, len(paths)):
            path = paths[i]
            if len(path) > 1 and path[0] == path[len(path) - 1]:
                final_paths.append(path)
                continue
            p_x = -1
            p_y = -1
            x = path[len(path) - 1][0]
            y = path[len(path) - 1][1]
            if len(path) > 1:
                p_x = path[len(path) - 2][0]
                p_y = path[len(path) - 2][1]

            cases = find_cases(x, y, p_x, p_y)
            for case in cases:
                path2 = []
                path2.extend(path)
                path2.append(case)
                new_paths.append(path2)
        paths = new_paths

    # final_path = final_paths[0]
    for final_path in final_paths:
        # for i in range(0, len(elements)):
        #     for j in range(0, len(elements[i])):
        #         if [i, j] in final_path:
        #             print("x", end=" "),
        #         else:
        #             print("-", end=" "),
        #     print(""),
        # print(f"final_path: {final_path}")
        # print(np.matrix(final_path))
        res = (len(final_path) - 1) // 2
        print(f"res: {res}")


def navigate(path):
    current = path[len(path) - 1]
    x = current[0]
    y = current[1]
    c = elements[x][y]

    previous_x = -1
    previous_y = -1
    if len(path) > 1:
        previous = path[len(path) - 2]
        previous_x = previous[0]
        previous_y = previous[1]
        if x == start[0] and y == start[1]:
            # looped // remove last ?
            return path

    cases = find_cases(x, y, previous_x, previous_y)
    for case in cases:
        path2 = []
        path2.extend(path)
        path2.extend([case])
        path2 = navigate(path2)
        if len(path2) > 1 and path2[0][0] == path2[len(path2) - 1][0] and path2[0][1] == path2[len(path2) - 1][1]:
            return path2

    return path


def puzzle1(filename):
    start = timer()
    print(f"\n\npuzzle1: {filename}")
    read_file(filename)
    # solve_recursive()
    solve()
    end = timer()
    print(f"Time elapsed (in seconds): {end - start}")


def find_cases(x, y, previous_x, previous_y):
    c = elements[x][y]
    all_cases = []
    if c == 'S':
        all_cases.append([x - 1, y])
        all_cases.append([x + 1, y])
        all_cases.append([x, y - 1])
        all_cases.append([x, y + 1])
    elif c == 'J':
        all_cases.append([x - 1, y])
        all_cases.append([x, y - 1])
    elif c == 'L':
        all_cases.append([x - 1, y])
        all_cases.append([x, y + 1])
    elif c == 'F':
        all_cases.append([x, y + 1])
        all_cases.append([x + 1, y])
    elif c == '7':
        all_cases.append([x, y - 1])
        all_cases.append([x + 1, y])
    elif c == '|':
        all_cases.append([x - 1, y])
        all_cases.append([x + 1, y])
    elif c == '-':
        all_cases.append([x, y - 1])
        all_cases.append([x, y + 1])

    cases = []
    for case in all_cases:
        if case[0] < 0 or case[1] < 0:
            continue
        elif case[0] == previous_x and case[1] == previous_y:
            continue
        c2 = elements[case[0]][case[1]]
        if c2 == '.':
            continue
        cases.append(case)

    return cases


def puzzle2(filename):
    start = timer()
    print(f"\n\npuzzle2: {filename}")
    read_file(filename)
    # solve_recursive(2)
    solve(2)
    end = timer()
    print(f"Time elapsed (in seconds): {end - start}")



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Start Time =", current_time)
    # puzzle1('../puzzles/2023/10/example.txt')  # result -> 4
    # puzzle1('../puzzles/2023/10/example2.txt')  # result -> 8
    # puzzle1('../puzzles/2023/10/input.txt')  # result -> 48 wrong
    # puzzle1('../puzzles/2023/10/input.txt')  # result -> 6828 wrong
    # puzzle1('../puzzles/2023/10/input.txt')  # result -> 6875 correct
    puzzle2('../puzzles/2023/10/example.txt')  # result -> ?
    # puzzle2('../puzzles/2023/10/input.txt')  # result -> ?
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("End Time =", current_time)
