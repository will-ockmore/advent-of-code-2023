import itertools
import math
import re
from collections import defaultdict
from pathlib import Path

with open((Path(__file__).parent / "input.txt").resolve()) as infile:
    input = [line.strip() for line in infile]

    instructions = [0 if c == "L" else 1 for c in input[0]]

    network = {}

    for line in input[1:]:
        if line:
            node, left, right = re.findall(r"[A-Z]+", line)
            network[node] = (left, right)


current = "AAA"

for i, instruction in enumerate(itertools.cycle(instructions)):
    if current == "ZZZ":
        break
    current = network[current][instruction]

print(i)

# Part 2
nodes = [node for node in network if node[-1] == "A"]
starts = [node for node in nodes if node[-1] == "A"]

ends = {node for node in nodes if node[-1] == "Z"}
visited = [defaultdict(dict) for _ in nodes]
cycle_points = [0 for _ in nodes]


for i, instruction in enumerate(itertools.cycle(instructions)):
    all_cycles_found = True
    for j, node in enumerate(nodes):
        if cycle_points[j]:
            continue
        all_cycles_found = False
        visits = visited[j][node]
        if i % len(instructions) in visits:
            # This is the cycle point
            cycle_points[j] = i - visits[i % len(instructions)]

        visits[i % len(instructions)] = i
        nodes[j] = network[node][instruction]

    if all_cycles_found:
        break

    nodes = [network[node][instruction] for node in nodes]

# Now we have the cycle points, we can calculate the number of steps to get to the end
print(math.lcm(*cycle_points))
