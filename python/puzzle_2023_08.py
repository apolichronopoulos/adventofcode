step_list = []
map = {}
mapping = {
    "L": 0,
    "R": 1,
}


def read_file(filename, part=1):
    step_list.clear()
    map.clear()
    f = open(filename, "r")

    if part == 2:
        print("part 2")

    index = 0
    for line in f:
        line = line.strip()
        if line == "":
            continue
        if index == 0:
            step_list.extend([*line])
        else:
            x = line.split("=")
            key = x[0].strip()
            value = x[1].strip()
            value = value[1:len(value) - 1].split(",")
            l = value[0].strip()
            r = value[1].strip()
            map[key] = [l, r]
        index += 1


def solve(part=1):
    results = []
    for step in step_list:

        key = step_list[i]

        result = key

        if part == 2:
            print("part 2")

        results.append(result)

    res = 0
    for i in range(0, len(results)):
        res += 1

    print(f"res: {res}")


def puzzle1(filename):
    read_file(filename)
    print(step_list)
    print(map)
    print(mapping)
    # solve()


def puzzle2(filename):
    read_file(filename, 2)
    solve(2)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    puzzle1('../puzzles/2023/08/example.txt')  # result -> ??
    # puzzle1('../puzzles/2023/08/input.txt')  # result -> ??
    # puzzle2('../puzzles/2023/08/example.txt')  # result -> ??
    # puzzle2('../puzzles/2023/08/input.txt')  # result -> ??
