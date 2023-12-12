from datetime import datetime
from functools import lru_cache
from timeit import default_timer as timer

from utils.utils import print_index

gears = []
gears_numbers = []


def read_file(filename, part=1):
    gears.clear()
    f = open(filename, "r")
    for line in f:
        if line == "":
            continue
        line = line.strip()
        line = line.split()

        if part == 2:
            g = "?".join(5 * [line[0]])
            gn = ",".join(5 * [line[1]])
        else:
            g = line[0]
            gn = line[1]

        gears.append(g)
        gears_numbers.append(gn.split(","))


@lru_cache(maxsize=None)
def find_gears(line):
    results = []
    count = 0
    for i, c in enumerate(line):
        if c == '#':
            count += 1
        elif c == '?':
            return results
        elif count > 0:
            results.append(str(count))
            count = 0
    if count > 0:
        results.append(str(count))
    return results


def solve(part=1):
    # print_index(gears)
    # print_index(gears_numbers)

    res = 0
    for i, case in enumerate(gears_numbers):
        case_s = ",".join(case)
        print(f"{i} - {gears[i]} - {case}")
        works = []
        lines = [gears[i]]
        while lines:
            line = lines[len(lines) - 1]
            del lines[len(lines) - 1]
            if '?' in line:
                for j, c in enumerate(line):
                    if c == '?':
                        for new_c in ['.', '#']:
                            line1 = line[:j] + new_c + line[j + 1:]
                            fgs = ",".join(find_gears(line1))
                            if fgs == '' or case_s.startswith(fgs):
                                lines.append(line1)
            else:
                if find_gears(line) == case:
                    works.append(line)
        res += len(set(works))
        print(f"---------> result: {len(set(works))} <---------")

    print(f"---------> final result: {res} <---------")
    return res


def generate_combinations(s, index, current_combination, combinations):
    if index == len(s):
        combinations.append(''.join(current_combination))
        return

    if s[index] == '?':
        current_combination[index] = '.'
        generate_combinations(s, index + 1, current_combination, combinations)
        current_combination[index] = '#'
        generate_combinations(s, index + 1, current_combination, combinations)
        current_combination[index] = '?'  # reset for backtracking
    else:
        generate_combinations(s, index + 1, current_combination, combinations)


def solve_smart(part=1):
    # print_index(gears)
    # print_index(gears_numbers)

    res = 0
    for i, case in enumerate(gears_numbers):
        print(f"{i} - {gears[i]} - {case}")

        input_string = gears[i]
        initial_combination = list(input_string)
        all_combinations = []
        generate_combinations(input_string, 0, initial_combination, all_combinations)
        count = 0
        for combination in all_combinations:
            if find_gears(combination) == case:
                count += 1
        res += count
        print(f"---------> result: {count} <---------")
    print(f"---------> final result: {res} <---------")
    return res


def puzzle1(filename, brute=True):
    t_start = timer()
    print(f"\n\npuzzle1: {filename}")
    read_file(filename)
    if brute:
        solve()
    else:
        solve_smart()
    t_end = timer()
    print(f"Time elapsed (in seconds): {t_end - t_start}")


def puzzle2(filename, brute=True):
    t_start = timer()
    print(f"\n\npuzzle1: {filename}")
    read_file(filename, part=2)
    if brute:
        solve()
    else:
        solve_smart()
    t_end = timer()
    print(f"Time elapsed (in seconds): {t_end - t_start}")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Start Time =", current_time)

    # puzzle1('../puzzles/2023/12/example.txt')  # result -> 6
    # puzzle1('../puzzles/2023/12/example2.txt')  # result -> 21
    # puzzle1('../puzzles/2023/12/input.txt')  # result -> ?

    # puzzle1('../puzzles/2023/12/example.txt', False)  # result -> 6
    # puzzle1('../puzzles/2023/12/example2.txt', False)  # result -> 21
    # puzzle1('../puzzles/2023/12/input.txt', False)  # result -> 6981

    puzzle2('../puzzles/2023/12/example.txt', False)  # result -> result 6
    # puzzle2('../puzzles/2023/12/example2.txt', False)  # result -> should be ?
    # puzzle2('../puzzles/2023/12/input.txt', False)  # result -> ?

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("End Time =", current_time)
