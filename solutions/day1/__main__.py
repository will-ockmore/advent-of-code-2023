import re
from pathlib import Path
from typing import Final

with open((Path(__file__).parent / "input.txt").resolve()) as infile:
    input = [line.strip() for line in infile]


def part1(lines):
    result = []
    for line in lines:
        first = ""
        last = ""
        for char in line:
            if char.isdigit():
                if not first:
                    first = char
                    last = char
                else:
                    last = char
        result.append(first + last)

    print(sum(int(num) for num in result if num))


digits: Final[list[tuple[str, int]]] = {
    "one": "o1e",
    "two": "t2o",
    "three": "t3e",
    "four": "f4r",
    "five": "f5e",
    "six": "s6x",
    "seven": "s7n",
    "eight": "e8t",
    "nine": "n9e",
}


def replace_match(match):
    return digits[match.group(0)]


def part2():
    digits_replaced_input = []
    for line in input:
        print(line)
        line_with_digits_replaced = re.sub("|".join(digits.keys()), replace_match, line)
        print(line_with_digits_replaced)
        # Catch any overlapping
        line_with_digits_replaced = re.sub(
            "|".join(digits.keys()), replace_match, line_with_digits_replaced
        )
        print(line_with_digits_replaced)
        digits_replaced_input.append(line_with_digits_replaced)

    part1(digits_replaced_input)


part1(input)
part2()
