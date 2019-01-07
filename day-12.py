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



""" reddit sophiebits, changed for readability and python3"""
# this question was supremely badly worded.

# from reading the reddit solution megathread, i shouldn't have wrapped the pots
# and i should have kept adding plants on.

# for part two, i needed to get my own pattern number -- 15 instead of 38. it
# converged slightly quicker also -- 90 gens instead of 97.

def nextg(cur, recipe):
    start = min(cur)
    end = max(cur)
    x = set()

    for i in range(start - 3, end + 4):
        pat = ''.join('#' if i + k in cur else '.' for k in [-2, -1, 0, 1, 2])
        if pat in recipe:
            x.add(i)

    return x

def viz(cur):
    print(''.join('#' if i in cur else '.' for i in range(-5, 120)))

with open('day-12.txt') as file:
    lines = [line.strip() for line in file]
    # print(lines)

init = lines[0][len('initial state: '):]
recipe = set()
for line in lines[2:]:
    if line[-1] == '#':
        recipe.add(line[:5])

# Part 1:
cur = set(i for i, c in enumerate(init) if c == '#')
for i in range(20):
    cur = nextg(cur, recipe)
cur = sum(cur)
print("Part One: {}".format(cur))

# Part 2:
pattern = (50000000000 - 100) * 15  # my input adds 15 each gen
cur = set(i for i, c in enumerate(init) if c == '#')
# ls = 0
# viz(cur)
for i in range(100):
    cur = nextg(cur, recipe)
    # viz(cur)
    # s = sum(cur)
    # print(i, s, s - ls)
    # ls = s
cur = sum(cur)
cur += pattern
print("Part Two: {}".format(cur))