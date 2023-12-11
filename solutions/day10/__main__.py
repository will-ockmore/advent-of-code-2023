import sys
from enum import Enum, auto
from pathlib import Path

with open((Path(__file__).parent / "input.txt").resolve()) as infile:
    input = [[c for c in line.strip()] for line in infile]


class Direction(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()


start = None

# Find the start
for y, row in enumerate(input):
    for x, char in enumerate(row):
        if char == "S":
            start = (x, y)
            break
    else:
        continue
    break

if not start:
    raise Exception("No start found")


class InvalidPath(Exception):
    pass


def find_path(initial_pos, initial_direction):
    curr = initial_pos
    direction = initial_direction

    path = []
    while True:
        x, y = curr
        if not (0 <= x < len(input[0]) and 0 <= y < len(input)):
            raise InvalidPath

        symbol = input[y][x]

        if symbol == "S":
            return path

        match symbol, direction:
            case "|", Direction.UP:
                path += [curr]
                curr = (x, y - 1)
                direction = Direction.UP
            case "|", Direction.DOWN:
                path += [curr]
                curr = (x, y + 1)
                direction = Direction.DOWN
            case "-", Direction.RIGHT:
                path += [curr]
                curr = (x + 1, y)
                direction = Direction.RIGHT
            case "-", Direction.LEFT:
                path += [curr]
                curr = (x - 1, y)
                direction = Direction.LEFT
            case "L", Direction.DOWN:
                path += [curr]
                curr = (x + 1, y)
                direction = Direction.RIGHT
            case "L", Direction.LEFT:
                path += [curr]
                curr = (x, y - 1)
                direction = Direction.UP
            case "J", Direction.DOWN:
                path += [curr]
                curr = (x - 1, y)
                direction = Direction.LEFT
            case "J", Direction.RIGHT:
                path += [curr]
                curr = (x, y - 1)
                direction = Direction.UP
            case "7", Direction.UP:
                path += [curr]
                curr = (x - 1, y)
                direction = Direction.LEFT
            case "7", Direction.RIGHT:
                path += [curr]
                curr = (x, y + 1)
                direction = Direction.DOWN
            case "F", Direction.LEFT:
                path += [curr]
                curr = (x, y + 1)
                direction = Direction.DOWN
            case "F", Direction.UP:
                path += [curr]
                curr = (x + 1, y)
                direction = Direction.RIGHT
            case _:
                raise InvalidPath


def find_path_pt_2(initial_pos, initial_direction):
    curr = initial_pos
    direction = initial_direction

    path = []

    # One of these will contain the points enclosed by the path
    left_points = set()
    right_points = set()

    # Will be either 360 or -360, for a right or left turn
    angle = 0

    while True:
        x, y = curr
        if not (0 <= x < len(input[0]) and 0 <= y < len(input)):
            raise InvalidPath

        symbol = input[y][x]

        if symbol == "S":
            path += [curr]
            path = set(path)
            return path, right_points - path if angle > 0 else left_points - path

        match symbol, direction:
            case "|", Direction.UP:
                path += [curr]
                left_points.add((x - 1, y))
                right_points.add((x + 1, y))
                curr = (x, y - 1)
                direction = Direction.UP
            case "|", Direction.DOWN:
                path += [curr]
                left_points.add((x + 1, y))
                right_points.add((x - 1, y))
                curr = (x, y + 1)
                direction = Direction.DOWN
            case "-", Direction.RIGHT:
                path += [curr]
                left_points.add((x, y - 1))
                right_points.add((x, y + 1))
                curr = (x + 1, y)
                direction = Direction.RIGHT
            case "-", Direction.LEFT:
                path += [curr]
                left_points.add((x, y + 1))
                right_points.add((x, y - 1))
                curr = (x - 1, y)
                direction = Direction.LEFT
            case "L", Direction.DOWN:
                path += [curr]
                right_points.add((x, y - 1))
                right_points.add((x - 1, y))
                angle -= 90
                curr = (x + 1, y)
                direction = Direction.RIGHT
            case "L", Direction.LEFT:
                path += [curr]
                left_points.add((x, y - 1))
                left_points.add((x - 1, y))
                angle += 90
                curr = (x, y - 1)
                direction = Direction.UP
            case "J", Direction.DOWN:
                path += [curr]
                left_points.add((x + 1, y))
                left_points.add((x, y + 1))
                angle += 90
                curr = (x - 1, y)
                direction = Direction.LEFT
            case "J", Direction.RIGHT:
                path += [curr]
                right_points.add((x + 1, y))
                right_points.add((x, y + 1))
                angle -= 90
                curr = (x, y - 1)
                direction = Direction.UP
            case "7", Direction.UP:
                path += [curr]
                right_points.add((x + 1, y))
                right_points.add((x, y - 1))
                angle -= 90
                curr = (x - 1, y)
                direction = Direction.LEFT
            case "7", Direction.RIGHT:
                path += [curr]
                left_points.add((x + 1, y))
                left_points.add((x, y - 1))
                angle += 90
                curr = (x, y + 1)
                direction = Direction.DOWN
            case "F", Direction.LEFT:
                path += [curr]
                right_points.add((x - 1, y))
                right_points.add((x, y - 1))
                angle -= 90
                curr = (x, y + 1)
                direction = Direction.DOWN
            case "F", Direction.UP:
                path += [curr]
                left_points.add((x - 1, y))
                left_points.add((x, y - 1))
                angle += 90
                curr = (x + 1, y)
                direction = Direction.RIGHT
            case _:
                raise InvalidPath


BOLD_WHITE = "\x1b[37;1m"
RESET = "\x1b[0m"


def print_points(points: set[tuple[int, int]]):
    for y, row in enumerate(input):
        for x, char in enumerate(row):
            if (x, y) in points:
                sys.stdout.write(f"{BOLD_WHITE}{char}{RESET}")
            else:
                sys.stdout.write(".")
        sys.stdout.write("\n")


for x, y, allowed_pipes, direction in [
    (start[0] + 1, start[1], ["-", "7", "J"], Direction.RIGHT),
    (start[0] - 1, start[1], ["-", "L", "F"], Direction.LEFT),
    (start[0], start[1] + 1, ["|", "J", "L"], Direction.DOWN),
    (start[0], start[1] - 1, ["|", "7", "F"], Direction.UP),
]:
    try:
        if input[y][x] in allowed_pipes:
            path = find_path((x, y), direction)
            # Any path is fine, there will be two idential paths
            print(len(path) // 2 + 1)
            # print_points(set(path))

            # Part 2
            path, interior_points = find_path_pt_2((x, y), direction)

            # print_points(path)

            visited = set()

            queue = list(interior_points)

            while queue:
                x, y = queue.pop()
                visited.add((x, y))
                next_points = [
                    pos
                    for pos in [
                        (x + 1, y),
                        (x - 1, y),
                        (x, y + 1),
                        (x, y - 1),
                    ]
                    if pos not in path
                    and pos not in visited
                    and pos not in interior_points
                ]
                if any(x[1] < 0 for x in next_points):
                    breakpoint()
                queue += next_points

            # print_points(visited)

            print(len(visited))

            break
    except InvalidPath:
        continue
