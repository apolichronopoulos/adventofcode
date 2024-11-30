import sys
from datetime import datetime
from functools import lru_cache
from timeit import default_timer as timer

import sympy as sp
from colorama import Fore, Back, init
from shapely.geometry import LineString

from utils.utils import print_color

print(sys.getrecursionlimit())
sys.setrecursionlimit(10000)

hails = {}

first_three_hailstones = []


def read_file(filename, part=1):
    hails.clear()
    first_three_hailstones.clear()
    f = open(filename, "r")
    for i, line in enumerate(f):
        line = line.strip()
        if line == "":
            continue
        position, velocity = line.split('@')
        px, py, pz = position.strip().split(',')
        px, py, pz = int(px), int(py), int(pz)
        vx, vy, vz = velocity.strip().split(',')
        vx, vy, vz = int(vx), int(vy), int(vz)

        if i < 3:
            nums = line.replace('@', ',').split(',')
            first_three_hailstones.append(tuple(map(int, nums)))

        hails[str(i)] = ([(px, py, pz), (vx, vy, vz)])


@lru_cache
def calculate_pos(px, py, vx, vy, n):
    return px + vx * n, py + vy * n


@lru_cache
def calculate_pos2(px, py, pz, vx, vy, vz, n):
    return px * vx * n, py + vy * n, pz + vz * n


def solve(part=1, minP: int = 7, maxP: int = 24):
    res = 0
    points = []
    for k, hail in hails.items():
        px, py, pz = hail[0]
        vx, vy, vz = hail[1]
        p1 = (calculate_pos(px, py, vx, vy, 0))
        p2 = (calculate_pos(px, py, vx, vy, maxP))
        points.append([p1, p2])

    checked = {}
    for k1, hail1 in hails.items():
        for k2, hail2 in hails.items():
            if k1 == k2:
                continue
            key = (k1, k2)
            if (k1, k2) in checked or (k2, k1) in checked:
                continue

            points1 = points[int(k1)]
            points2 = points[int(k2)]

            line1 = LineString(points1)
            line2 = LineString(points2)

            if not line1.intersects(line2):
                checked[key] = False
                continue

            int_pt = line1.intersection(line2)

            if minP <= int_pt.x <= maxP and minP <= int_pt.y <= maxP:
                checked[key] = True
                res += 1
            else:
                checked[key] = False

    print_color(f"---------> final result: {res} <---------", Fore.LIGHTRED_EX, Back.LIGHTYELLOW_EX)
    return res


def solve2(part=2):
    unknowns = sp.symbols('x0 y0 z0 vx vy vz t1 t2 t3')
    x0, y0, z0, vx, vy, vz, *time = unknowns
    equations = []  # build system of 9 equations with 9 unknowns
    for t, hail in zip(time, first_three_hailstones):
        equations.append(sp.Eq(x0 + t * vx, hail[0] + t * hail[3]))
        equations.append(sp.Eq(y0 + t * vy, hail[1] + t * hail[4]))
        equations.append(sp.Eq(z0 + t * vz, hail[2] + t * hail[5]))

    solution = sp.solve(equations, unknowns).pop()
    res = sum(solution[:3])
    print_color(f"---------> final result: {res} <---------", Fore.LIGHTRED_EX, Back.LIGHTYELLOW_EX)
    return res


def common_elements(list1, list2):
    return list(set(list1) & set(list2))


def puzzle1(filename, minP: int = 7, maxP: int = 24):
    t_start = timer()
    print_color(f"puzzle1: {filename}", Fore.MAGENTA)
    read_file(filename)
    res = solve(part=1, minP=minP, maxP=maxP)
    t_end = timer()
    print_color(f"Time elapsed (in seconds): {t_end - t_start}", Fore.MAGENTA)
    return res


def puzzle2(filename):
    t_start = timer()
    print_color(f"puzzle2: {filename}", Fore.MAGENTA)
    read_file(filename, part=2)
    res = solve2(part=2)
    t_end = timer()
    print(f"Time elapsed (in seconds): {t_end - t_start}")
    return res


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    init()
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print_color(f"Start Time = {current_time}", Fore.YELLOW)

    assert puzzle1('../../puzzles/2023/24/example.txt', minP=7, maxP=24) == 2
    assert puzzle1('../../puzzles/2023/24/input.txt', 200000000000000, 400000000000000) == 21843

    assert puzzle2('../../puzzles/2023/24/example.txt') == 47

    puzzle2_res = puzzle2('../../puzzles/2023/24/input.txt')
    assert puzzle2_res != -1
    assert puzzle2_res != 0
    assert puzzle2_res != 27670116110564327421
    assert puzzle2_res == 540355811503157

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print_color(f"End Time = {current_time}", Fore.YELLOW)
