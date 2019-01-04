""" Part One """
from collections import deque

class Node(object):
    def __init__(self, header):
        """ header as tuple (num children, num metadata) """
        self.header = header
        self.children = None
        self.metadata = None

    def add_child(self, child):
        """ child as node """
        if not self.children:
            self.children = []
        self.children.append(child)

    def add_metadata(self, metadata):
        """ metadata as list """
        self.metadata = metadata


class Tree(object):
    def __init__(self, root):
        """ root as node """
        self.root = root


    def get_meta_sum(self):
        meta_sum = 0
        relations = [self.root]
        while relations:
            node = relations.pop()
            meta_sum += 0 if not node.metadata else sum(node.metadata)
            if node.children:
                relations.extend(node.children)

        return meta_sum


def get_input_dq():
    with open('day-08.txt') as file:
        input_dq = deque([int(n) for n in file.read().strip().split()])

    return input_dq


def construct_tree(input_dq):
    return Tree(construct_node(input_dq))


def construct_node(input_dq):
    if len(input_dq) < 2:
        return None

    num_children, num_metadata = input_dq.popleft(), input_dq.popleft()
    node = Node((num_children, num_metadata))

    # get children
    for i in range(num_children):
        child = construct_node(input_dq)
        node.add_child(child)

    # get metadata
    metadata = []
    for i in range(num_metadata):
        metadata.append(input_dq.popleft())
    node.add_metadata(metadata)

    return node


""" Part Two """
def get_node_value(node):
    value = 0
    if not node.children:
        value += sum(node.metadata)
    else:
        for m in node.metadata:
            if 0 < m <= len(node.children):
                value += get_node_value(node.children[m-1])

    return value
