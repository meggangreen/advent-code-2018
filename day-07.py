""" Part One """
# tree
# DFS in alpha order?
# given a list of -edges-
# find root -- no parent
# traverse

from collections import OrderedDict, deque  #defaultdict
# import json
import re

def construct_trees_by_TingYu(edges):
    """ https://gist.github.com/aethanyc/8313640 """
    """Given a list of edges [parent, child], return trees. """
    # trees = defaultdict(dict)

    for parent, child in edges:
        if not trees.get(child):
            trees[child] = {'Parents': set(), 'Children': set()}
        trees[child]['Parents'].add(parent)
        if not trees.get(parent):
            trees[parent] = {'Parents': set(), 'Children': set()}
        trees[parent]['Children'].add(child)
        # trees[parent][child] = trees[child]

    # Find roots
    parents, children = zip(*edges)
    roots = set(parents).difference(children)
    leaves = set(children).difference(parents)

    print(roots, leaves)

    return roots, trees

    # return {root: trees[root] for root in roots}

def get_edges():
    pattern = re.compile(r"Step (\w) must be finished before step (\w)")
    # Step A must be finished before step I can begin.

    with open('day-07.txt') as file:
        edges = [pattern.match(edge).groups() for edge in file.readlines()]

    return edges