import re
from collections import deque

COORD = re.compile(r"^[xy]=[\d]+")
SPAN = re.compile(r"[\d]+\.\.[\d]+")

def get_dim_loc_min_max(line):
    dim = line[0]
    loc = int(re.search(COORD, line)[0].split('=')[1])
    mini, maxi = tuple(int(n) for n in re.search(SPAN, line)[0].split('..'))
    return dim, loc, mini, maxi


class Grid(dict):
    def __init__(self, lines):
        super().__init__()

        # Organize clay coords
        for line in lines:
            dim, n, mini, maxi = get_dim_loc_min_max(line)
            new_ys = [n] if dim == 'y' else [y for y in range(mini, maxi+1)]
            new_low_x, new_upp_x = (mini, maxi) if dim == 'y' else (n, n)
            self._update_coords(new_ys, new_low_x, new_upp_x)

        # Get grid bounds
        y_bounds = sorted(self.keys())
        self.min_y, self.max_y = y_bounds[0], y_bounds[-1]
        self.min_x = sorted(self.items(), key=lambda yx: yx[1])[0][1][0][0]
        self.max_x = sorted(self.items(), key=lambda yx: yx[1][-1][1])[-1][1][-1][1]


    def display(self):
        for y in range(0, self.max_y+2):
        row = ['.']*((self.max_x+1)-(self.min_x-1))
        if y == 0:
            row[500-self.min_x] = '+'
        if self.get(y):
            for (low_x, upp_x) in self[y]:
                low_x = low_x - self.min_x
                upp_x = upp_x - self.min_x
                row[low_x:upp_x+1] = ['#'] * (upp_x+1 - low_x)
        print(''.join(row))


    def _update_coords(self, ys, low_x, upp_x):
        for y in ys:
            if not self.get(y):
                self[y] = deque([(low_x, upp_x)])
                continue

            for i in range(len(self[y])):
                mini, maxi = self[y][i]
                # equal to or contained by -- do nothing
                if ( (low_x == mini and upp_x == maxi) or
                     (low_x >= mini and upp_x <= maxi) ):
                    break
                # insert new lowest
                if low_x < mini and upp_x < mini:
                    self[y].rotate(-i)
                    self[y].append((low_x, upp_x))
                    self[y].rotate(i+1)
                # contains or expands -- replace
                elif ( (low_x <= mini and upp_x >= maxi) or
                       (low_x < mini and mini <= upp_x <= maxi) or
                       (upp_x > maxi and maxi >= low_x >= mini) ):
                    self[y].rotate(-i)
                    self[y].popleft()
                    self[y].append((min(low_x, mini), max(upp_x, maxi)))
                    self[y].rotate(i+1)
                # insert new greatest
                elif i+1 == len(self[y]):
                    self[y].append((low_x, upp_x))

            # combine adjacent ranges
            i = 0
            while i < len(self[y])-1:
                if self[y][i][1] == self[y][i+1][0]:
                    mini, maxi = self[y][i][0], self[y][i+1][1]
                    self[y].rotate(-i)
                    self[y].popleft()
                    self[y].popleft()
                    self[y].append((mini, maxi))
                    self[y].rotate(i+1)
                else:
                    i += 1

