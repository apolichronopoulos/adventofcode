seeds = []  #
seed_mapping = {}  # key -> list (destination, source, range)
mapping = {}  # key -> list (destination, source, range)

steps = [
    "seed-to-soil",
    "soil-to-fertilizer",
    "fertilizer-to-water",
    "water-to-light",
    "light-to-temperature",
    "temperature-to-humidity",
    "humidity-to-location",
]


def read_file(filename):
    f = open(filename, "r")
    map_key = ""
    key_list = []
    for line in f:
        line = line.strip()
        # print(line)
        if line == "":
            continue
        if line.startswith("seeds:"):
            x = line.split()
            seeds.extend(x[1:len(x):1])
            continue
        if "map:" in line:
            if map_key != "":
                seed_mapping[map_key] = key_list
            map_key = line.split()[0]
            key_list = []
            continue
        x = line.split()
        destination = x[0]
        source = x[1]
        range = x[2]
        key_list.append([destination, source, range])
    if key_list:
        seed_mapping[map_key] = key_list


def puzzle1(filename):
    read_file(filename)
    # print(f"{seeds}")
    # print(f"{seed_mapping}")
    for key in seed_mapping:
        map = {}
        for record in seed_mapping[key]:
            d = int(record[0])
            s = int(record[1])
            r = int(record[2])
            for i in range(0, r):
                # print(f"{d} {s} {r}")
                map[s + i] = d + i
        mapping[key] = map

    res = []
    for seed in seeds:
        k = int(seed)
        error = False
        for step in steps:
            if k in mapping[step]:
                k = (mapping[step])[k]
            if not k:
                error = True
                break
        if not error:
            res.append(int(k))

    print(f"min seed: {min(res)}")


def puzzle2(filename):
    f = open(filename, "r")
    data = {}
    cards = []
    cards_to_check = []
    for line in f:
        print(line)
        x = line.split(":")
        card = x[0].strip().split()[1]
        parts = x[1].strip().split("|")
        winning = parts[0].strip().split()
        played = parts[1].strip().split()
        won = []
        for number in played:
            if number in winning:
                won.append(number)
        data[card] = won
        cards_to_check.append(card)

    # iterations = 0
    while len(cards_to_check) > 0:
        # iterations += 1
        # print(f"iteration: {iterations}")
        # print(f"cards_to_check: {len(cards_to_check)} / cards: {len(cards)} / sum: {len(cards_to_check) + len(cards)}")
        check = len(cards_to_check) - 1  # works
        # check = 0 # doesnt work - in proper time
        card = cards_to_check[check]
        cards.append(card)
        del cards_to_check[check]
        if card in data:
            won = len(data[card])
            for card2add in range(int(card) + 1, int(card) + won + 1):
                if card2add <= len(data):
                    cards_to_check.append(str(card2add))

    print(f"result: {sorted(cards)}")
    print(f"result: {len(cards)}")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # puzzle1('../puzzles/2023/05/example.txt')  # result -> 13
    puzzle1('../puzzles/2023/05/input.txt')  # result -> 2169
    # puzzle2('../puzzles/2023/05/example.txt')  # result -> 30
    # puzzle2('../puzzles/2023/05/input.txt')  # correct -> 5744979
