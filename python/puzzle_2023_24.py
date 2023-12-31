import sys
import threading
from datetime import datetime
from timeit import default_timer as timer

from colorama import Fore, Back, init
from shapely.geometry import LineString

from utils.utils import print_color

print(sys.getrecursionlimit())
sys.setrecursionlimit(10000)

hails = {}
min_x, min_y, min_z = sys.maxsize, sys.maxsize, sys.maxsize
max_x, max_y, max_z = - sys.maxsize, - sys.maxsize, - sys.maxsize


def read_file(filename, part=1):
    hails.clear()
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

        global max_x, max_y, max_z
        max_x = max(px, max_x)
        max_y = max(py, max_y)
        max_z = max(pz, max_z)
        min_x = min(px, max_x)
        min_y = min(py, max_y)
        min_z = min(pz, max_z)
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


def calc_possible_v0s(i, possible_v0s, max_v, max_n, all_v):
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
        return 0
    print_color(f'found solution for axis {i} for max_n={max_n} / max_v={max_v}', Fore.YELLOW)

    all_v[i] = possible_v0s


# def worker():
#     print("Worker thread running")


def solve2(part=2, max_v: int = 5000, max_n: int = 5000):
    print_color(f'running for max_n={max_n} / max_v={max_v}', Fore.YELLOW)

    # max_xyz = max(max_x, max_y, max_z)
    # min_xyz = max(min_x, min_y, min_z)

    all_v = {}

    t1 = threading.Thread(target=calc_possible_v0s, args=(0, {}, max_v, max_n, all_v))
    t2 = threading.Thread(target=calc_possible_v0s, args=(1, {}, max_v, max_n, all_v))
    t3 = threading.Thread(target=calc_possible_v0s, args=(2, {}, max_v, max_n, all_v))

    t1.start()
    t2.start()
    t3.start()

    t1.join()
    t2.join()
    t3.join()

    if len(all_v) != 3:
        print_color(f'max_n={max_n} / max_v={max_v} is too low', Fore.RED)
        return 0

    print(f'found some solutions, calculating best case')

    start_p = [0, 0, 0]
    # start_v = [0, 0, 0]

    possible_v0s = []
    for i in range(3):
        solutions = all_v[i]
        possible_v0s.append([])
        for v, p0s in solutions.items():
            possible_v0s[i].append(v)

    found_solution = False
    for vx0 in possible_v0s[0]:
        for vy0 in possible_v0s[1]:
            for vz0 in possible_v0s[2]:
                # start_v = [vx0, vy0, vz0]
                for px0 in all_v[0][vx0]:
                    for py0 in all_v[1][vy0]:
                        for pz0 in all_v[2][vz0]:
                            if found_solution:
                                break
                            is_valid = True
                            for k, hail in hails.items():
                                px, py, pz = hail[0]
                                vx, vy, vz = hail[1]
                                nx = (px0 - px) / (vx - vx0) if vx != vx0 else (px0 - px)
                                ny = (py0 - py) / (vy - vy0) if vy != vy0 else (py0 - py)
                                nz = (pz0 - pz) / (vz - vz0) if vz != vz0 else (pz0 - pz)
                                # p0 -> 24, 13, 10
                                # v0 -> -3, 1, 2
                                nx = max(nx, ny, nz) if nx == 0 else nx
                                ny = max(nx, ny, nz) if ny == 0 else ny
                                nz = max(nx, ny, nz) if nz == 0 else nz
                                if not (nx == ny == nz):
                                    is_valid = False
                                    break
                            if is_valid:
                                found_solution = True
                                start_p = [px0, py0, pz0]
                                break

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

    # assert puzzle2('../puzzles/2023/24/example.txt', 100, 100) == 47
    # assert puzzle2('../puzzles/2023/24/example.txt', 500, 500) == 47
    # assert puzzle2('../puzzles/2023/24/example.txt', 10000, 10000) == 47

    # puzzle2_res = puzzle2('../puzzles/2023/24/input.txt', 100, 100)
    puzzle2_res = puzzle2('../puzzles/2023/24/input.txt', 500, 500)
    # puzzle2_res = puzzle2('../puzzles/2023/24/input.txt', 500, 5000)
    # puzzle2_res = puzzle2('../puzzles/2023/24/input.txt', 10000, 10000)
    # assert puzzle2_res != -1
    # assert puzzle2_res != 0
    # assert puzzle2_res != 27670116110564327421

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print_color(f"End Time = {current_time}", Fore.YELLOW)
