# Puzzle input: sn = 3031

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