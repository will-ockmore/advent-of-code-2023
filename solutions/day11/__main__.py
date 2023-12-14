import itertools
from pathlib import Path

with open((Path(__file__).parent / "input.txt").resolve()) as infile:
    input = [line.strip() for line in infile if line]

# Expand lines
expanded = []

for y, line in enumerate(input):
    new_line = ""
    for x, c in enumerate(line):
        new_line += c
        if all(ln[x] == "." for ln in input):
            new_line += "."
    expanded.append(new_line)
    if all(c == "." for c in new_line):
        expanded.append(new_line)
        continue

galaxies = []

for y, line in enumerate(expanded):
    for x, c in enumerate(line):
        if c == "#":
            galaxies.append((x, y))

print(
    sum(
        # Manhattan distance
        abs(x_1 - x_2) + abs(y_1 - y_2)
        for (x_1, y_1), (x_2, y_2) in itertools.combinations(galaxies, 2)
    )
)

# Part 2
expanded_x = set()
expanded_y = set()
galaxies = []

for y, line in enumerate(input):
    for x, c in enumerate(line):
        if all(ln[x] == "." for ln in input):
            expanded_x.add(x)
        if c == "#":
            galaxies.append((x, y))
    if all(c == "." for c in line):
        expanded_y.add(y)
        continue

total = 0

for (x_1, y_1), (x_2, y_2) in itertools.combinations(galaxies, 2):
    base_distance = abs(x_1 - x_2) + abs(y_1 - y_2)

    # Add the expanded distances
    xs = set(range(min(x_1, x_2), max(x_1, x_2)))
    ys = set(range(min(y_1, y_2), max(y_1, y_2)))

    total += (
        base_distance
        + len(xs.intersection(expanded_x)) * (1e6 - 1)
        + len(ys.intersection(expanded_y)) * (1e6 - 1)
    )

print(int(total))
