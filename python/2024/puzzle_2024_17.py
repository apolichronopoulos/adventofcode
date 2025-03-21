# -*- coding: utf-8 -*-
import math
import sys

from utils.utils import aoc_submit, file, puzzle, time_and_color

sys.setrecursionlimit(20000)

registers = []
opcodes = []
results = []
intr_pointer = 0


def read_file(filename, separator=":"):
    f = open(filename, "r")
    registers.clear()
    opcodes.clear()
    results.clear()
    global intr_pointer
    intr_pointer = 0
    for line in f:
        line = line.strip()
        if line == "":
            continue
        side1, side2 = line.split(separator)
        if "register" in side1.lower():
            registers.append(int(side2))
        else:
            opcodes.extend([int(x) for x in side2.split(",")])


def combo(operand):
    if operand in [0, 1, 2, 3]:
        return operand
    elif operand in [4, 5, 6]:
        return registers[operand - 4]
    else:
        raise "invalid operand"


def calculate(opcode, operand):
    global intr_pointer
    res = 0
    if opcode == 0:
        res = int(registers[0] / math.pow(2, combo(operand)))
        registers[0] = res
    elif opcode == 1:
        res = registers[1] ^ operand  # bitwise XOR
        registers[1] = res
    elif opcode == 2:
        res = combo(operand) % 8
        res = format(res, "b")
        res = int(res[-3:], 2)
        registers[1] = res
    elif opcode == 3:
        res = 0
        if registers[0] != 0:
            intr_pointer = operand
            return res
    elif opcode == 4:
        res = registers[1] ^ registers[2]  # bitwise XOR
        registers[1] = res
    elif opcode == 5:
        res = combo(operand) % 8
        results.append(res)
    elif opcode == 6:
        res = int(registers[0] / math.pow(2, combo(operand)))
        registers[1] = res
    elif opcode == 7:
        res = int(registers[0] / math.pow(2, combo(operand)))
        registers[2] = res

    intr_pointer += 2
    return res


def run_program(a, b, c, expected=[]):
    results.clear()
    registers.clear()
    registers.extend([a, b, c])
    global intr_pointer
    intr_pointer = 0
    while intr_pointer < len(opcodes) - 1:
        opcode, operand = opcodes[intr_pointer], opcodes[intr_pointer + 1]
        calculate(opcode, operand)
    return ",".join([str(r) for r in results])


def solve(part=1):
    global intr_pointer
    a, b, c = registers
    res = run_program(a, b, c)
    if part == 1:
        return res

    expected_output = [s for s in opcodes]
    found_bits = 0
    solutions = [0]

    lshr_operand = 3
    check_range = 2**lshr_operand

    while found_bits != len(expected_output):
        target = expected_output[-found_bits - 1 :]
        if len(solutions) == 0:
            return None
        all_n = [s for s in solutions]
        solutions.clear()
        for x in range(check_range):
            for n in all_n:
                a = x + (n * check_range)
                res = run_program(a, 0, 0)
                if res == ",".join([str(r) for r in target]):
                    if debug:
                        print(f"A={a} --> {res}")
                    solutions.append(a)
        if len(solutions) > 0:
            found_bits += 1

    return min(solutions)


if __name__ == "__main__":
    time_and_color(start=True)
    debug = False
    submit = False  # be careful

    assert (
        puzzle(file("/2024/17/example.txt"), read_file, solve, 1)
        == "4,6,3,5,6,3,5,2,1,0"
    )
    answer1 = puzzle(file("/2024/17/input.txt"), read_file, solve, 1)
    assert answer1 == "6,7,5,2,1,3,5,1,7"
    if submit:
        aoc_submit("2024", "17", 1, answer1)

    assert puzzle(file("/2024/17/example2.txt"), read_file, solve, 2) == 117440
    answer2 = puzzle(file("/2024/17/input.txt"), read_file, solve, 2)
    assert answer2 == 216549846240877
    if submit:
        aoc_submit("2024", "17", 2, answer2)

    time_and_color(start=False)
