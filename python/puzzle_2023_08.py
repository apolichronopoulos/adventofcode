keys = []
values = []
mapping = {
    "A": 13,
    "K": 12,
    "Q": 11,
    "J": 10,
    "T": 9,
    "9": 8,
    "8": 7,
    "7": 6,
    "6": 5,
    "5": 4,
    "4": 3,
    "3": 2,
    "2": 1
}


def read_file(filename, part=1):
    keys.clear()
    values.clear()
    f = open(filename, "r")

    if part == 2:
        print("part 2")

    for line in f:
        line = line.strip()
        if line == "":
            continue
        x = line.split()
        key = x[0]
        value = x[1]
        keys.append(key)
        values.append(value)


def solve(part=1):
    results = []
    for i in range(0, len(keys)):
        key = keys[i]

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
    solve()


def puzzle2(filename):
    read_file(filename, 2)
    solve(2)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    puzzle1('../puzzles/2023/08/example.txt')  # result -> ??
    # puzzle1('../puzzles/2023/08/input.txt')  # result -> ??
    # puzzle2('../puzzles/2023/08/example.txt')  # result -> ??
    # puzzle2('../puzzles/2023/08/input.txt')  # result -> ??
