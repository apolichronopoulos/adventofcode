import sys
from datetime import datetime
from timeit import default_timer as timer

from colorama import Fore, Back, init
from shapely.geometry import LineString

from utils.utils import print_color

print(sys.getrecursionlimit())
sys.setrecursionlimit(10000)

hails = {}
hails_p = []
hails_v = []


def read_file(filename, part=1):
    hails.clear()
    hails_p.clear()
    hails_v.clear()
    f = open(filename, "r")
    for i, line in enumerate(f):
        line = line.strip()
        if line == "":
            continue
        position, velocity = line.split('@')
        px, py, pz = position.strip().split(',')
        px, py, pz = int(px), int(py), int(pz)
        hails_p.append((px, py, pz))
        vx, vy, vz = velocity.strip().split(',')
        vx, vy, vz = int(vx), int(vy), int(vz)
        hails_v.append((vx, vy, vz))
        hails[str(i)] = ([(px, py, pz), (vx, vy, vz)])


def calculate_pos(px, py, vx, vy, n):
    return px + vx * n, py + vy * n


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


def solve2(part=2, max_v: int = 5000, max_n: int = 5000):
    print_color(f'running for max_n={max_n} / max_v={max_v}', Fore.YELLOW)

    all_v = {}

    for i in range(3):
        possible_v0s = {}
        print_color(f'running for axis -> {i}', Fore.RED)
        for v0 in range(-max_v, max_v + 1):
            if v0 == 0:
                continue
            p0s = {}
            for k, hail in hails.items():
                pi = hail[0][i]
                vi = hail[1][i]
                p0s[k] = []
                for n in range(1, max_n + 1):
                    p0 = (pi + vi * n) - (v0 * n)
                    p0s[k].append(p0)
            com_el = None
            for k, v in p0s.items():
                if com_el is None:
                    com_el = set(v)
                else:
                    com_el = common_elements(com_el, v)
                    if not com_el:
                        break
            if com_el:
                possible_v0s[v0] = com_el

        if not possible_v0s:
            print_color(f'max_n={max_n} / max_v={max_v} is too low for axis {i}', Fore.RED)
            exit(1)
        all_v[i] = possible_v0s

    print(f'found some solutions, calculating best case')

    start_p = [0, 0, 0]
    start_v = [0, 0, 0]
    for i, solutions in all_v.items():
        v0 = sys.maxsize
        p0 = sys.maxsize
        for v, p0s in solutions.items():
            if len(solutions) == 1 or (0 < v < v0):
                v0 = v
                p0 = p0s[0]
        start_v[i] = v0
        start_p[i] = p0

    start = (start_p[0], start_p[1], start_p[2])

    res = start[0] + start[1] + start[2]
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


def puzzle2(filename, max_v: int = 5000, max_n: int = 5000):
    t_start = timer()
    print_color(f"puzzle2: {filename}", Fore.MAGENTA)
    read_file(filename, part=2)
    res = solve2(part=2, max_v=max_v, max_n=max_n)
    t_end = timer()
    print(f"Time elapsed (in seconds): {t_end - t_start}")
    return res


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    init()
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print_color(f"Start Time = {current_time}", Fore.YELLOW)

    # assert puzzle1('../puzzles/2023/24/example.txt', minP=7, maxP=24) == 2
    # assert puzzle1('../puzzles/2023/24/input.txt', 200000000000000, 400000000000000) == 21843

    assert puzzle2('../puzzles/2023/24/example.txt', 100, 100) == 47
    # assert puzzle2('../puzzles/2023/24/example.txt', 500, 500) == 47

    # puzzle2_res = puzzle2('../puzzles/2023/24/input.txt', 5000, 5000)
    # assert puzzle2_res != -1  # won't run
    # assert puzzle2_res != 27670116110564327421  # won't run

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print_color(f"End Time = {current_time}", Fore.YELLOW)
