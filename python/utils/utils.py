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


def print_index(index=[], ending=" "):
    for i in range(0, len(index)):
        for j in range(0, len(index[i])):
            c = index[i][j]
            print(c, end=ending)
        print(""),


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
