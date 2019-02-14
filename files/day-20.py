""" Let's make some trees """
# this is "implement jsonify"

import re
from collections import deque

# class Section:
#     """ A section of the route in which there are no deviations -- ie each node,
#         a letter, has only one child -- because I think it will save in counting.
#         'children' is a list of Sections.

#     """

#     def __init__(self, doors): #, start, children=None):
#         self.data = doors
#         # self.start = float('inf') * -1
#         # self.len = len(self.data)
#         self.children = None


#     def locate(self, start):
#         self.start = start


#     def adopt(self, children):
#         if not self.children:
#             self.children = []
#         self.children.extend(children)
#         # self.children.sort(key=lambda child: child.start)


# class Route:
#     """ The tree of Sections """

#     def __init__(self, root):
#         self.root = root


#     def find_most_doors_no_repeat(self, to_visit=None):
#         """ DFS shortest path to farthest end """

#         path = deque()
#         doors = 0

#         if not to_visit:
#             to_visit = [self.root]

#         while to_visit:
#             section = to_visit.pop()

#             if section.children:
#                 to_visit.extend(section.children)
#                 route = Route(section)
#                 doors += route.find_most_doors_no_repeat(to_visit)

#             else:
#                 import pdb; pdb.set_trace()
#                 path.appendleft(section)
#                 doors += section.len
#                 return doors





#         def walk_through_doors(section):
#             pass


def remove_skip(puzzle_in):
    match = re.search(skip, puzzle_in)
    if match:
        puzzle_in = puzzle_in[:match.span()[0]] + puzzle_in[match.span()[1]:]

    return puzzle_in


# def find_next_closer(puzzle_in):
#     match = re.search(closer, puzzle_in)
#     if match:
#         return match.start()


# def find_last_closer(puzzle_in):
#     matches = [m for m in re.finditer(closer, puzzle_in)]
#     if matches:
#         return matches[-1].start()


# def find_penult_closer(puzz_in):
#     matches = [m for m in re.finditer(closer, puzzle_in)]
#     if matches:
#         return matches[-2].end()


# def find_opener(puzzle_in):
#     match = re.search(opener, puzzle_in)
#     if match:
#         return match.end()  # + 1


# def explore(puzzle_in):
#     sections = []

#     # if there is a path to skip, skip it
#     if puzzle_in[-1] == '|':
#         return

#     start = find_opener(puzzle_in)
#     if not start:
#         sections.extend([Section(r) for r in puzzle_in.split('|')])

#     else:
#         # import pdb; pdb.set_trace()
#         # this is not finding my last ')'
#         end = find_last_closer(puzzle_in)
#         to_explore = puzzle_in[start:end]
#         sections.extend([Section(r) for r in puzzle_in[:start-1].split('|')])
#         parent = sections.pop()
#         if parent == 'EEN':
#             print("\n\n\nPARENT: EEN\n\n\n")
#             # import pdb; pdb.set_trace()
#         parent.adopt(explore(to_explore))
#         sections.append(parent)

#     return sections


# def balance_parens(puzz_in):

#     sections = []
#     start = None
#     end = -1

#     for i, p in enumerate(puzz_in):
#         if p == '(':
#             import pdb; pdb.set_trace()
#             start = end + 1  # 0 if not end else end + 1
#             end = i
#             sections.append(puzz_in[start:end])
#         if p == ')':
#             import pdb; pdb.set_trace()
#             start = end + 1
#             end = i
#             children = [Section(char) for char in puzz_in[start:end].split('|')]
#             # only gets preceeding parents
#             parent_level = [Section(char) for char in sections.pop().split('|')]
#             parent_level[-1].adopt(children)


# def make_edges_list(puzz_in, i=0):
#     sections = []
#     children = []
#     mid = -1

#     start = mid + 1
#     mid = find_opener(puzz_in)
#     dle = find_penult_closer(puzz_in)
#     end = find_last_closer(puzz_in)

#     before = puzz_in[start:mid]
#     after = puzz_in[dle:end]

#     for b in before.split('|'):
#         i += 1
#         sections.append(Section(str(i), sect))

#     for group in (before, after):
#         next_level = puzz_in[mid+1:dle]
#         for g in group.split('|')
#     to_section = before.split('|')
#     for sect in to_section:
#         i += 1
#         sections.append(Section(str(i), sect))

#     children, i = make_edges_list(next_level, i)
#     sections[-1].adopt(children)

#     to_section = after.split('|')
#     for sect in to_section:
#         if sect:
#             i += 1
#             sections.append(Section(str(i), sect))

#     return sections, i

class Node:
    def __init__(self, data):
        self.data = data
        self.children = []


def parse_nested_string(puzzle_input):
    # returns list of lists

    symbs = '(|)'
    if not puzzle_input:
        return []

    result = []
    node = None

    i = -1
    # import pdb; pdb.set_trace()
    while i < len(puzzle_input):
        i += 1

        if puzzle_input[i] not in symbs:
            if not node:
                node = Node(puzzle_input[i])
                result.append(node)
            else:
                child = Node(puzzle_input[i])
                node.children.append(child)
                node = child
            # key = str(i)  # puzzle_input[i]
            # if key:

        elif puzzle_input[i] == '(':
            # key = ''.join(key)
            result.append(parse_nested_string(puzzle_input[i+1:]))
            # result.append({key: value})
            # key = []

        elif puzzle_input[i] == '|':
            # if puzzle_input[i+1] == ')':
            #     key = []
            #     return result
            #     # i += 1
            #     continue
            node = None
            # key = ''.join(key)
            # value = []
            # result.append({key: value})
            # key = []

        elif puzzle_input[i] == ')':
            key = ''.join(key)
            value = []
            result.append({key: value})
            key = []
            return result







###################

if __name__ == '__main__':
    skip = re.compile(r'\([\w\|]+\|\)')
    opener = re.compile(r'\(')
    closer = re.compile(r'\)')  # re.compile(r'\)[\w]*$')
    level = '()'

    with open('day-20.txt', 'r') as file:
        puzzle_input = file.read().strip()[1:-1]

    # get rid of optional paths early
    # print(len(puzzle_input))  # 14323
    while True:
        puzzle_length = len(puzzle_input)
        puzzle_input = remove_skip(puzzle_input)
        if puzzle_length == len(puzzle_input):
            break
    with open('day-20-clean.txt', 'w') as file:
        file.write(puzzle_input)
    # print(len(puzzle_input))  # 11418

    # root = explore(puzzle_input)[0]
    # route = Route(root)
