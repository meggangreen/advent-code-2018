""" Let's make some trees """

import re
from collections import deque

class Section(str):
    """ A section of the route in which there are no deviations -- ie each node,
        a letter, has only one child -- because I think it will save in counting.
        'children' is a list of Sections.

    """

    def __init__(self, doors): #, start, children=None):
        super().__init__()
        self.start = float('inf') * -1
        self.len = self.__len__()
        self.children = None


    def locate(self, start):
        self.start = start


    def adopt(self, children):
        if not self.children:
            self.children = []
        self.children.extend(children)
        self.children.sort(key=lambda child: child.start)


class Route:
    """ The tree of Sections """

    def __init__(self, root):
        self.root = root


    def find_most_doors_no_repeat(self):
        """ DFS shortest path to farthest end """

        section = self.root
        path = [section]
        to_visit = deque(section.children)

        # for section in to_visit:


        def walk_through_doors(section):
            pass


""" Part One is just easier to do in regex """
skip = re.compile(r'\([\w\|]+\|\)')
opener = re.compile(r'\(')
closer = re.compile(r'\)[\w]*$')
level = '()'

with open('day-20.txt', 'r') as file:
    route = file.read().strip()[1:-1]

def remove_skip(route):
    match = re.search(skip, route)
    if match:
        route = route[:match.span()[0]] + routeroute[match.span()[1]:]

    return route


def find_closer(route):
    match = re.search(closer, route)
    if match:
        return match.span()[0]


def find_opener(route):
    match = re.search(opener, route)
    if match:
        return match.span()[0] + 1


def explore(route):

    # while True:
    #     length = len(route)
    #     route = remove_skip(route)
    #     if length == len(route):
    #         break

    doors = 0

    if route[-1] == '|':
        return doors

    start = find_opener(route)
    if start:
        end = find_closer(route)
        route = route[start:end]
        doors += explore(route)

    doors


    r = 0
    while r < len(route):
        if route[r] in 'NESW':
            doors += 1
        elif route[r] == '(':
        elif route[r] == ')':
            # should not arrive?
            break
        # elif route[r] == '|' and route[r+1] == ')':
        #     doors = 0
        #     break

    return doors
