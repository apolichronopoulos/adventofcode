from colorama import Fore, Back, Style, init
from termcolor import colored


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


def print_index(index=[], ending=" ", color=Fore.RESET):
    set_print_color(color=color)
    for i in range(0, len(index)):
        for j in range(0, len(index[i])):
            c = index[i][j]
            print(c, end=ending)
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
