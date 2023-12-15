from datetime import datetime
from timeit import default_timer as timer

from colorama import Fore

from utils.utils import print_color

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

    results = []
    for final_path in final_paths:
        results.append((len(final_path) - 1) // 2)

    max_res = 0
    duplicates = [number for number in results if results.count(number) > 1]
    results = list(set(duplicates))
    for res in results:
        max_res = res

    final_path = []
    for path in final_paths:
        if max_res == (len(path) - 1) // 2:
            final_path = path
            break

    if part == 1:
        # print(f"---------> final path: {final_path} <---------")
        print(f"---------> final res: {max_res} <---------")
    # else:
    #     print(f"---------> final path: {final_path} <---------")

    return final_path


def puzzle1(filename):
    t_start = timer()
    print(f"\n\npuzzle1: {filename}")
    read_file(filename)
    solve()
    t_end = timer()
    print(f"Time elapsed (in seconds): {t_end - t_start}")


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
    t_start = timer()
    print(f"\n\npuzzle2: {filename}")
    read_file(filename)
    path = solve(2)
    count_inside_tiles(path)
    t_end = timer()
    print(f"Time elapsed (in seconds): {t_end - t_start}")


def count_inside_tiles(path):
    print(f"---------> final path: {path} <---------")

    min_i = -1
    min_j = -1
    max_i = -1
    max_j = -1

    for node in path:
        i = node[0]
        j = node[1]
        if min_i == -1 or i < min_i:
            min_i = i
        if min_j == -1 or j < min_j:
            min_j = j
        if max_i == -1 or i > max_i:
            max_i = i
        if max_j == -1 or j > max_j:
            max_j = j

    # print_index(path)

    row_openers = [[] for x in range(min_i, max_i + 1)]
    column_openers = [[] for x in range(min_j, max_j + 1)]

    counts_rows = []
    counts_cols = []

    for i in range(min_i, max_i + 1):
        for j in range(min_j, max_j + 1):
            c = elements[i][j]
            if [i, j] in path:
                if open_row(c):
                    row_openers[i - min_i].append(j)
                if open_col(c):
                    column_openers[j - min_j].append(i)

    for i in range(min_i, max_i + 1):
        for j in range(min_j, max_j + 1):
            if [i, j] not in path:
                count = 0
                for index in row_openers[i - min_i]:
                    if j < index:
                        break
                    count += 1
                if count % 2 != 0:
                    counts_rows.append([i, j])
                count = 0
                for index in column_openers[j - min_j]:
                    if i < index:
                        break
                    count += 1
                if count % 2 != 0:
                    counts_cols.append([i, j])

    print_index(path, counts_rows)
    print(f"counts_rows: {len(counts_rows)}")

    counts = []
    for c in counts_rows:
        # counts.append(c)
        if c in counts_cols:
            counts.append(c)

    print_index(path, counts)
    count = len(counts)

    print(f"---------> final res: {count} <---------")
    return count


# -
# L
# F

# |
# J
# 7

def open_row(c):
    return c in ['|', 'L', 'F', 'J', '7']


def close_row(c):
    return c in ['|', 'J', '7']


def open_col(c):
    return c in ['-', 'L', 'F', 'J', '7']


def close_col(c):
    return c in ['-', 'L', 'J']


#
# def touch_in_row(c1, c2):
#     return c1 in ['L', 'F', '-'] and c2 in ['7', 'J', '-']
#
#
# def touch_in_col(c1, c2):
#     return c1 in ['7', 'F', '|'] and c2 in ['L', 'J', '|']


def print_index(path=[], counts=[]):
    for i in range(0, len(elements)):
        for j in range(0, len(elements[i])):
            c = elements[i][j]
            if [i, j] == start:
                print_color("S", ending=" ", color=Fore.MAGENTA)
            elif [i, j] in path:
                print_color(c, ending=" ")
            elif [i, j] in counts:
                print_color("I", ending=" ", color=Fore.CYAN)
            else:
                print(".", end=" ")
        print(""),


# print(f"final_path: {path}")
# print(np.matrix(path))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Start Time =", current_time)
    # puzzle1('../puzzles/2023/10/example.txt')  # result -> 4
    # puzzle1('../puzzles/2023/10/example2.txt')  # result -> 8
    # puzzle1('../puzzles/2023/10/input.txt')  # result -> 6875 correct
    # puzzle2('../puzzles/2023/10/example_part2_small.txt')  # result -> 4 should be 4
    puzzle2('../puzzles/2023/10/example_part2_large.txt')  # result -> ? should be 8
    # puzzle2('../puzzles/2023/10/example_part2_large2.txt')  # result -> ? should be 10
    # puzzle2('../puzzles/2023/10/input.txt')  # result -> ?
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("End Time =", current_time)
