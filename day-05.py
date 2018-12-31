""" Part One """

def get_polymer():
    with open('day-05.txt') as file:
        polymer = file.read().strip()

    return polymer


def catalyze_reaction(polymer):
    reaction = list(polymer)

    i = 0
    j = 1
    while j < len(reaction):
        if reaction[i] == 0 and i > 0:
            i += -1
        elif (reaction[i] == 0 and i == 0) or reaction[i].swapcase() != reaction[j]:
            i = j
            j += 1
        else:  # reaction!
            reaction[i] = 0
            reaction[j] = 0
            j += 1
            if i == 0:
                i = j
                j += 1
            else:
                i += -1

    return reaction


def collapse_product(reaction):
    product = ''.join([unit for unit in reaction if unit != 0])
    return product
