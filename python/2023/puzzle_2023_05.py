# -*- coding: utf-8 -*-
seeds = []  #
seed_mapping = {}  # key -> list (destination, source, range)
mapping = {}  # key -> list (destination, source, range)

steps = [
    "seed-to-soil",
    "soil-to-fertilizer",
    "fertilizer-to-water",
    "water-to-light",
    "light-to-temperature",
    "temperature-to-humidity",
    "humidity-to-location",
]


def read_file(filename):
    f = open(filename, "r")
    map_key = ""
    key_list = []
    for line in f:
        line = line.strip()
        if line == "":
            continue
        if line.startswith("seeds:"):
            x = line.split()
            seeds.extend(x[1 : len(x) : 1])
            continue
        if "map:" in line:
            if map_key != "":
                seed_mapping[map_key] = key_list
            map_key = line.split()[0]
            key_list = []
            continue
        x = line.split()
        d = x[0]
        s = x[1]
        r = x[2]
        key_list.append([d, s, r])
    if key_list:
        seed_mapping[map_key] = key_list


def puzzle1(filename):
    read_file(filename)
    print(f"{seeds}")
    print(f"{seed_mapping}")

    res = []
    for seed in seeds:
        k = int(seed)
        error = False
        print(f"seed: {seed}")
        for step in steps:
            for record in seed_mapping[step]:
                d = int(record[0])
                s = int(record[1])
                r = int(record[2])
                if k in range(s, s + r + 1):
                    x = k - s
                    k = d + x
                    break
        if not error:
            res.append(int(k))

        print(f"{step}: {k}")

    print(f"min seed: {min(res)}")


def puzzle2(filename):
    read_file(filename)
    print(f"{seeds}")

    min_res = 0
    for i in range(0, len(seeds), 2):
        seed = int(seeds[i])
        s_min = seed
        s_max = s_min + int(seeds[i + 1]) - 1
        seed_list = [[s_min, s_max]]
        for step in steps:
            print(f"seed_list: {seed_list}")
            print(f"i: {i} seed: {seed}, step: {step}")
            seed_list_step = []
            while seed_list:
                m = seed_list[len(seed_list) - 1]
                del seed_list[len(seed_list) - 1]
                s1_min = m[0]
                s1_max = m[1]
                found = False
                for record in seed_mapping[step]:
                    d = int(record[0])
                    s = int(record[1])
                    r = int(record[2])
                    s2_min = s
                    s2_max = s + r - 1

                    d2_min = d
                    d2_max = d + r - 1

                    overlap_min = max(s1_min, s2_min)
                    overlap_max = min(s1_max, s2_max)
                    if overlap_min <= overlap_max:
                        dif_min = max(0, s1_min - s2_min)
                        dif_max = s2_max - s1_max
                        d_min = d2_min + dif_min
                        d_max = min(d2_max, d2_max - dif_max)
                        seed_list_step.append([d_min, d_max])
                        if s1_min < s2_min:
                            seed_list.append([s1_min, s2_min - 1])
                        if s1_max > s2_max:
                            seed_list.append([s2_max + 1, s1_max])
                        found = True
                        print(
                            f"s1 ({s1_min}, {s1_max}) with s2 ({s2_min}, {s2_max}) with dest ({d},{d + r - 1}) -> ({d_min}, {d_max})"
                        )
                if not found:
                    print(f"not found {s1_min, s1_max}")
                    seed_list_step.append([s1_min, s1_max])

            seed_list = seed_list_step

        print(f"seed_list: {seed_list}")
        for item in seed_list:
            if min_res == 0 or min_res > item[0]:
                min_res = item[0]

    print(f"min seed: {min_res}")


if __name__ == "__main__":
    # puzzle1('../../puzzles/2023/05/example.txt')  # result -> 35
    # puzzle1('../../puzzles/2023/05/input.txt')  # result -> 289863851
    # puzzle2('../../puzzles/2023/05/example.txt')  # result -> 46 # same brute force works, not for input.txt though
    # puzzle2('../../puzzles/2023/05/input.txt')  # correct -> 63092906 too high
    puzzle2("../../puzzles/2023/05/input.txt")  # correct -> 60568880 correct
