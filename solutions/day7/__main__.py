from collections import Counter
from pathlib import Path

FACE_CARDS = {"A": 14, "K": 13, "Q": 12, "J": 11, "T": 10}


with open((Path(__file__).parent / "input.txt").resolve()) as infile:
    input = [line.strip().split() for line in infile if line]

hands = {}

for cards, bid in input:
    rank = Counter([card for card in cards])

    hands[
        (
            *sorted(rank.values(), reverse=True),
            *(int(FACE_CARDS.get(k, k)) for k in cards),
        )
    ] = bid

total = 0

for i, hand in enumerate(sorted(hands.keys())):
    total += (i + 1) * int(hands[hand])

print(total)

# Part 2

hands = {}

FACE_CARDS["J"] = -1

for cards, bid in input:
    rank = Counter([card for card in cards if card != "J"])

    if num_j := sum(1 for card in cards if card == "J"):
        if num_j == 5:
            rank["A"] = 5
        else:
            rank[rank.most_common()[0][0]] += num_j

    hands[
        (
            *sorted(rank.values(), reverse=True),
            *(int(FACE_CARDS.get(k, k)) for k in cards),
        )
    ] = bid

total = 0

for i, hand in enumerate(sorted(hands.keys())):
    total += (i + 1) * int(hands[hand])

print(total)
