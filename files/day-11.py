# Puzzle input: sn = 3031

import numpy

""" Part One """

def calc_power_level(x, y, sn):
    return int(str(((x + 10) * y + sn) * (x + 10) // 100)[-1]) - 5


def make_grid(sn):
    grid = [[0]*300 for j in range(300)]
    for x in range(300):
        for y in range(300):
            grid[x][y] = calc_power_level(x+1, y+1, sn)

    return grid


def get_most_fuel(grid):
    fuel = float('inf') * -1
    x, y = -1, -1

    for i in range(len(grid)-3):
        for j in range(len(grid)-3):
            section = []
            section.extend(grid[i][j:j+3])
            section.extend(grid[i+1][j:j+3])
            section.extend(grid[i+2][j:j+3])
            section = sum(section)
            if section > fuel:
                fuel = section
                x, y = i+1, j+1

    return (x, y), fuel


""" Part Two """
# copied and modified from reddit sciyoshi
# it's really slow, but if you have a better guesstimate of the size you can
# reduce the range of size
# i'm not sure it's faster than my way would have been, but it's fewer lines

def power(x, y):
    rack = (x + 1) + 10
    power = rack * (y + 1)
    power += 3031
    power *= rack

    return (power // 100 % 10) - 5


def get_any_size_most_fuel():
    maxes = []
    grid = numpy.fromfunction(power, (300, 300))
    # don't rule out 1x1 or 2x2 sections
    for size in range(1, 30):
        sections = sum(grid[x:x-size or None, y:y-size or None]
                       for x in range(size) for y in range(size))
        maximum = int(sections.max())
        location = numpy.where(sections == maximum)
        maxes.append((maximum, location[0][0] + 1, location[1][0] + 1, size))

    return sorted(maxes, reverse=True)[0]
