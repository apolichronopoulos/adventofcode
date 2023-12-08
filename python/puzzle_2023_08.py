from timeit import default_timer as timer

steps = []
nodes = {}
guide = {
    "L": 0,
    "R": 1,
}


def read_file(filename, part=1):
    steps.clear()
    nodes.clear()
    f = open(filename, "r")

    index = 0
    for line in f:
        line = line.strip()
        if line == "":
            continue
        if index == 0:
            steps.extend([*line])
        else:
            x = line.split("=")
            key = x[0].strip()
            value = x[1].strip()
            value = value[1:len(value) - 1].split(",")
            l = value[0].strip()
            r = value[1].strip()
            nodes[key] = [l, r]
        index += 1


def solve(part=1):
    start = "AAA"
    end = "ZZZ"
    step_count = 0

    positions = [start]
    if part == 2:
        start = 'A'
        end = 'Z'
        positions.clear()
        for node in nodes:
            if node.endswith('A'):
                positions.append(node)

    iterations = 0
    finished = False
    loop = []
    while not finished:
        print(f"iterations: {iterations}")
        iterations += 1

        for step in steps:
            if finished:
                break
            g = guide[step]
            step_count += 1
            # print(f"count: {step_count}, going {step}")
            # print(f"positions: {positions}")

            # x = "".join(positions)
            # if x in loop:
            #     print(f"loop in {x}")
            #     exit(1)
            # loop.append(x)

            z = 0
            for i in range(0, len(positions)):
                positions[i] = (nodes[positions[i]])[g]
                if positions[i].endswith(end):
                    z += 1

            # if z > 0:
            #     print(f"{step_count} ending with z: {z}/{len(positions)}")
            #     print(f"{positions}")

            if z == len(positions):
                finished = True
                break

    res = step_count
    print(f"res: {res}")


def puzzle1(filename):
    start = timer()
    print(f"\n\npuzzle1: {filename}")
    read_file(filename)
    # print(steps)
    # print(nodes)
    # print(guide)
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
    # puzzle1('../puzzles/2023/08/example.txt')  # result -> 6
    # puzzle1('../puzzles/2023/08/input.txt')  # result -> 19637
    # puzzle2('../puzzles/2023/08/example2.txt')  # result -> 6
    puzzle2('../puzzles/2023/08/input.txt')  # result -> ??
