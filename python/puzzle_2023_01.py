def puzzle1(filename):
    f = open(filename, "r")
    sum = 0
    for line in f:
        t1 = ""
        t2 = ""
        print(line)
        for c in line:
            if c.isdigit():
                t2 = c
                if t1 == "":
                    t1 = c
        sum += int(t1 + t2)
    print(f"result: {sum}")


numbers = {
    "zero": "0",
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}


def puzzle2(filename):
    f = open(filename, "r")
    sum = 0
    for line in f:
        line = line.strip()
        s = len(line)
        t1 = ""
        t2 = ""
        i = 0
        for c in line:
            if c.isdigit():
                t2 = c
                if t1 == "":
                    t1 = c
            else:
                for number in numbers:
                    n = len(number)
                    if line[i:min(i + n, s)] == number:
                        t2 = numbers[number]
                        if t1 == "":
                            t1 = numbers[number]
            i += 1
        print(f"{line} -> {t1 + t2}")
        sum += int(t1 + t2)
    print(f"result: {sum}")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    puzzle1('../puzzles/2023/01/example.txt')
    puzzle1('../puzzles/2023/01/input.txt')
    puzzle2('../puzzles/2023/01/example2.txt')
    puzzle2('../puzzles/2023/01/input.txt')  # wrong 54886 too low
    puzzle2('../puzzles/2023/01/input.txt')  # will 56324 do? yeeey
