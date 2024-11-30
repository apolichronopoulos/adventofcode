def puzzle1(filename, max_colors):
    f = open(filename, "r")
    sum = 0
    for line in f:
        print(line)
        x = line.split(":")
        game = int(x[0].strip().split()[1])
        possible = True
        for round in x[1].split(";"):
            for color in round.split(","):
                n = int(color.strip().split()[0])
                c = color.strip().split()[1][0]
                if max_colors[c] < n:
                    possible = False
        if possible:
            sum += game

    print(f"result: {sum}")


def puzzle2(filename):
    f = open(filename, "r")
    sum = 0
    for line in f:
        print(line)
        x = line.split(":")
        max_colors = {'r': 0, 'g': 0, 'b': 0}
        for round in x[1].split(";"):
            for color in round.split(","):
                n = int(color.strip().split()[0])
                c = color.strip().split()[1][0]
                if max_colors[c] < n:
                    max_colors[c] = n
        power = max(max_colors['r'], 1) * max(max_colors['g'], 1) * max(max_colors['b'], 1)
        print(f"max_colors {max_colors}\n")
        print(f"power {power}\n")
        sum += power

    print(f"result: {sum}")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    puzzle1('../../puzzles/2023/02/example.txt', {'r': 12, 'g': 13, 'b': 14})  # result -> 8
    puzzle1('../../puzzles/2023/02/input.txt', {'r': 12, 'g': 13, 'b': 14})  # result -> 2169
    puzzle2('../../puzzles/2023/02/example.txt')  # result -> 2286
    puzzle2('../../puzzles/2023/02/input.txt')  # correct -> 60948
