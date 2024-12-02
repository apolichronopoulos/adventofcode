# -*- coding: utf-8 -*-
hands = []  #
bids = []  #
cards = {
    "A": 13,
    "K": 12,
    "Q": 11,
    "J": 10,
    "T": 9,
    "9": 8,
    "8": 7,
    "7": 6,
    "6": 5,
    "5": 4,
    "4": 3,
    "3": 2,
    "2": 1,
}


def read_file(filename, part=1):
    hands.clear()
    bids.clear()
    f = open(filename, "r")
    if part == 2:
        cards["J"] = 0
    for line in f:
        line = line.strip()
        if line == "":
            continue
        x = line.split()
        hand = x[0]
        bid = x[1]
        hands.append(hand)
        bids.append(bid)


def solve(part=1):
    results = []
    for i in range(0, len(hands)):
        hand = hands[i]

        singles = []
        pairs = []
        triads = []
        counts = {}

        for c in hand:
            singles.append(cards[c])
            count = 0
            if c in counts:
                count = counts[c]
            counts[c] = count + 1

        j = 0
        if part == 2 and "J" in counts:
            j = counts["J"]
            counts["J"] = 0

        vals = [0, 0, 0, 0, 0]
        for c in counts:
            count = counts[c]
            v = cards[c]
            if count == 2:
                pairs.append(v)
            if count == 3:
                triads.append(v)
            if v > vals[count - 1]:
                vals[count - 1] = v

        fullhouse = 1 if pairs and triads else 0
        has_pairs = 1 if len(pairs) >= 2 else 0

        t = 0  # singles
        if vals[5 - 1] > 0:
            t = 6  # 5kind
        elif vals[4 - 1] > 0:
            t = 5  # 4kind
        elif fullhouse > 0:
            t = 4  # full
        elif vals[3 - 1] > 0:
            t = 3  # 3kind
        elif has_pairs:
            t = 2  # pairs
        elif vals[2 - 1] > 0:
            t = 1  # pair

        if part == 2 and j > 0:
            if has_pairs or vals[3 - 1] > 0:
                t += j + 1
            elif vals[2 - 1] > 0:
                t += 1 + j + (1 if j // 2 else 0)
            else:
                t += j + (1 if j // 2 else 0) + (1 if j // 3 else 0)

        score = str(min(t, 6))

        for c in singles:
            score = score + str(c).zfill(2)

        result = {"hand": hands[i], "bid": bids[i], "score": int(score)}
        results.append(result)

    results = sorted(results, key=lambda x: x["score"])

    res = 0
    scores = {}
    duplicates = 0
    for i in range(0, len(results)):
        r = results[i]
        if r["score"] in scores:
            duplicates += 1
            print(f"xxxxxxxxx we have a duplicate ranking for score {r['score']}")
        rank = i + 1 - duplicates
        scores[r["score"]] = r["score"]
        print(
            f"{rank} * {int(r['bid'])} // score = {str(r['score']).zfill(11)} // hand = {r['hand']}"
        )
        res += rank * int(r["bid"])

    print(f"res: {res}")
    print(f"duplicates: {duplicates}")


def puzzle1(filename):
    read_file(filename)
    solve()


def puzzle2(filename):
    read_file(filename, 2)
    solve(2)


if __name__ == "__main__":
    # puzzle1('../../puzzles/2023/07/example.txt')  # result -> 6440
    # puzzle1('../../puzzles/2023/07/input.txt')  # result -> 241344943
    # puzzle2('../../puzzles/2023/07/example.txt')  # result -> 5905
    puzzle2("../../puzzles/2023/07/input.txt")  # result -> 243101568
