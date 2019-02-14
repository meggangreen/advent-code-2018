""" Parts One and Two """
import re
import pdb

TELA = [[0]*1000 for x in range(1000)]

CLAIM_IDS = set([])
DUPE_IDS = set([])
DUPE_INCHES = set([])

def get_claims():
    pattern = re.compile(r"#(\d+) @ (\d+),(\d+): (\d+)x(\d+)\s")

    with open('day-03.txt') as file:
        claims = [pattern.match(raw).groups() for raw in file.readlines()]

    return claims


def process_claims(num=None):
    claims = get_claims()
    for claim in claims[:num]:
        CLAIM_IDS.add(int(claim[0]))
        draw_claim(claim)


def draw_claim(claim):
    cid, col, row, width, height = (int(n) for n in claim)
    for w in range(width):
        for h in range(height):
            if TELA[col+w][row+h] == 0:
                TELA[col+w][row+h] = [cid]
            elif TELA[col+w][row+h] != 0:
                TELA[col+w][row+h].append(cid)
                DUPE_INCHES.add((col+w, row+h))
                DUPE_IDS.update(TELA[col+w][row+h])


def count_duplicate_inches():
    return len(DUPE_INCHES)


def get_nonduplicate_claim():
    return CLAIM_IDS - DUPE_IDS
