import itertools
import re
from pathlib import Path

with open((Path(__file__).parent / "input.txt").resolve()) as infile:
    content = infile.read()

    if m := re.match(r"^seeds: (.*)", content):
        seeds = [int(x) for x in m.group(1).split()]

    maps = content.split("\n\n")[1:]

    map_ranges = []

    for m in maps:
        lines = m.split("\n")

        map_range = []

        for line in lines[1:]:
            if line:
                dest, source, length = [int(x) for x in line.split()]
                map_range.append((source, dest, length))

        map_range.sort()
        map_ranges.append((map_range))


def get_min_location(seeds):
    locations = []

    for seed in seeds:
        for map_range in map_ranges:
            if seed < map_range[0][0]:
                continue
            for i, (source, dest, length) in enumerate(map_range):
                if len(map_range) == i + 1 or source <= seed < map_range[i + 1][0]:
                    if seed < source + length:
                        seed = dest + (seed - source)
                    break

        locations.append(seed)

    print(min(locations))


get_min_location(seeds)

all_seeds = list(
    itertools.chain(
        *(range(start, start + length) for start, length in itertools.batched(seeds, 2))
    )
)

get_min_location(all_seeds)
