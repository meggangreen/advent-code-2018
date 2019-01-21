
# {o: sum(map(lambda x: x.count(o), ls)) for o in opts}

test_0 = """.#.#...|#.
.....#|##|
.|..|...#.
..|#.....#
#.#|||#|#|
...#.||...
.|....|...
||...#|.#|
|.||||..|.
...#.|..|."""

test_1 = """.......##.
......|###
.|..|...#.
..|#||...#
..##||.|#|
...#||||..
||...|||..
|||||.||.|
||||||||||
....||..|."""

test_2 = """.......#..
......|#..
.|.|||....
..##|||..#
..###|||#|
...#|||||.
|||||||||.
||||||||||
||||||||||
.|||||||||"""

test_3 = """.......#..
....|||#..
.|.||||...
..###|||.#
...##|||#|
.||##|||||
||||||||||
||||||||||
||||||||||
||||||||||"""

test_4 = """.....|.#..
...||||#..
.|.#||||..
..###||||#
...###||#|
|||##|||||
||||||||||
||||||||||
||||||||||
||||||||||"""

test_5 = """....|||#..
...||||#..
.|.##||||.
..####|||#
.|.###||#|
|||###||||
||||||||||
||||||||||
||||||||||
||||||||||"""

# After 6 minutes:
# ...||||#..
# ...||||#..
# .|.###|||.
# ..#.##|||#
# |||#.##|#|
# |||###||||
# ||||#|||||
# ||||||||||
# ||||||||||
# ||||||||||

# After 7 minutes:
# ...||||#..
# ..||#|##..
# .|.####||.
# ||#..##||#
# ||##.##|#|
# |||####|||
# |||###||||
# ||||||||||
# ||||||||||
# ||||||||||

# After 8 minutes:
# ..||||##..
# ..|#####..
# |||#####|.
# ||#...##|#
# ||##..###|
# ||##.###||
# |||####|||
# ||||#|||||
# ||||||||||
# ||||||||||

# After 9 minutes:
# ..||###...
# .||#####..
# ||##...##.
# ||#....###
# |##....##|
# ||##..###|
# ||######||
# |||###||||
# ||||||||||
# ||||||||||

test_10 = """.||##.....
||###.....
||##......
|##.....##
|##.....##
|##....##|
||##.####|
||#####|||
||||#|||||
||||||||||"""

COVER = '|.#'

ADJ8 = [-1-1j, 0-1j, 1-1j,
        -1-0j, 1+0j,
        -1+1j, 0+1j, 1+1j]

ACRES = {}

def define_acres(puzzle_input):
    for i, row in enumerate(puzzle_input.split("\n")):
        for j, char in enumerate(row):
            ACRES[j-i*1j] = char

    return ACRES


def calc_resource_value():
    vals = ''.join(ACRES.values())
    coverage = {char: vals.count(char) for char in COVER}
    return coverage, coverage['|'] * coverage['#']


def my_adjacents(my_position):
    adj8 = []
    for adj in ADJ8:
        acre = ACRES.get(my_position+adj)
        if acre:
            adj8.append(acre)

    return adj8


def new_minute_new_me(my_position):
    """ Rules:
        - open to wood if three+ adjacents are wood, else no change
        - wood to yard if three+ adjacents are yard, else no change
        - yard to yard if 1+ adjacent is yard and 1+ adjacent is wood, else to open
            ^^^ yard to open if no adjacents are yard nor wood, else no change
    """

    me = ACRES[my_position]
    my_adj8 = my_adjacents(my_position)

    if me == '.' and my_adj8.count('|') >= 3:
        me = '|'
    elif me == '|' and my_adj8.count('#') >= 3:
        me = '#'
    elif me == '#' and ('#' not in my_adj8 or '|' not in my_adj8):
        me = '.'

    return me


def new_acres_is_the_place_to_be():
    new_acres = {}
    for position in ACRES:
        new_acres[position] = new_minute_new_me(position)

    return new_acres


if __name__ == '__main__':
    puzzle_input = test_0
    ACRES = define_acres(puzzle_input)
    for m in range(10):
        ACRES = new_acres_is_the_place_to_be()

    assert calc_resource_value()==({'|': 37, '.': 32, '#': 31}, 1147)


    print("\n\n\n\n")
    print("Starting Calculations")

    with open('day-18.txt') as file:
        puzzle_input = file.read()

    ACRES = define_acres(puzzle_input)
    for m in range(10):
        ACRES = new_acres_is_the_place_to_be()

    print("P1:", calc_resource_value())

    ACRES = define_acres(puzzle_input)
    for m in range(468):
        ACRES = new_acres_is_the_place_to_be()

    print("P2:", calc_resource_value())


    """ Searched for some hints on reddit:

    ACRES = define_acres(puzzle_input)
    results = set()
    for m in range(500):
        ACRES = new_acres_is_the_place_to_be()
        result = calc_resource_value()
        acs = tuple([f"{k}:{str(v)}" for k, v in result[0].items()])
        if acs in results:
            print("repeat!", m+1, acs, result[1])
        if m+1 >= 400:  # after finding the first repeated sequence
            results.add(acs)

    # first sequence repeat was at 444
    # then I manually checked how often it repeated - every 28
    # (1000000000 - 444) % 28
    # >> 24
    # 444 + 24
    # >> 468
    # what was the stdout for 468? 177004

    """

