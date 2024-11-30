from functools import lru_cache


@lru_cache(maxsize=None)
def generate_combinations(s, index, current_combination):
    if index == len(s):
        return current_combination

    if s[index] == '?':
        result_dot = generate_combinations(s, index + 1, current_combination + '.')
        result_hash = generate_combinations(s, index + 1, current_combination + '#')
        return result_dot + result_hash
    else:
        return generate_combinations(s, index + 1, current_combination + s[index])


# Example usage:
input_string = '??.####?.??#?#?.?.??'
original_size = len(input_string)
initial_combination = ''
result = generate_combinations(input_string, 0, initial_combination)
print(result)


def split_into_tokens(s, token_size):
    return [s[i:i + token_size] for i in range(0, len(s), token_size)]


# Example usage:
# input_string = '??.####?.??#?#?.?.??'
# token_size = 2
tokens = split_into_tokens(result, original_size)
print(tokens)


# chunks = list(filter(None, line.split(".")))
# has_qm = "?" in line

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


# Example usage:
input_string = '####.##.##.??.####?.??#?#?.?.??'
print(find_gears(input_string))
