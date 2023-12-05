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
        # print(line)
        if line == "":
            continue
        if line.startswith("seeds:"):
            x = line.split()
            seeds.extend(x[1:len(x):1])
            continue
        if "map:" in line:
            if map_key != "":
                seed_mapping[map_key] = key_list
            map_key = line.split()[0]
            key_list = []
            continue
        x = line.split()
        destination = x[0]
        source = x[1]
        range = x[2]
        key_list.append([destination, source, range])
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


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    puzzle1('../puzzles/2023/05/example.txt')  # result -> 35
    puzzle1('../puzzles/2023/05/input.txt')  # result -> 289863851
    # puzzle2('../puzzles/2023/05/example.txt')  # result ->
    # puzzle2('../puzzles/2023/05/input.txt')  # correct ->
