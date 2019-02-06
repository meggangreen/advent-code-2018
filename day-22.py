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


def graph_cave_paths():
    """ I struggled with what the edges should be, how best to incorporate the tools. """

    for coord in CAVE.nodes:
        region = CAVE.nodes[coord]
        tools = TOOLS[region['terrain']]
        EDGES.add_edge((coord, tools[0]), (coord, tools[1]), weight=7)

        for adj in [-1, -1j]:  # north and west only -- looking ahead to south and east double-adds edges
            next_region = CAVE.nodes.get(coord + adj)
            if next_region:
                next_tools = set(TOOLS[next_region['terrain']])
                for tool in set(tools).intersection(next_tools):
                    EDGES.add_edge((coord, tool), (coord+adj, tool), weight=1)


################################################################################

if __name__ == '__main__':

    rocky, wet, narrow = 0, 1, 2
    torch, gear, neither = "t", "c", "n"
    TOOLS = {rocky: (torch, gear), wet: (gear, neither), narrow: (torch, neither)}

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


    CAVE = nx.Graph()
    EDGES = nx.Graph()
    graph_cave_regions(TARGET + 100+100j)  # expand cave knowledge in case of roundabout paths
    graph_cave_paths()

    # I generally know that Dijkstra's algorithm finds the shortest path from
    # the current node to an adjacent node (thanks amsowie!). So the long way to
    # implement this would be to find all the paths, and pick the shortest ... ?
    # Or is it like house robbing where picking the shortest at each chance _is_
    # the shortest?
    pt2 = nx.dijkstra_path_length(EDGES, (MOUTH, torch), (TARGET, torch))  # 1008

    print(f"Part 1: {pt1}")
    print(f"Part 2: {pt2}")
