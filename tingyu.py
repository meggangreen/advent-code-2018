from collections import defaultdict
import json

def construct_trees_by_TingYu(edges):
    """ https://gist.github.com/aethanyc/8313640 """
    """Given a list of edges [child, parent], return trees. """
    trees = defaultdict(dict)

    for child, parent in edges:
        trees[parent][child] = trees[child]

    # Find roots
    children, parents = zip(*edges)
    roots = set(parents).difference(children)

    print(trees)

    return {root: trees[root] for root in roots}

if __name__ == '__main__':
    edges = [[0, 6], [17, 5], [2, 7], [4, 14], [12, 9], [15, 5], [11, 1], [14, 8], [16, 6], [5, 1], [10, 7], [6, 10], [8, 2], [13, 1], [1, 12], [7, 1], [3, 2], [19, 12], [18, 19]]
    print(json.dumps(construct_trees_by_TingYu(edges), indent=4))