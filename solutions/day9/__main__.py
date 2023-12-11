from pathlib import Path

with open((Path(__file__).parent / "input.txt").resolve()) as infile:
    input = [[int(x) for x in line.strip().split()] for line in infile if line]


def get_next(sequence):
    steps = [number - sequence[i] for i, number in enumerate(sequence[1:])]

    if len(set(steps)) == 1:
        return sequence[-1] + steps[0]

    return sequence[-1] + get_next(steps)


print(sum(get_next(sequence) for sequence in input))

# Part 2

print(sum(get_next(sequence[::-1]) for sequence in input))
