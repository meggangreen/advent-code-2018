""" Part One """
def get_changes():

    with open('day-01.txt') as file:
        changes = file.readlines()

    for i, change in enumerate(changes):
        changes[i] = int(change.strip())

    return changes


def get_final_frequency():
    return sum(get_changes())


""" Part Two """
def get_first_duplicate():
    changes = get_changes()
    freqs = set([0])
    curr = 0
    dupe = False

    while dupe is False:
        for change in changes:
            curr += change
            if curr not in freqs:
                freqs.add(curr)
            else:
                dupe = True
                return curr
