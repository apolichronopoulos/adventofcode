from functools import lru_cache

from datetime import datetime
from functools import lru_cache
from timeit import default_timer as timer

from utils.utils import print_index, split_into_tokens, replace_char


@lru_cache(maxsize=None)
def find_gears(line):
    results = []
    chunks = list(filter(None, line.split(".")))
    for chunk in chunks:
        if '?' in chunk:
            return results
        else:
            results.append(str(len(chunk)))
    return results


@lru_cache(maxsize=None)
def generate_combinations2(s, index, current_combination):
    print(f"{current_combination}")
    global combinations, case_s
    if index == len(s):
        combinations.append(current_combination)
        return
    if s[index] == '?':
        generate_combinations2(s, index + 1, replace_char(current_combination, '.', index))
        generate_combinations2(s, index + 1, replace_char(current_combination, '#', index))
    else:
        cc = "".join(current_combination)

        fg1 = ",".join(find_gears(cc))
        if fg1 != '' and not case_s.startswith(fg1):
            return

        fg2 = ",".join(find_gears(cc[::-1])[::-1])
        if fg2 != '' and not case_s.endswith(fg2):
            return

        generate_combinations2(s, index + 1, current_combination)


# should produce 506250
input_string = "?###??????????###??????????###??????????###??????????###????????"
case = ['3', '2', '1', '3', '2', '1', '3', '2', '1', '3', '2', '1', '3', '2', '1']

# should produce 2500
# input_string = "????.######..#####.?????.######..#####.?????.######..#####.?????.######..#####.?????.######..#####."
# case = ['1', '6', '5', '1', '6', '5', '1', '6', '5', '1', '6', '5', '1', '6', '5']

# should produce 6
# input_string = "?#???.??#??#???#???."
# case = ['2', '10', '1']


# TODO: generate_combinations2
case_s = ",".join(case)
initial_combination = input_string
combinations = []
generate_combinations2(input_string, 0, initial_combination)
all_combinations = combinations

count = 0
for combination in all_combinations:
    if find_gears(combination) == case:
        count += 1
print(f"---------> result: {count} <---------")
