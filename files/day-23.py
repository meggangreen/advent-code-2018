""" Notes

    It's a pretty good feeling to read a puzzle and say "I can do that!"

    nanobot x,y,z,r

"""

import re
from queue import PriorityQueue

class Nano:
    def __init__(self, x, y, z, r):
        self.x = x
        self.y = y
        self.z = z
        self.r = r

    def is_in_my_range(self, nano):
        manhattan = sum([abs(self.x - nano.x),
                         abs(self.y - nano.y),
                         abs(self.z - nano.z)])
        return self.r >= manhattan

    def get_bounds(self):

        x_upp = self.x + self.r
        x_low = self.x - self.r
        y_upp = self.y + self.r
        y_low = self.y - self.r
        z_upp = self.z + self.r
        z_low = self.z - self.r

        return [x_upp, x_low, y_upp, y_low, z_upp, z_low]


class NanoFam(list):
    def __init__(self, nanos):
        super().__init__(nanos)
        # self.nanos = nanos  # list of Nano objs
        self.r_leader = None

    def set_r_leader(self):
        leader = Nano(0, 0, 0, float('inf') * -1)
        for nano in self:
            if nano.r > leader.r:
                leader = nano

        self.r_leader = leader


def count_nanos_in_r_leader_range(nanofam):
    """ Part One """

    leader = nanofam.r_leader

    count = 0
    for nano in nanofam:
        if leader.is_in_my_range(nano):
            count += 1

    return count


def get_nanos_in_range(origin, nanofam):
    matches = NanoFam([])

    for nano in nanofam:
        if origin.is_in_my_range(nano):
            matches.append(nano)

    matches.sort(key=lambda n: n.r, reverse=True)

    return matches


def get_intersection_coords(nanofam):

    # get coordinate that has most intersections with nano ranges
    # my r_leader connects with most nanos -- 341
    # what are the coordinates that exist within all 341 nano ranges?
    # what is the nano within leader's range that has the smallest range?
    # 0,0,0 to outer bounds of smallest-r nano is 0,5009904,0 -- 5009904 is too low says AOC
    # result included all 341 nanos and the distance was 16556366,37610040,6956865 -- 61130571 is too low

    the341 = get_nanos_in_range(nanofam.r_leader, nanofam)

    winner = Nano(0, 0, 0, float('inf'))
    w_x_upp, w_x_low, w_y_upp, w_y_low, w_z_upp, w_z_low = winner.get_bounds()

    count = 0
    for nano in the341:
        if winner.is_in_my_range(nano):
            count += 1
            x_upp, x_low, y_upp, y_low, z_upp, z_low = nano.get_bounds()
            w_x_upp = min(w_x_upp, x_upp)
            w_y_upp = min(w_y_upp, y_upp)
            w_z_upp = min(w_z_upp, z_upp)
            w_x_low = max(w_x_low, x_low)
            w_y_low = max(w_y_low, y_low)
            w_z_low = max(w_z_low, z_low)
            winner = nano

    print(count)
    return [w_x_upp, w_x_low, w_y_upp, w_y_low, w_z_upp, w_z_low]


def make_nano_fam(filename):
    xyz_patt = re.compile(r'(?<=pos=<)[\-\d]+,[\-\d]+,[\-\d]+(?=>)')
    r_patt = re.compile(r'(?<=r=)[\d]+')
    with open(filename) as file:
        lines = [line.strip() for line in file.readlines()]

    nanofam = NanoFam([])

    for line in lines:
        x, y, z = [int(n) for n in re.search(xyz_patt, line)[0].split(',')]
        r = int(re.search(r_patt, line)[0])
        nanofam.append(Nano(x, y, z, r))

    nanofam.set_r_leader()

    return nanofam


def part_two_copied():
    """ thanks to EriiKKo https://www.reddit.com/r/adventofcode/comments/a8s17l/2018_day_23_solutions/ecdqzdg """

    # The lowest valued entries are retrieved first (the lowest valued entry is
    # the one returned by sorted(list(entries))[0]). A typical pattern for
    # entries is a tuple in the form: (priority, data).

    # this works because each smaller bot is completely nested in the larger,
    # which I did find on my own in looking at the341

    with open('day-23.txt') as file:
        lines = file.readlines()

    bots = [map(int, re.findall(r"-?[\d]+", line)) for line in lines]

    segments = PriorityQueue()

    # The queue is holding entries for the start and end of each "line segment"
    # as measured by manhattan distance to 0,0,0. At the start of the segment,
    # the '1' (last element in the tuple) adds to the total of overlapping
    # segments. The '-1' that marks the segment's end is used to decrease the counter.
    for x, y, z, r in bots:
        d = abs(x) + abs(y) + abs(z)    # manhattan distance to 0,0,0
        segments.put((max(0, d - r), 1))       # priority = 0 or d - r
        segments.put((d + r + 1, -1))          # priority = d + r + 1

    count = 0
    maxCount = 0
    result = 0

    # calculates the maximum number of overlapping segments,
    # and the point where the maximum is hit, which is the answer
    while not segments.empty():
        dist, e = segments.get()
        count += e
        if count > maxCount:
            result = dist
            maxCount = count

    return result


################################################################################

if __name__ == '__main__':
    nanofam = make_nano_fam('day-23.txt')
    pt1 = count_nanos_in_r_leader_range(nanofam)  # 341

    pt2 = part_two_copied()  # 105191907

    print(f"Part 1: {pt1}")
    print(f"Part 2: {pt2}")

