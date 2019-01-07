""" Part One """
from collections import deque

def get_initial_pots():
    with open('day-12.txt') as file:
        pots = deque([pot for pot in file.readlines()[0].strip()[15:]])
    return pots


def get_rules():
    s = ' => '
    with open('day-12.txt') as file:
        lines = [line.strip().split(s) for line in file.readlines()[2:]]
        rules = {combo: rule for combo, rule in lines}

    return rules


def one_generation(pots, rules):
    new_pots = deque()

    for i in range(len(pots)):
        combo = ''.join([pots[c] for c in range(-2, 3)])
        new_pots.append(rules[combo])
        pots.rotate(-1)

    return new_pots


def multi_generations(num):
    rules = get_rules()
    pots = get_initial_pots()

    for n in range(num):
        pots = one_generation(pots, rules)

    return pots


def get_plant_sum(gens):
    pots = multi_generations(gens)
    return sum([i for i, p in enumerate(pots) if p == '#'])
