""" Parts One and Two """
# puzzle input: '793031'

""" I thought that this was a time in which there would be some "tricky"
    way to solve this -- but actually the voted-best solution on reddit was the
    brute force solution. So now I'm a little sad I didn't just write my own =/
    I modified the copied version (reddit Jead) a bit so that it would work for
    smaller recipe numbers.
"""

recipes = '793031'

def find_scores(recipes):
    n = len(recipes) + 1
    score = '37'
    elf1 = 0
    elf2 = 1

    while len(score) < int(recipes) + 10 or recipes not in score[-n:]:
        score += str(int(score[elf1]) + int(score[elf2]))
        elf1 = (elf1 + int(score[elf1]) + 1) % len(score)
        elf2 = (elf2 + int(score[elf2]) + 1) % len(score)

    print('P1: ', score[int(recipes):int(recipes)+10])
    print('P2: ', score.index(recipes), len(score))
