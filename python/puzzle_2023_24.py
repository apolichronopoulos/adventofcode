import sys
from datetime import datetime
from timeit import default_timer as timer

from colorama import Fore, Back, init
from shapely.geometry import LineString

from utils.utils import print_color, print_index

print(sys.getrecursionlimit())
sys.setrecursionlimit(10000)

hails = {}
hails_p = []
hails_v = []

tiles = []
matrix = []


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
    global start
    print_index(matrix, color=Fore.CYAN, ending="")

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

            # plt.close()
            # li1 = [(points1[0]), (points1[1])]
            # plt.plot(*zip(*li1), label=f"{key} line 1")
            # li2 = [(points2[0]), (points2[1])]
            # plt.plot(*zip(*li2), label=f"{key} line 2")
            # plt.show()

            if not line1.intersects(line2):
                checked[key] = False
                continue

            int_pt = line1.intersection(line2)

            if minP <= int_pt.x <= maxP and minP <= int_pt.y <= maxP:
                checked[key] = True
                res += 1
                # point_of_intersection = int_pt.x, int_pt.y
                # print(point_of_intersection)
            else:
                checked[key] = False

    print_color(f"---------> final result: {res} <---------", Fore.LIGHTRED_EX, Back.LIGHTYELLOW_EX)
    return res


def solve2(part=2, minP: int = 7, maxP: int = 24):
    global start
    print_index(matrix, color=Fore.CYAN, ending="")

    res = 0
    points = []
    lines = []
    for k, hail in hails.items():
        px, py, pz = hail[0]
        vx, vy, vz = hail[1]
        p1 = (calculate_pos(px, py, vx, vy, 0))
        p2 = (calculate_pos(px, py, vx, vy, maxP))
        points.append([p1, p2])
        lines.append(LineString([p1, p2]))

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

            # plt.close()
            # li1 = [(points1[0]), (points1[1])]
            # plt.plot(*zip(*li1), label=f"{key} line 1")
            # li2 = [(points2[0]), (points2[1])]
            # plt.plot(*zip(*li2), label=f"{key} line 2")
            # plt.show()

            if not line1.intersects(line2):
                checked[key] = False
                continue

            int_pt = line1.intersection(line2)
            point_of_intersection = int_pt.x, int_pt.y
            print(point_of_intersection)

            if minP <= int_pt.x <= maxP and minP <= int_pt.y <= maxP:
                checked[key] = True
                res += 1  # todo check area?
            else:
                checked[key] = False

    print_color(f"---------> final result: {res} <---------", Fore.LIGHTRED_EX, Back.LIGHTYELLOW_EX)
    return res


def puzzle1(filename, minP: int = 7, maxP: int = 24):
    t_start = timer()
    print_color(f"puzzle1: {filename}", Fore.MAGENTA)
    read_file(filename)
    res = solve(part=1, minP=minP, maxP=maxP)
    t_end = timer()
    print_color(f"Time elapsed (in seconds): {t_end - t_start}", Fore.MAGENTA)
    return res


def puzzle2(filename, minP: int = 7, maxP: int = 24):
    t_start = timer()
    print_color(f"puzzle2: {filename}", Fore.MAGENTA)
    read_file(filename, part=2)
    res = solve2(part=2, minP=minP, maxP=maxP)
    t_end = timer()
    print(f"Time elapsed (in seconds): {t_end - t_start}")
    return res


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    init()
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print_color(f"Start Time = {current_time}", Fore.YELLOW)

    assert puzzle1('../puzzles/2023/24/example.txt', minP=7, maxP=24) == 2
    assert puzzle1('../puzzles/2023/24/input.txt', 200000000000000, 400000000000000) == 21843

    # assert puzzle2('../puzzles/2023/24/example.txt') == -1
    # assert puzzle2('../puzzles/2023/24/input.txt') == -1  # won't run

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print_color(f"End Time = {current_time}", Fore.YELLOW)
