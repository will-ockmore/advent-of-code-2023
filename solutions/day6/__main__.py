import math
from pathlib import Path

with open((Path(__file__).parent / "input.txt").resolve()) as infile:
    lines = infile.readlines()

    nums = [[int(x) for x in line.strip().split()[1:]] for line in lines if line]
    input = list(zip(nums[0], nums[1]))

"""
Knowns:
d = distance (to beat)
t_t = total time

Variable:
s = speed
t_b = time spent accelerating (on the button)
t_r = time spent at constant speed (after releasing the button)

So:

s = t_b
t_r = t_t - t_b
d = s * t_r

Substituting:

d = t_b * (t_t - t_b)

Solving for t_b:

1/2 * (t_t - sqrt(t_t^2 - 4d)) < t_b < 1/2 * (t_t + sqrt(t_t^2 - 4d))
"""

results = []


def get_num_ways_to_win(t_t, d):
    lower = 0.5 * (t_t - (t_t**2 - 4 * d) ** 0.5)
    upper = 0.5 * (t_t + (t_t**2 - 4 * d) ** 0.5)

    return len(list(range(math.ceil(lower), math.floor(upper) + 1)))


for t_t, d in input:
    results.append(get_num_ways_to_win(t_t, d))

print(math.prod(results))

# Part 2

t_t = int("".join(n for n in lines[0] if n.isdigit()))
d = int("".join(n for n in lines[1] if n.isdigit()))

print(get_num_ways_to_win(t_t, d))
