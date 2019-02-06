""" Notes

    Oh good, another grid. I can do this one, I know it.

    DEPTH
    TYPES = {0: ("rocky", "."), 1: ("wet", "="), 2: ("narrow", "|")}
    SPECIALS = ["mouth", "target"]

    regions = {coord, Region}

    region.title None or a special
    region.type TYPES[r.erosion]
    region.coord (x+yj) -- x and y >= 0
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

    risk = sum([r.erosion for r in regions if (r.coord.real <= t.coord.real and
                                               r.coord.imag <= t.coord.imag)])

"""