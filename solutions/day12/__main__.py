from pathlib import Path

with open((Path(__file__).parent / "input.txt").resolve()) as infile:
    input = []
    for line in infile:
        if line:
            condition, sizes = line.strip().split()
            sizes = [int(x) for x in sizes.split(",")]
            input.append((condition, sizes[::-1]))


def find_arrangements(input):
    complete = 0

    for condition_str, sizes in input:

        def valid_combinations(current, sizes_index, start):
            if sizes_index == len(sizes):
                if sum(1 for c in current if c == "#") == sum(sizes):
                    return 1
                return 0

            size = sizes[sizes_index]

            # Need space for each size and one for the separator;
            # except for the last size, which needs no extra space
            # Negative to work with indexing
            remaining_sizes = sizes[sizes_index + 1 :]
            reserved_space = (
                1 - sum(remaining_sizes) - len(remaining_sizes)
                if remaining_sizes
                else None
            )

            for k, c in enumerate(current[start:reserved_space]):
                pos = start + k

                # Check if it's valid to continue
                if (
                    reserved_space is not None
                    and pos + size - reserved_space > len(current)
                ) or (reserved_space is None and pos + size > len(current)):
                    break

                if c != ".":
                    # Try to insert the size
                    if (
                        "." not in current[pos : pos + size]
                        and (len(current) == pos + size or current[pos + size] != "#")
                        and (pos == 0 or current[pos - 1] != "#")
                    ):
                        new = current[:pos] + "#" * size + current[pos + size :]
                        return valid_combinations(new, sizes_index + 1, pos + size + 1)
            return 0

        print(condition_str, sizes)
        valid = [(condition_str, sizes.copy(), 0)]

        while valid:
            current, curr_sizes, start = valid.pop()

            if not curr_sizes:
                if sum(1 for c in current if c == "#") == sum(sizes):
                    complete += 1
                continue

            # Try to insert the next size into the current valid combinations
            size = curr_sizes.pop()

            # Need space for each size and one for the separator;
            # except for the last size, which needs no extra space
            # Negative to work with indexing
            reserved_space = (
                1 - sum(curr_sizes) - len(curr_sizes) if curr_sizes else None
            )

            for k, c in enumerate(current[start:reserved_space]):
                pos = start + k

                # Check if it's valid to continue
                if (
                    reserved_space is not None
                    and pos + size - reserved_space > len(current)
                ) or (reserved_space is None and pos + size > len(current)):
                    break

                if c != ".":
                    # Try to insert the size
                    if (
                        "." not in current[pos : pos + size]
                        and (len(current) == pos + size or current[pos + size] != "#")
                        and (pos == 0 or current[pos - 1] != "#")
                    ):
                        new = current[:pos] + "#" * size + current[pos + size :]
                        valid.append((new, curr_sizes.copy(), pos + size + 1))

    return complete


print(find_arrangements(input))

# Part 2

# Duplicate the input five times, separated by a ?, and duplicate the sizes five times as well
duplicated_input = [
    ("?".join(condition_str for _ in range(5)), sizes * 5)
    for condition_str, sizes in input
]

print(find_arrangements(duplicated_input))
