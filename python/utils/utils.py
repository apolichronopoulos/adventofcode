from colorama import Fore, Back


def read_file(filename, separator=""):
    elements = []
    f = open(filename, "r")
    for line in f:
        elements_i = []
        if line == "":
            continue
        if separator == "":
            line = line.strip()
        else:
            line = line.split(separator)
        for c in line:
            elements_i.append(c)
        elements.append(elements_i)

    return elements


def print_index(index=[], counts=[], results=[], ending=" ", color=Fore.RESET):
    set_print_color(color=color)
    for i in range(0, len(index)):
        for j in range(0, len(index[i])):
            c = index[i][j]
            if [i, j] in counts:
                print_color(c, color=Fore.RED, ending=ending)
            elif [i, j] in results:
                print_color('#', color=Fore.MAGENTA, ending=ending)
            elif results:
                print_color('.', color=color, ending=ending)
            else:
                print_color(c, color=color, ending=ending)
        print(""),
    reset_print_color()


def get_combinations(my_list):  # creating a user-defined method
    my_result = []
    for i in range(0, len(my_list)):
        for j in range(i, len(my_list)):
            if i != j:
                my_result.append((my_list[i], my_list[j]))
    return my_result


def split_into_tokens(s, token_size):
    return [s[i:i + token_size] for i in range(0, len(s), token_size)]


def replace_char(s, c, i):
    return s[:i] + c + s[i + 1:]


def print_color(s, color=Fore.RED, background=Back.RESET, ending="\n"):
    print(color + background + s + Fore.RESET + Back.RESET, end=ending)


def set_print_color(color=Fore.RED, background=Back.RESET):
    print(color + background, end="")


def reset_print_color():
    print(Fore.RESET + Back.RESET, end="")


def flip_and_rotate_grid(grid, index=1):
    num_cols = len(grid[0])
    rotated = num_cols * ['']
    for i, row in enumerate(grid):
        for j, c in enumerate(row):
            rotated[j] += c
    grid.clear()
    grid.extend(rotated)
    if index == 0:
        return grid
    else:
        return rotate_grid(grid, index - 1)


# Clockwise rotation
def rotate_grid(grid, index=1):
    num_cols = len(grid[0])
    rotated = num_cols * ['']
    for i, row in enumerate(grid):
        for j, c in enumerate(row):
            rotated[j] = c + rotated[j]
    grid.clear()
    grid.extend(rotated)
    if index == 0:
        return grid
    else:
        return rotate_grid(grid, index - 1)


def find_neighbors(x, y, tiles):
    all_cases = [[x, y + 1], [x - 1, y], [x + 1, y], [x, y - 1]]
    cases = []
    for case in all_cases:
        if case[0] < 0 or case[1] < 0 or case[0] >= len(tiles) or case[1] >= len(tiles[0]):
            continue
        cases.append(case)
    return cases
