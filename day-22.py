""" Notes

    Oh good, another grid. I can do this one, I know it.

    Part 2 help from the best redditor ever korylprince:
    https://www.reddit.com/r/adventofcode/comments/a8i1cy/2018_day_22_solutions/ecazvbe

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

import networkx as nx
from copy import deepcopy

class Region:
    def __init__(self, coord):
        self.coord = coord
        self.title = None
        self.geologi = None
        self.erosion = None
        self.terrain = None

        self.__set_title()
        self.__set_geologi()
        self.__set_erosion()
        self.__set_terrain()

    def __set_title(self):
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
            self.geologi = (CAVE.nodes[self.coord-1]['erosion'] *
                            CAVE.nodes[self.coord-1j]['erosion'])

    def __set_erosion(self):
        self.erosion = (self.geologi + DEPTH) % 20183

    def __set_terrain(self):
        self.terrain = self.erosion % 3


def graph_cave_regions(upp_bound):
    for y in range(int(upp_bound.imag+1)):
        for x in range(int(upp_bound.real+1)):
            coord = x + y * 1j
            region = Region(coord)
            CAVE.add_node(coord,
                          coord=region.coord,
                          title=region.title,
                          geologi=region.geologi,
                          erosion=region.erosion,
                          terrain=region.terrain)


################################################################################

if __name__ == '__main__':
    TERRAINS = {0: ("rocky", "."), 1: ("wet", "="), 2: ("narrow", "|")}
    SPECIALS = ["mouth", "target"]

    MOUTH = 0+0j

    # testing
    CAVE = nx.Graph()
    DEPTH = 510
    TARGET = 10+10j
    graph_cave_regions(TARGET)
    assert sum([CAVE.nodes[r]['terrain'] for r in CAVE.nodes]) == 114


    # puzzle
    CAVE = nx.Graph()
    DEPTH = 11109
    TARGET = 9+731j  # risk grid has 6579 regions
    graph_cave_regions(TARGET)

    pt1 = sum([CAVE.nodes[r]['terrain'] for r in CAVE.nodes])  # 7299


    pt2 = len(nx.shortest_path(CAVE, source=MOUTH, target=TARGET))  # 1008

    print(f"Part 1: {pt1}")
    print(f"Part 2: {pt2}")
