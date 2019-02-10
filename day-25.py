""" Notes

in_constellation = True if manhattan distance is <= 3

"""

import networkx as nx
from day_25_test import test_inputs, test_results

def calc_manhattan_dist(coord1, coord2):
    return sum([abs(coord1[i] - coord2[i]) for i in range(len(coord1))])


def make_constellations(coords):
    constellations = nx.Graph()

    for c in range(len(coords)-1):
        constellations.add_node(coords[c])
        for i in range(c+1, len(coords)):
            constellations.add_node(coords[i])
            md = calc_manhattan_dist(coords[c], coords[i])
            if md <= 3:
                constellations.add_edge(coords[c], coords[i])

    return constellations


def get_coords(text):
    return [tuple(int(n) for n in line.split(',')) for line in text.split()]


################################################################################
if __name__ == '__main__':

    # testing
    for t, text in enumerate(test_inputs):
        coords = get_coords(text)
        constellations = make_constellations(coords)
        num_cons = len(list(nx.connected_components(constellations)))
        assert num_cons == test_results[t], print(t)


    with open('day-25.txt') as file:
        text = file.read()

    pt1 = len(list(nx.connected_components(make_constellations(get_coords(text)))))

    pt2 = "Finished!"

    print(f"Part 1: {pt1}\nPart 2: {pt2}")
