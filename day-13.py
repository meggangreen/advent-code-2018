""" Part One """
# Bummer! it works for the test input, but misses the first crash on the regular
# I had fun making the objects, but it seems like I'm the only one using OOP in
# Python instead of just scripting

CHOICES = ['left', 'straight', 'right']
ORIENS = 'NESW'
NS = 'NS'
EW = 'EW'
TRACKS = []
CARTS = []

class Cart(object):
    def __init__(self, data, track_id, position, orientation):
        self.data = data
        self.track_id = track_id
        self.position = position
        self.path = []
        self.orientation = orientation
        self.i_choice = 'left'


    def __repr__(self):
        return (f"{self.__class__.__name__} "
                f"{self.data!r} @ {self.position!r}")


    def update_i_choice(self):
        c = CHOICES.index(self.i_choice)
        self.i_choice = CHOICES[0] if c + 1 >= len(CHOICES) else CHOICES[c+1]


    def update_orientation(self, direction):
        if direction == 'straight':
            return

        o = ORIENS.index(self.orientation)
        if direction == 'right':
            self.orientation = ORIENS[0] if o + 1 >= len(ORIENS) else ORIENS[o+1]
        elif direction == 'left':
            self.orientation = ORIENS[3] if o - 1 < 0 else ORIENS[o-1]


    def update_position(self, x, y):
        current_x, current_y = self.position
        if self.orientation == 'N':
            current_y += -y
        elif self.orientation == 'S':
            current_y += y
        elif self.orientation == 'E':
            current_x += x
        elif self.orientation == 'W':
            current_x += -x

        self.position = (current_x, current_y)
        self.path.append(get_path_step(self.track_id, self.position))


    def advance(self):
        action = self.path[-1]
        if action == '-':
            direction = 'straight'
            x, y = 1, 0
        elif action == '|':
            direction = 'straight'
            x, y = 0, 1
        elif action == '/':
            if self.orientation in NS:
                direction = 'right'
                x, y = 1, 0
            else:
                direction = 'left'
                x, y = 0, 1
        elif action == '\\':
            if self.orientation in EW:
                direction = 'right'
                x, y = 0, 1
            else:
                direction = 'left'
                x, y = 1, 0
        elif action == '+':
            direction = self.i_choice
            if ((direction == 'straight' and self.orientation in EW)
               or (direction != 'straight' and self.orientation in NS)):
                x, y = 1, 0
            if ((direction == 'straight' and self.orientation in NS)
               or (direction != 'straight' and self.orientation in EW)):
                x, y = 0, 1
            self.update_i_choice()

        self.update_orientation(direction)
        self.update_position(x, y)


class Cycle(object):
    def __init__(self):
        self.num = 0
        self.crash = None
        self.positions = []


    def run(self, carts):
        while self.num < 1000:
            positions = {self.num: [], 'crash': []}
            for cart in carts:
                cart.advance()
                if cart.position in positions[self.num]:
                    positions['crash'].append(cart.position)
                    print(f"Crash at {positions['crash']} on cycle {self.num}!")
                    return
                else:
                    positions[self.num].append(cart.position)
            self.positions.append(positions)
            self.num += 1


class Track(object):
    def __init__(self, track_id, grid):
        self.track_id = track_id
        self.grid = grid


def parse_input():
    grid = None
    carts = []
    # with open('day-13-test.txt') as file:
    with open('day-13.txt') as file:
        lines = [line.rstrip('\n') for line in file.readlines()]
    grid = [[''] * len(lines) for j in range(max([len(line) for line in lines]))]
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            grid[x][y] = char
            if char in '<>^v':
                carts.append((x, y, char))

    track = Track(0, grid)

    for c, cart in enumerate(carts):
        x, y, _ = cart
        carts[c] = make_cart(cart, c)
        section = [grid[i][y-1:y+2] for i in range(x-1, x+2)]
        grid[x][y] = replace_cart(carts[c], section)
        carts[c].path.append(grid[x][y])

    track.grid = grid

    return track, carts


def make_cart(cart, c):
    x, y, char = cart
    data = chr(65+c)
    orientation = ORIENS['^>v<'.index(char)]
    position = (x, y)
    return Cart(data, 0, position, orientation)


def replace_cart(cart, section):
    if cart.orientation in NS and section[0][1] != '-' and section[2][1] != '-':
        return '|'
    elif cart.orientation in EW and section[1][0] != '|' and section[1][2] != '|':
        return '-'
    else:
        return '8'


def get_path_step(track_id, position):
    x, y = position
    return TRACKS[track_id].grid[x][y]


# ################
# if __name__ == '__main__':
#     track, carts = parse_input()
#     TRACKS.append(track)
#     CARTS.extend(carts)


""" Parts One and Two copied from reddit sbjf """
# uses complex numbers -- i havent read itertools module
from itertools import cycle

with open('day-13-test.txt') as file:
# with open('day-13.txt') as file:
    puzzle_input = file.read()

grid = {}; carts = {}; directions = {'<': -1, '>': 1, '^': 1j, 'v': -1j}
for i, row in enumerate(puzzle_input.split("\n")):
    for j, char in enumerate(row):
        position = j-i*1j
        if char in r'/\+':
            grid[position] = char
        elif char in directions:
            carts[position] = directions[char], cycle([1j, 1, -1j])

while len(carts) > 1:
    for position in sorted(carts, key=lambda x: (-x.imag, x.real)):
        if position not in carts:
            continue  # deleted due to collision
        direction, turn = carts.pop(position)  # take out cart
        position += direction  # update position

        if position in carts:  # handle collision
            print('collision!', position)  #, '-- cart was at ', position - direction)
            del carts[position]
            continue

        track = grid.get(position)  # update direction
        if track == '+':
            direction = direction * next(turn)
        elif track is not None:  # / or \
            direction *= 1j * (2*((track == '/') ^ (direction.real == 0))-1)

        carts[position] = direction, turn  # put cart back onto tracks

print(carts)