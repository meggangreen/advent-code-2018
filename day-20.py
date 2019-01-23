""" Let's make some trees """

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


class Route:
    """ The tree of Sections """

    def __init__(self, root):
        self.root = root


    def find_most_doors_no_repeat(self):
        def walk_through_doors(section):

            section = self.root

