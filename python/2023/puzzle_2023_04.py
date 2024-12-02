# -*- coding: utf-8 -*-
def puzzle1(filename):
    f = open(filename, "r")
    res = 0
    for line in f:
        if debug:
            print(line)
        x = line.split(":")
        card = int(x[0].strip().split()[1])
        parts = x[1].strip().split("|")
        winning = parts[0].strip().split()
        played = parts[1].strip().split()
        power = -1
        for number in played:
            if number in winning:
                power += 1
        if power >= 0:
            res += pow(2, power)
    print(f"result: {res}")
    return res


def puzzle2(filename):
    f = open(filename, "r")
    data = {}
    cards = []
    cards_to_check = []
    for line in f:
        if debug:
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

    if debug:
        print(f"cards: {sorted(cards)}")
    print(f"result: {len(cards)}")
    res = len(cards)
    return res


if __name__ == "__main__":
    debug = False
    assert puzzle1("../../puzzles/2023/04/example.txt") == 13
    assert puzzle1("../../puzzles/2023/04/input.txt") == 27059
    assert puzzle2("../../puzzles/2023/04/example.txt") == 30
    assert puzzle2("../../puzzles/2023/04/input.txt") == 5744979
