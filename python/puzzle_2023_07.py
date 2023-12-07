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
    "2": 1
}


def read_file(filename, part=1):
    hands.clear()
    bids.clear()
    f = open(filename, "r")
    for line in f:
        line = line.strip()
        if line == "":
            continue

        x = line.split()
        hand = x[0]
        bid = x[1]

        if part == 2:
            print(f"part 2")
        else:
            hands.append(hand)
            bids.append(bid)


def solve():
    results = []
    for i in range(0, len(hands)):
        hand = hands[i]

        singles = []
        pairs = []
        triads = []
        counts = {}

        for c in hand:
            count = 0
            singles.append(cards[c])
            if c in counts:
                count = counts[c]
            counts[c] = count + 1

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

        score = ""
        for v in vals:
            score = str(1 if v > 0 else 0) + score

        fullhouse = 1 if pairs and triads else 0
        has_pairs = 1 if len(pairs) == 2 else 0

        score = score[:2] + str(fullhouse) + score[2:4] + str(has_pairs) + score[4:]

        for c in singles:
            score = score + str(c).zfill(2)

        # result = {"hand": hands[i], "bid": bids[i], "score": score}
        result = {"hand": hands[i], "bid": bids[i], "score": int(score)}
        results.append(result)

    results = sorted(results, key=lambda x: x['score'])
    # print(results)

    res = 0

    scores = {}

    f = open("output.txt", "w")

    duplicates = 0
    for i in range(0, len(results)):
        r = results[i]
        if r['score'] in scores:
            duplicates += 1
            print(f"xxxxxxxxx we have a duplicate ranking for score {r['score']}")
        rank = i + 1 - duplicates
        scores[r['score']] = r['score']
        print(
            f"{rank} * {int(r['bid'])} // score = {r['score']} // hand = {r['hand']} // hand = {''.join(sorted(r['hand']))}")
        res += rank * int(r['bid'])
        f.write(f"{r['hand']} {int(r['bid'])} {''.join(sorted(r['hand']))}\n")


    print(f"res: {res}")
    print(f"duplicates: {duplicates}")
    f.close()


def puzzle1(filename):
    read_file(filename)
    solve()


def puzzle2(filename):
    read_file(filename, 2)
    solve()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # puzzle1('../puzzles/2023/07/example.txt')  # result -> 6440
    # puzzle1('../puzzles/2023/07/input.txt')  # result -> 241643046
    # puzzle1('../puzzles/2023/07/input.txt')  # result -> 241528490
    # puzzle1('../puzzles/2023/07/input.txt')  # result -> 481877332
    # puzzle1('../puzzles/2023/07/input.txt')  # result -> 241042455
    # puzzle1('../puzzles/2023/07/input.txt')  # result -> 241542955
    # puzzle1('../puzzles/2023/07/example2.txt')  # result -> 6440
    # puzzle1('../puzzles/2023/07/input.txt')  # result -> 241298043
    # puzzle1('../puzzles/2023/07/input.txt')  # result -> 241556315
    # puzzle1('../puzzles/2023/07/input.txt')  # result -> 241480245
    # puzzle1('../puzzles/2023/07/input.txt')  # result -> 241344943
    # ########################################
    puzzle2('../puzzles/2023/07/example.txt')  # result ->
    # puzzle2('../puzzles/2023/07/input.txt')  # correct ->
