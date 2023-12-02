import math
from pathlib import Path
from typing import Final


def parse_game(line):
    game_id, game = line.split(":")
    game_id = int(game_id.split(" ")[1])

    rounds = [
        {
            color: int(number)
            for number, color in [
                color_pair.split(" ") for color_pair in game_round.strip().split(", ")
            ]
        }
        for game_round in game.strip().split(";")
    ]

    return game_id, rounds


with open((Path(__file__).parent / "input.txt").resolve()) as infile:
    input = [parse_game(line.strip()) for line in infile]

LIMITS: Final = {
    "red": 12,
    "green": 13,
    "blue": 14,
}


def part1():
    total = 0
    for game, rounds in input:
        possible = True
        for round in rounds:
            for color, number in round.items():
                if number > LIMITS[color]:
                    possible = False
        if possible:
            total += game
    print(total)


def part2():
    total = 0
    for game, rounds in input:
        max_colors = {}
        for round in rounds:
            for color, number in round.items():
                if color not in max_colors:
                    max_colors[color] = number
                else:
                    max_colors[color] = max(max_colors[color], number)
        power = math.prod(max_colors.values())
        total += power

    print(total)


part1()
part2()
