from datetime import datetime
from timeit import default_timer as timer

from colorama import Fore

from utils.utils import print_color

elements = []
counts = []
touch_sides = []

start = [-1, -1]

min_i, min_j, max_i, max_j = -1, -1, -1, -1


# 7 F
# 7 J
# 7 L
# F 7
# F J
# J F
# J L
# L 7
# L J


# |, -, 7, J, L, F
def touch_close(c1, c2, horizontally=True):
    if horizontally:
        return [c1, c2] in [
            ['7', 'F'],
            ['7', 'L'],
            ['F', '7'],
            # ['F', 'J'],  # not close
            ['J', 'F'],
            ['J', 'L'],
            # ['L', '7'],  # not close
            ['L', 'J']
        ]
    else:
        return [c1, c2] in [
            # ['7', 'L'],
            ['7', 'J'],
            ['F', 'L'],
            # ['F', 'J'],
        ]


def read_file(filename, part=1):
    global start
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
    counts.clear()
    touch_sides.clear()

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
    res = count_inside_elements(path)
    t_end = timer()
    print(f"Time elapsed (in seconds): {t_end - t_start}")
    return res


def count_inside_elements(path):
    rows, cols = len(elements), len(elements[0])

    global min_i, min_j, max_i, max_j
    for node in path:
        i, j = node[0], node[1]
        if min_i == -1 or i < min_i:
            min_i = i
        if min_j == -1 or j < min_j:
            min_j = j
        if max_i == -1 or i > max_i:
            max_i = i
        if max_j == -1 or j > max_j:
            max_j = j

    # print_index(path, counts)

    for i in range(rows):
        for j in range(cols):
            if [i, j] not in path:
                if touches_sides(i, j):
                    touch_sides.append([i, j])

    for i in range(min_i, max_i + 1):
        open_row = False
        last_c_row = '.'
        for j in range(min_j, max_j + 1):
            c = elements[i][j]
            if [i, j] in touch_sides:
                continue
            if [i, j] not in path:
                last_c_row = '.'
                if open_row:
                    counts.append([i, j])
                continue
            elif c == '|' or last_c_row == '|':
                open_row = not open_row
            elif c == '-':
                continue
            elif c in ['7', 'L', 'F', 'J']:
                if last_c_row == '.' or touch_close(last_c_row, c):
                    open_row = not open_row
            last_c_row = c

    print(f"counts: {len(counts)}")
    print_index(path, counts)
    count = len(counts)

    print(f"---------> final res: {count} <---------")
    return count


def touches_sides(i, j):
    t1, t2, t3, t4 = True, True, True, True
    for x in range(0, i):
        if elements[x][j] != '.':
            t1 = False
            break
    for x in range(i + 1, len(elements)):
        if elements[x][j] != '.':
            t2 = False
            break
    for x in range(0, j):
        if elements[i][x] != '.':
            t3 = False
            break
    for x in range(j + 1, len(elements[0])):
        if elements[i][x] != '.':
            t4 = False
            break
    return t1 or t2 or t3 or t4


def print_index(path=[], counts=[]):
    # if len(elements) > 100 or len(elements[0]) > 100:
    #     return
    for i in range(0, len(elements)):
        for j in range(0, len(elements[i])):
            c = elements[i][j]
            if [i, j] == start:
                print_color("S", ending=" ", color=Fore.MAGENTA)
            elif [i, j] in path:
                print_color(c, ending=" ")
            elif [i, j] in counts:
                print_color(c, ending=" ", color=Fore.CYAN)
                # print_color("I", ending=" ", color=Fore.CYAN)
            else:
                # print(".", end=" ")
                print(c, end=" ")
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

    # assert puzzle2('../puzzles/2023/10/example_part2_small.txt') == 4  # result -> 4 should be 4
    # assert puzzle2('../puzzles/2023/10/example_part2_large.txt') == 8  # result -> ? should be 8
    # assert puzzle2('../puzzles/2023/10/example_part2_large2.txt') == 10  # result -> ? should be 10

    final_res = puzzle2('../puzzles/2023/10/input.txt')
    assert final_res > 244 and final_res != 68 and final_res != 227 and final_res != 481

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("End Time =", current_time)
