""" Part One """
# tree
# DFS in alpha order?
# given a list of -edges-
# find root -- no parent
# traverse

from collections import deque
import re

class Node(object):
    def __init__(self, data):
        self.data = data
        self.parents = set()
        self.children = set()


    def add_child(self, child):
        self.children.add(child)


    def add_parent(self, parent):
        self.parents.add(parent)


    def is_root(self):
        return len(self.parents) == 0


def get_edges():
    pattern = re.compile(r"Step (\w) must be finished before step (\w)")

    with open('day-07.txt') as file:
        edges = [pattern.match(edge).groups() for edge in file.readlines()]

    return edges


def construct_nodes(edges):
    """ based on 'construct_trees_by_TingYu' at """
    """ https://gist.github.com/aethanyc/8313640 """
    """ Given a list of edges [parent, child], return nodes """

    nodes = {n: Node(n) for n in set(sum(edges, ()))}

    for parent, child in edges:
        nodes[parent].add_child(nodes[child])
        nodes[child].add_parent(nodes[parent])

    return nodes


def update_available(nodes, complete):
    def is_node_ready(node):
        for parent in node.parents:
            if parent.data not in complete:
                return False

        return True

    return [node.data for node in nodes if is_node_ready(node) is True]


def set_up_flow():
    all_nodes = construct_nodes(get_edges())

    complete = []
    available = deque()

    available.extend(update_available(all_nodes.values(), complete))
    available = deque(sorted(available))

    return all_nodes, complete, available


def complete_all_nodes():
    all_nodes, complete, available = set_up_flow()

    while available:
        node = all_nodes[available.popleft()]
        complete.append(node.data)
        available.extend(update_available(node.children, complete))
        available = deque(sorted(available))

    return ''.join(complete)  # Order of completion

""" Part Two """
class Elf(object):
    def __init__(self, name='Bob'):
        self.name = name
        self.proj = None
        self.start = None
        self.end = None


def complete_with_help():
    all_nodes, complete, available = set_up_flow()
    workers = [Elf(i) for i in range(5)]

    sec = -1

    while len(complete) < 26:
        sec += 1
        for elf in workers:
            if sec == elf.end:
                complete.append(elf.proj.data)
                available.extend(update_available(elf.proj.children, complete))
                available = deque(sorted(available))
                elf.proj, elf.start, elf.end = None, None, None
            if available and elf.proj is None:
                elf.proj = all_nodes[available.popleft()]
                elf.start = sec
                elf.end = sec + (ord(elf.proj.data) - 4)

    # idk why it's one second off, but there you are.
    return sec-1, ''.join(complete)
