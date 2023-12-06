times = []  #
distances = []


def read_file(filename, part=1):
    f = open(filename, "r")
    for line in f:
        line = line.strip()
        print(line)
        if line == "":
            continue

        x = line.split()
        x = x[1:len(x):1]
        if part == 2:
            x = "".join(x)
            if line.startswith("Time:"):
                times.append(x)
            elif line.startswith("Distance:"):
                distances.append(x)
        else:
            if line.startswith("Time:"):
                times.extend(x)
            elif line.startswith("Distance:"):
                distances.extend(x)


def solve():
    print(f"{times}")
    print(f"{distances}")
    res = 1
    wins = []
    for i in range(0, len(times)):
        t = int(times[i])
        d = int(distances[i])
        results = []
        print(f"t: {t}, d: {d}")
        for h in range(0, t + 1):
            r = h * (t - h)
            if r > d:
                results.append(h)
                print(f"hold for {h} and you will travel for {r}")

        wins.append(len(results))

    print(f"wins: {wins}")
    for w in wins:
        res = res * w

    print(f"res: {res}")


def puzzle1(filename):
    read_file(filename)
    solve()


def puzzle2(filename):
    read_file(filename, 2)
    solve()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # puzzle1('../puzzles/2023/06/example.txt')  # result -> 288
    # puzzle1('../puzzles/2023/06/input.txt')  # result -> 608902
    # puzzle2('../puzzles/2023/06/example.txt')  # result -> 71503
    puzzle2('../puzzles/2023/06/input.txt')  # correct -> 46173809
