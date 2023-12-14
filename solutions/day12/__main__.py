from pathlib import Path

with open((Path(__file__).parent / "input.txt").resolve()) as infile:
    input = []
    for line in infile:
        if line:
            condition, sizes = line.strip().split()
            sizes = [int(x) for x in sizes.split(",")]
            input.append((condition, sizes[::-1]))

complete = 0

for condition_str, sizes in input:
    valid = [(condition_str, sizes.copy(), 0)]

    while valid:
        current, curr_sizes, start = valid.pop()

        if not curr_sizes and sum(1 for c in current if c == "#") == sum(sizes):
            complete += 1
            continue

        # Try to insert the next size into the current valid combinations
        size = curr_sizes.pop()

        # Need space for each size and one for the separator;
        # except for the last size, which needs no extra space
        # Negative to work with indexing
        reserved_space = 1 - sum(curr_sizes) - len(curr_sizes) if curr_sizes else None

        for k, c in enumerate(current[start:reserved_space]):
            pos = start + k
            if c != ".":
                # Try to insert the size
                if (
                    len(current[pos + size : reserved_space]) >= 0
                    and "." not in current[pos : pos + size]
                    and (reserved_space is not None or pos + size <= len(current))
                    and (len(current) == pos + size or current[pos + size] != "#")
                    and (pos == 0 or current[pos - 1] != "#")
                ):
                    new = current[:pos] + "#" * size + current[pos + size :]
                    valid.append((new, curr_sizes.copy(), pos + size + 1))


print(complete)
