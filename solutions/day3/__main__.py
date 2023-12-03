import string
from pathlib import Path

with open((Path(__file__).parent / "input.txt").resolve()) as infile:
    input = [[char for char in line.strip()] for line in infile]


def parse(lines):
    result = []
    numbers = set()
    asterisks = set()

    def check_around_symbol(coords):
        start_line_idx, start_idx = coords

        # Look at all adjacent squares to find any numbers
        to_check = {
            (start_line_idx - 1, start_idx - 1),
            (start_line_idx - 1, start_idx),
            (start_line_idx - 1, start_idx + 1),
            (start_line_idx, start_idx - 1),
            (start_line_idx, start_idx + 1),
            (start_line_idx + 1, start_idx - 1),
            (start_line_idx + 1, start_idx),
            (start_line_idx + 1, start_idx + 1),
        }
        # Don't check any numbers we've already found
        to_check -= numbers

        while to_check:
            check_line_idx, check_idx = to_check.pop()
            if (
                0 <= check_line_idx < len(lines)
                and 0 <= check_idx < len(lines[check_line_idx])
                and lines[check_line_idx][check_idx] in string.digits
                and (check_line_idx, check_idx) not in numbers
            ):
                num_coords = {(check_line_idx, check_idx)}
                num = lines[check_line_idx][check_idx]

                # Gather the whole number
                # Backwards first
                num_idx = check_idx - 1
                while (
                    0 <= check_line_idx < len(lines)
                    and 0 <= num_idx < len(lines[check_line_idx])
                    and (num_char := lines[check_line_idx][num_idx]) in string.digits
                ):
                    to_check.discard((check_line_idx, num_idx))
                    num_coords.add((check_line_idx, num_idx))
                    num = num_char + num
                    num_idx -= 1

                # Then forwards
                num_idx = check_idx + 1
                while (
                    0 <= check_line_idx < len(lines)
                    and 0 <= num_idx < len(lines[check_line_idx])
                    and (num_char := lines[check_line_idx][num_idx]) in string.digits
                ):
                    to_check.discard((check_line_idx, num_idx))
                    num_coords.add((check_line_idx, num_idx))
                    num = num + num_char
                    num_idx += 1

                # Add the number to the set of numbers we've found
                numbers.update(num_coords)

                result.append((num, num_coords))

    for line_idx, line in enumerate(lines):
        for idx, char in enumerate(line):
            if char not in string.digits and char != ".":
                if char == "*":
                    asterisks.add((line_idx, idx))
                check_around_symbol((line_idx, idx))

    return result, asterisks


result, asterisks = parse(input)


def part1():
    print(sum(int(num) for num, _ in result if num))


def part2():
    gear_ratio_sum = 0
    for line_idx, idx in asterisks:
        adjacent_nums = set()
        adjacent_points = {
            (line_idx - 1, idx - 1),
            (line_idx - 1, idx),
            (line_idx - 1, idx + 1),
            (line_idx, idx - 1),
            (line_idx, idx + 1),
            (line_idx + 1, idx - 1),
            (line_idx + 1, idx),
            (line_idx + 1, idx + 1),
        }

        for num, coords in result:
            if any(coord in adjacent_points for coord in coords):
                adjacent_nums.add((num, frozenset(coords)))

        if len(adjacent_nums) == 2:
            num1, _ = adjacent_nums.pop()
            num2, _ = adjacent_nums.pop()

            gear_ratio = int(num1) * int(num2)
            gear_ratio_sum += gear_ratio

    print(gear_ratio_sum)


part1()
part2()
