# -*- coding: utf-8 -*-
import sys
from datetime import datetime

import numpy as np
from pulp import LpMinimize, LpProblem, LpStatus, LpVariable, lpSum
from utils.utils import (
    aoc_submit,
    custom_args,
    file,
    puzzle,
    substring_between,
    time_and_color,
)

print(sys.getrecursionlimit())
sys.setrecursionlimit(10000)

lights = []
buttons = []
joltages = []


def read_file(filename, part=1):
    f = open(filename, "r")
    lights.clear()
    buttons.clear()
    joltages.clear()
    for i, line in enumerate(f):
        line = line.strip()
        if line == "":
            continue

        l = substring_between(line, "[", "]", False)
        lights.append([c for c in l])

        b = substring_between(line, "(", ")", True)
        temp_buttons = []
        for x in b.split():
            text = substring_between(x, "(", ")", False)
            temp_buttons.append([int(n) for n in text.split(",") if n])
        buttons.append(temp_buttons)

        j = substring_between(line, "{", "}", False)
        joltages.append([int(x) for x in j.split(",") if x])

        if debug:
            print("--------------")
            print(f"light: {l}")
            print(f"buttons: {b}")
            print(f"\t{temp_buttons}")
            print(f"joltages: {j}")
            print(f"\t{[int(x) for x in j.split(',') if x]}")


def solve(part=1):
    res = 0

    for i in range(0, len(lights)):
        light = lights[i]
        btns = buttons[i]
        jlts = joltages[i]
        if debug:
            print(
                f'{datetime.now().strftime("%H:%M:%S")}: Solving light {i}: {"".join(light)} with buttons {btns}'
            )

        if part == 1:
            temp = press_a_button(
                "".join(light), btns, ["".join(["." for x in light])], [], 0, []
            )
        else:
            temp = solve_joltages(light, btns, jlts)

        res += temp

        if debug:
            print(f'light {i} ({"".join(light)}) solved in {temp} presses')
            print(f"Total so far: {res}")

    return res


def solve_joltages(light, btns, jlts):
    # Note: it happens that this problem can be solved with linear programming.
    # Each button press adds 1 to the joltages of the counters it affects.
    # We want to find the minimum number of presses for each button such that
    # the resulting joltages match the target joltages.
    # Strangely enough, light state does not matter for this calculation.

    # Define a button-pressing matrix A
    A = np.array([[1 if i in b else 0 for b in btns] for i in range(len(jlts))])

    # Define the target joltages vector b
    b = np.array(jlts)

    # Set up the linear programming problem
    prob = LpProblem("CounterPressProblem", LpMinimize)

    # Define integer variables for the number of presses for each button
    x = [LpVariable(f"x{i}", lowBound=0, cat="Integer") for i in range(A.shape[1])]

    # Objective: Minimize the total number of button presses
    prob += lpSum(x), "TotalPresses"

    # Constraints: A * x = b
    for i in range(A.shape[0]):
        prob += (
            lpSum(A[i, j] * x[j] for j in range(A.shape[1])) == b[i],
            f"Counter{i}Constraint",
        )

    prob.solve()

    press_counts = [int(var.varValue) for var in x]

    return sum(press_counts)


def single_button_press(light, btn):
    new_state = [c for c in light]
    for p in btn:
        if p < 0 or p >= len(light):
            continue
        new_state[p] = "#" if new_state[p] == "." else "."
    return "".join(new_state)


def press_a_button(light, btns, states, last_clicks=[], clicks=0, previous_states=[]):
    new_states = []
    while len(states) > 0:
        state = states.pop(0)
        last_click = last_clicks.pop(0) if last_clicks else -1
        state_history = previous_states.pop(0) if previous_states else set()
        if light == state:
            return clicks
        state_history.add(state)
        for b in btns:
            if b == last_click:
                continue
            new_state = single_button_press(state, b)
            if new_state in state_history:
                continue
            new_states.append(new_state)
            last_clicks.append(b)
            previous_states.append(state_history)

    if len(new_states) == 0:
        raise Exception("No solution to this light found")

    return press_a_button(
        light, btns, new_states, last_clicks, clicks + 1, previous_states
    )


if __name__ == "__main__":
    time_and_color(start=True)
    submit, debug = custom_args().submit, custom_args().debug

    assert puzzle(file("/2025/10/example.txt"), read_file, solve, 1) == 7
    answer1 = puzzle(file("/2025/10/input.txt"), read_file, solve, 1)
    assert answer1 == 441

    if submit:
        aoc_submit("2025", "10", 1, answer1)

    assert puzzle(file("/2025/10/example.txt"), read_file, solve, 2) == 33
    answer2 = puzzle(file("/2025/10/input.txt"), read_file, solve, 2)
    assert answer2 == 18559

    if submit:
        aoc_submit("2025", "10", 2, answer2)

    time_and_color(start=False)
