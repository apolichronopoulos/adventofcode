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
    f = open(filename, "r")
    for line in f:
        line = line.strip()
        print(line)
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
    print(f"{hands}")
    print(f"{bids}")
    results = []
    for i in range(0, len(hands)):
        hand = hands[i]
        print(f"hand {hand}")

        singles = []
        doubles = []
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
                doubles.append(v)
            if v > vals[count - 1]:
                vals[count - 1] = v

        score = ""
        for v in vals:
            score = str(v).zfill(2) + score


        double1 = "00"
        double2 = "00"
        if len(doubles) == 2:
            double1 = str(doubles[0]).zfill(2)
            double2 = str(doubles[1]).zfill(2)

        score = score[:6] + double1 + double2 + score[6:]

        # singles = sorted(singles, key=lambda x: x['score'])
        singles.sort(reverse=True)
        for c in singles:
            score = score + str(c).zfill(2)

        result = {"hand": hands[i], "bid": bids[i], "score": score}
        results.append(result)

    results = sorted(results, key=lambda x: x['score'])
    print(results)

    res = 0

    duplicates = 0
    for i in range(0, len(results)):
        r = results[i]
        # if i < len(results) - 2:
        #     next = results[i + 1]
        #     if r['score'] == next['score']:
        #         duplicates += 1
        #         print(f"xxxxxxxxx we have a duplicate ranking for score {r['score']}")
        rank = i + 1 - duplicates
        print(f"{rank} * {int(r['bid'])} // score = {r['score']} // hand = {r['hand']}")
        res += rank * int(r['bid'])

    print(f"res: {res}")
    print(f"duplicates: {duplicates}")


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
    puzzle1('../puzzles/2023/07/input.txt')  # result -> 241298043
    # puzzle2('../puzzles/2023/07/example.txt')  # result ->
    # puzzle2('../puzzles/2023/07/input.txt')  # correct ->
