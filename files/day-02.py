""" Part One """
def get_boxids():
    with open('day-02.txt') as file:
        boxids = [boxid.strip() for boxid in file.readlines()]

    return boxids

def parse_boxids():
    boxids = get_boxids()
    two_let = set([])
    three_let = set([])
    letters = {}

    for boxid in boxids:
        letters.clear()
        for letter in boxid:
            letters[letter] = letters.get(letter, 0) + 1
        for letter, count in letters.items():
            if count == 2 and boxid not in two_let:
                two_let.add(boxid)
            if count == 3 and boxid not in three_let:
                three_let.add(boxid)

    return (two_let, three_let)


def calc_checksum():
    two_let, three_let = parse_boxids()
    return len(two_let) * len(three_let)


""" Part Two """
def get_matching_boxid():
    from difflib import SequenceMatcher

    boxids = get_boxids()
    idx = None

    for b in range(len(boxids)):
        for c in range(b+1, len(boxids)):
            # difflib SM docs: https://docs.python.org/3.7/library/difflib.html#difflib.SequenceMatcher
            matches = SequenceMatcher(None, boxids[b], boxids[c]).get_matching_blocks()
            if len(matches) == 3 and matches[0][2] + matches[1][2] == 25:
                idx = matches[1][0]
                boxid = boxids[b][0:idx] + boxids[b][idx:]

    return boxid

