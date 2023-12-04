from collections import defaultdict
from pathlib import Path

with open((Path(__file__).parent / "input.txt").resolve()) as infile:
    input = []
    for line in infile:
        card, nums = line.strip().split(":")
        winning_nums, your_nums = [
            [num for num in x.strip().split(" ") if num]
            for x in nums.strip().split("|")
        ]
        input.append((card, winning_nums, your_nums))


def part1():
    print(
        sum(
            2 ** (matches - 1)
            if (matches := len(list(set(winning) & set(yours)))) > 0
            else 0
            for _, winning, yours in input
        )
    )


def part2():
    additional_scratchcards = defaultdict(int)

    for idx, (_, winning, yours) in enumerate(input):
        matches = len(list(set(winning) & set(yours)))
        for _ in range(additional_scratchcards[idx] + 1):
            for k in range(1, matches + 1):
                additional_scratchcards[idx + k] += 1

    print(len(additional_scratchcards.keys()) + sum(additional_scratchcards.values()))


part1()
part2()
