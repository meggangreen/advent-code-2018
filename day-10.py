""" Part One """
import re

def process_input():
    with open('day-10.txt') as f:
        lines = [[int(i) for i in re.findall(r'-?\d+', l.strip())] for l in f.readlines()]

    grid_sizes = {}
    for i in range(20000):
        minx = min(x + i * vx for (x, y, vx, vy) in lines)
        maxx = max(x + i * vx for (x, y, vx, vy) in lines)
        miny = min(y + i * vy for (x, y, vx, vy) in lines)
        maxy = max(y + i * vy for (x, y, vx, vy) in lines)
        grid_sizes[i] = maxx - minx + maxy - miny

    i = sorted(grid_sizes.items(), key=lambda kv: kv[1])[0][0]
    print("i = {}".format(i))
    return i, lines


def make_grid(i, lines):
    grid = [[' '] * 200 for j in range(200)]

    for (x, y, vx, vy) in lines:
        grid[y + i * vy - 450][x + i * vx - 350] = '*'

    for m in grid:
        print(''.join(m))
