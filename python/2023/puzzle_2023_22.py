# -*- coding: utf-8 -*-
import sys
from datetime import datetime
from timeit import default_timer as timer

from colorama import Back, Fore, init
from utils.utils import print_color

print(sys.getrecursionlimit())
sys.setrecursionlimit(10000)

bricks = []

max_x = -1
max_y = -1
max_z = -1

brick_blocks = {}
space = {}


def read_file(filename, part=1):
    bricks.clear()
    f = open(filename, "r")
    for i, line in enumerate(f):
        line = line.strip()
        if line == "":
            continue
        bricks.append([])
        for brick in line.split("~"):
            x, y, z = brick.split(",")
            x, y, z = int(x), int(y), int(z)
            global max_x, max_y, max_z
            max_x = max(max_x, x)
            max_y = max(max_y, y)
            max_z = max(max_z, z)
            bricks[i].append((x, y, z))


def solve(part=1):
    global start
    # print_index_dummy(bricks)

    brick_blocks.clear()
    space.clear()

    for z in range(max_z):
        space[z + 1] = []
        for x in range(max_x + 1):
            space[z + 1].append([])
            for y in range(max_y + 1):
                space[z + 1][x].append("-")

    for id, brick in enumerate(bricks):

        # id = pos_to_char(id)
        id = str(id)

        x0, y0, z0 = brick[0]
        x1, y1, z1 = brick[1]
        blocks = []
        for x in range(x0, x1 + 1):
            for y in range(y0, y1 + 1):
                for z in range(z0, z1 + 1):
                    blocks.append((x, y, z))
                    space[z][x][y] = str(id)
        brick_blocks[id] = blocks

    has_changes = 1
    while has_changes != 0:
        has_changes = len(apply_gravity(brick_blocks, space))

    res = 0
    for uid, blocks in brick_blocks.items():
        # print(f'removing id {id} brick')
        cp_space = {}
        for z in range(max_z):
            cp_space[z + 1] = []
            for x in range(max_x + 1):
                cp_space[z + 1].append([])
                for y in range(max_y + 1):
                    cp_space[z + 1][x].append("-")

        cp_brick_blocks = {}
        for k, v in brick_blocks.items():
            if k != uid:
                cp_blocks = []
                for x, y, z in v:
                    cp_space[z][x][y] = k
                    cp_blocks.append((x, y, z))
                cp_brick_blocks[k] = cp_blocks

        bricks_changed = apply_gravity(cp_brick_blocks, cp_space)
        if part == 1:
            if not bricks_changed:
                res = res + 1
        else:
            all_bricks_changed = set()
            while bricks_changed:
                for brick in bricks_changed:
                    all_bricks_changed.add(brick)
                bricks_changed = apply_gravity(cp_brick_blocks, cp_space)
            res += len(all_bricks_changed)

    # for z in range(1, max_z + 1):
    #     print(f'------ id: {z} ------')
    #     print_index_dummy(space[z])

    print_color(
        f"---------> final result: {res} <---------",
        Fore.LIGHTRED_EX,
        Back.LIGHTYELLOW_EX,
    )
    return res


def get_min_z(blocks):
    min_z = sys.maxsize
    for x, y, z in blocks:
        if z < min_z:
            min_z = z
    return min_z


def apply_gravity(brick_blocks2, space2):
    # for z in range(1, max_z + 1):
    # print(f'------ id: {z} ------')
    # print_index_dummy(space2[z])
    bricks_changed = set()
    for id, blocks in brick_blocks2.items():
        if get_min_z(blocks) == 1:
            continue
        is_stuck = False
        loop = 0
        while not is_stuck:
            loop += 1
            # print(f'id {id} loop {loop}')
            new_blocks = []
            for x, y, z in blocks:
                z = int(z)
                new_blocks.append((x, y, z - 1))
                if get_min_z(blocks) == 1 or (
                    space2[z - 1][x][y] != "-" and space2[z - 1][x][y] != str(id)
                ):
                    is_stuck = True
                    new_blocks.clear()
                    break
            if not is_stuck:
                bricks_changed.add(id)
                for x, y, z in blocks:
                    space2[z][x][y] = "-"
                for x, y, z in new_blocks:
                    space2[z][x][y] = str(id)
                blocks = new_blocks
                brick_blocks2[id] = blocks
    return bricks_changed


def puzzle1(filename):
    t_start = timer()
    print_color(f"puzzle1: {filename}", Fore.MAGENTA)
    read_file(filename)
    res = solve(part=1)
    t_end = timer()
    print_color(f"Time elapsed (in seconds): {t_end - t_start}", Fore.MAGENTA)
    return res


def puzzle2(filename):
    t_start = timer()
    print_color(f"puzzle2: {filename}", Fore.MAGENTA)
    read_file(filename, part=2)
    res = solve(part=2)
    t_end = timer()
    print(f"Time elapsed (in seconds): {t_end - t_start}")
    return res


# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    init()
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print_color(f"Start Time = {current_time}", Fore.YELLOW)

    assert puzzle1("../../puzzles/2023/22/example.txt") == 5

    puzzle1_res = puzzle1("../../puzzles/2023/22/input.txt")
    assert puzzle1_res < 519  # your answer is too high
    assert puzzle1_res == 448  # correct

    assert puzzle2("../../puzzles/2023/22/example.txt") == 7
    puzzle2_res = puzzle2("../../puzzles/2023/22/input.txt")
    assert puzzle2_res > 1919  # your answer is too low
    assert puzzle2_res == 57770  # correct

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print_color(f"End Time = {current_time}", Fore.YELLOW)
