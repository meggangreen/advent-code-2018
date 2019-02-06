""" Notes

    Oh good, another grid. I can do this one, I know it.

    puzzle input:
    DEPTH = 11109
    TARGET = 9,731 ==> (9+731j) :: risk grid has 6579 regions

    TYPES = {0: ("rocky", "."), 1: ("wet", "="), 2: ("narrow", "|")}
    SPECIALS = ["mouth", "target"]

    REGIONS = {coord: Region}

    region.coord (x+yj) -- x and y >= 0
    region.title None or a special
    region.type TYPES[r.erosion]
    region.geologi = {
        if r.title in ["mouth", "target"]:
            r.g = 0
        if r.coord.imag == 0:
            r.g = coord.real * 16807
        if r.coord.real == 0:
            r.g = coord.imag * 48271
        else:
            r.g = regions[r.coord-1].erosion * regions[r.coord-1j].erosion
    }
    region.erosion = (r.geologi + DEPTH) % 20183 = [0, 1, 2]

    special regions: mouth.coord = (0+0j)
                     target.coord = (tx+tyj)

    risk = sum([r.erosion for r in regions]) -- duh, ending points are target.coord
                                           if (r.coord.real <= t.coord.real and
                                               r.coord.imag <= t.coord.imag)])

"""

class Region:
    def __init__(self, coord):
        self.coord = coord
        self.title = None
        self.geologi = None
        self.erosion = None
        self.type = None

        self.__set_title(target)
        self.__set_geologi()
        self.__set_erosion()
        self.__set_type()

    def __set_title(self, target):
        if self.coord == TARGET:
            self.title = "target"
        if self.coord == 0+0j:
            self.title = "mouth"

    def __set_geologi(self):
        if self.title in SPECIALS:
            self.geologi = 0
        elif self.coord.imag == 0:
            self.geologi = self.coord.real * 16807
        elif self.coord.real == 0:
            self.geologi = self.coord.imag * 48271
        else:
            self.geologi = (REGIONS[self.coord-1].erosion *
                            REGIONS[self.coord-1j].erosion)

    def __set_erosion(self):
        self.erosion = (self.geologi + DEPTH) % 20183

    def __set_type(self):
        self.type = TYPES[self.erosion]


def make_regions(mouth=0+0j, target=TARGET):
    for x in range(target.real+1):
        for y in range(target.imag+1):
            coord = x + y * 1j
            REGIONS[coord] = Region(coord)


if __name__ == '__main__':
    TYPES = {0: ("rocky", "."), 1: ("wet", "="), 2: ("narrow", "|")}
    SPECIALS = ["mouth", "target"]

    # testing
    REGIONS = {}
    DEPTH = 510
    TARGET = 10+10j
    make_regions()
    assert sum([r.erosion for r in REGIONS]) == 114


    # puzzle
    REGIONS = {}
    DEPTH = 11109
    TARGET = 9+731j  # risk grid has 6579 regions

    make_regions()

    pt1 = sum([r.erosion for r in REGIONS])
    pt2 = None

    print(f"Part 1: {pt1}")
    print(f"Part 1: {pt1}")