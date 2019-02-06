""" Notes

    It's a pretty good feeling to read a puzzle and say "I can do that!"

    nanobot x,y,z,r

"""

import re

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


################################################################################

if __name__ == '__main__':
    nanofam = make_nano_fam('day-23.txt')
    pt1 = count_nanos_in_r_leader_range(nanofam)

    pt2 = None

    print(f"Part 1: {pt1}")
    print(f"Part 2: {pt2}")

