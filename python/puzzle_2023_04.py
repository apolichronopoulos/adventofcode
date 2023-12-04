def puzzle1(filename):
    f = open(filename, "r")
    sum = 0
    for line in f:
        print(line)
        x = line.split(":")
        card = int(x[0].strip().split()[1])
        parts = x[1].strip().split("|")
        winning = parts[0].strip().split()
        played = parts[1].strip().split()
        power = -1
        for number in played:
            if number in winning:
                power += 1
        if power >= 0:
            sum += pow(2, power)
    print(f"result: {sum}")


def puzzle2(filename):
    f = open(filename, "r")
    sum = 0
    for line in f:
        print(line)
        x = line.split(":")
        card = int(x[0].strip().split()[1])
        parts = x[1].strip().split("|")
        winning = parts[0].strip().split()
        played = parts[1].strip().split()
        power = -1
        for number in played:
            if number in winning:
                power += 1
        if power >= 0:
            sum += pow(2, power)
    print(f"result: {sum}")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    puzzle1('../puzzles/2023/04/example.txt')  # result -> 13
    puzzle1('../puzzles/2023/04/input.txt')  # result -> 2169
    # puzzle2('../puzzles/2023/04/example.txt')  # result -> 2286
    # puzzle2('../puzzles/2023/04/input.txt')  # correct -> 60948
