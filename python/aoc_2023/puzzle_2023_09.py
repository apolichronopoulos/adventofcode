from datetime import datetime
from timeit import default_timer as timer

elements = []
max_size = 0


def read_file(filename, part=1):
    global max_size
    elements.clear()
    f = open(filename, "r")
    for line in f:
        line = line.strip()
        if line == "":
            continue
        x = line.split()
        for i in range(0, len(x)):
            x[i] = int(x[i])
        elements.append(x)
        if len(x) > max_size:
            max_size = len(x)


def solve(part=1):
    res = 0
    for i in range(0, len(elements)):
        history = []
        history.append(elements[i])
        line = 0
        while True:
            current_line = history[line]
            if current_line.count(0) == len(current_line):
                break
            next_line = []
            for j in range(0, len(current_line) - 1):
                dif = current_line[j + 1] - current_line[j]
                next_line.append(dif)
            history.append(next_line)
            line += 1

        if part == 2:
            while len(history[0]) < max_size + 1:
                current_size = len(history)
                num = 0
                for x in range(current_size - 1, -1, -1):
                    num = history[x][0] - num
                    new_line = [num]
                    new_line.extend(history[x])
                    history[x] = new_line
        else:
            while len(history[0]) < max_size + 1:
                current_size = len(history)
                num = 0
                for x in range(current_size - 1, -1, -1):
                    num += history[x][len(history[x]) - 1]
                    history[x].append(num)

        print(history)
        res += num

    print(f"res: {res}")


def puzzle1(filename):
    start = timer()
    print(f"\n\npuzzle1: {filename}")
    read_file(filename)
    solve()
    end = timer()
    print(f"Time elapsed (in seconds): {end - start}")


def puzzle2(filename):
    start = timer()
    print(f"\n\npuzzle2: {filename}")
    read_file(filename, 2)
    solve(2)
    end = timer()
    print(f"Time elapsed (in seconds): {end - start}")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Start Time =", current_time)
    # puzzle1('../puzzles/2023/09/example.txt')  # result -> 114
    # puzzle1('../puzzles/2023/09/input.txt')  # result -> 1584748274
    # puzzle2('../puzzles/2023/09/example.txt')  # result -> 2
    puzzle2('../../puzzles/2023/09/input.txt')  # result -> 1026

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("End Time =", current_time)
