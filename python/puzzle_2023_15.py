from datetime import datetime
from timeit import default_timer as timer

from colorama import Fore, Back, init

from utils.utils import print_index, print_color

words = []


def read_file(filename, part=1):
    words.clear()
    f = open(filename, "r")
    for line in f:
        line = line.strip()
        if line == "":
            continue
        words.extend(line.split(","))


def get_ascii_hash(text: str):
    res = 0
    for c in text:
        res += ord(c)
        print(f'ASCII code for {c} -> {ord(c)} / total {res}')
        res = res * 17
        print(f'multiplied by 17 for {c} -> {res}')
        res = res % 256
        print(f'module 256 for {c} -> {res}')
    return res


def solve(part=1):
    print_index(words, color=Fore.CYAN, ending="")

    res = 0
    if part == 1:
        print_index(words, color=Fore.RED, ending="")
        for word in words:
            print(f"-------- {words} --------")
            res += get_ascii_hash(word)
    else:
        res = -1

    print_color(f"---------> final result: {res} <---------", Fore.LIGHTRED_EX, Back.LIGHTYELLOW_EX)
    return res


def puzzle1(filename):
    t_start = timer()
    print_color(f"puzzle1: {filename}", Fore.MAGENTA)
    read_file(filename)
    solve()
    t_end = timer()
    print_color(f"Time elapsed (in seconds): {t_end - t_start}", Fore.MAGENTA)


def puzzle2(filename):
    t_start = timer()
    print_color(f"puzzle2: {filename}", Fore.MAGENTA)
    read_file(filename, part=2)
    solve(part=2)
    t_end = timer()
    print(f"Time elapsed (in seconds): {t_end - t_start}")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    init()
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print_color(f"Start Time = {current_time}", Fore.YELLOW)

    # puzzle1('../puzzles/2023/15/example.txt')  # result -> 1320
    # puzzle1('../puzzles/2023/15/input.txt')  # result -> 513643
    puzzle2('../puzzles/2023/15/example.txt')  # result ->
    # puzzle2('../puzzles/2023/15/input.txt')  # result ->

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print_color(f"End Time = {current_time}", Fore.YELLOW)
