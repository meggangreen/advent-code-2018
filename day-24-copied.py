""" Needed for Part 2
    reddit pbfy0 https://www.reddit.com/r/adventofcode/comments/a91ysq/2018_day_24_solutions/ecfz0e4
"""

import re

inp_imm = """89 units each with 11269 hit points (weak to fire, radiation) with an attack that does 1018 slashing damage at initiative 7
371 units each with 8033 hit points with an attack that does 204 bludgeoning damage at initiative 15
86 units each with 12112 hit points (immune to slashing, bludgeoning; weak to cold) with an attack that does 1110 slashing damage at initiative 18
4137 units each with 10451 hit points (weak to slashing; immune to radiation) with an attack that does 20 slashing damage at initiative 11
3374 units each with 6277 hit points (weak to slashing, cold) with an attack that does 13 cold damage at initiative 10
1907 units each with 1530 hit points (immune to fire, bludgeoning; weak to radiation) with an attack that does 7 fire damage at initiative 9
1179 units each with 6638 hit points (immune to radiation; weak to slashing, bludgeoning) with an attack that does 49 fire damage at initiative 20
4091 units each with 7627 hit points with an attack that does 17 bludgeoning damage at initiative 17
6318 units each with 7076 hit points with an attack that does 8 bludgeoning damage at initiative 2
742 units each with 1702 hit points (weak to radiation; immune to slashing) with an attack that does 22 radiation damage at initiative 13"""

inp_infection = """3401 units each with 31843 hit points (weak to cold, fire) with an attack that does 16 slashing damage at initiative 19
1257 units each with 10190 hit points with an attack that does 16 cold damage at initiative 8
2546 units each with 49009 hit points (weak to bludgeoning, radiation; immune to cold) with an attack that does 38 bludgeoning damage at initiative 6
2593 units each with 12475 hit points with an attack that does 9 cold damage at initiative 1
2194 units each with 25164 hit points (weak to bludgeoning; immune to cold) with an attack that does 18 bludgeoning damage at initiative 14
8250 units each with 40519 hit points (weak to bludgeoning, radiation; immune to slashing) with an attack that does 8 bludgeoning damage at initiative 16
1793 units each with 51817 hit points (immune to bludgeoning) with an attack that does 46 radiation damage at initiative 3
288 units each with 52213 hit points (immune to bludgeoning) with an attack that does 339 fire damage at initiative 4
22 units each with 38750 hit points (weak to fire) with an attack that does 3338 slashing damage at initiative 5
2365 units each with 25468 hit points (weak to radiation, cold) with an attack that does 20 fire damage at initiative 12"""


class group:

    def __init__(self, n, hp_each, weaknesses, immunities, atk_dmg, atk_type, initiative, team):
        self.n = n
        self.hp_each = hp_each
        self.weaknesses = weaknesses
        self.immunities = immunities
        self.atk_dmg = atk_dmg
        self.atk_type = atk_type
        self.initiative = initiative
        self.team = team

    def __repr__(self):
        return 'group({!r})'.format(self.__dict__)

    @property
    def eff_power(self):
        return self.n * self.atk_dmg

    def dmg_to(self, other):
        return self.eff_power * (0 if self.atk_type in other.immunities else 2 if self.atk_type in other.weaknesses else 1)


def parse(st, team, boost=0):
    res = []
    for i in st.split('\n'):
        g = re.match(r'(\d+) units each with (\d+) hit points (?:\((.*?)\) )?with an attack that does (\d+) (\S+) damage at initiative (\d+)', i)
        n = int(g.group(1))
        hp = int(g.group(2))
        weaknesses = set()
        immunities = set()
        wi = g.group(3)
        if wi is not None:
            for cmp in wi.split('; '):
                if cmp.startswith('immune to '):
                    immunities |= set(cmp[len('immune to '):].split(', '))
                elif cmp.startswith('weak to '):
                    weaknesses |= set(cmp[len('weak to '):].split(', '))
        dmg = int(g.group(4))
        typ = g.group(5)
        initiative = int(g.group(6))
        res.append(group(n, hp, weaknesses, immunities, dmg + boost, typ, initiative, team))
    return res


def get_team(s):
    if s is None: return 'stalemate'
    for i in s:
        return i.team


def run_combat(imm_inp, inf_inp, boost=0):
    immune_system = set(parse(imm_inp, 'immune', boost))
    infection = set(parse(inf_inp, 'infection'))
    while immune_system and infection:
        potential_combatants = immune_system | infection
        attacking = {}
        for combatant in sorted(immune_system | infection, key=lambda x: (x.eff_power, x.initiative), reverse=True):
            try:
                s = max((x for x in potential_combatants if x.team != combatant.team and combatant.dmg_to(x) != 0), key=lambda x: (combatant.dmg_to(x), x.eff_power, x.initiative))
            except ValueError as e:
                attacking[combatant] = None
                continue
            potential_combatants.remove(s)
            attacking[combatant] = s
        did_damage = False
        for combatant in sorted(immune_system | infection, key=lambda x: x.initiative, reverse=True):
            if combatant.n <= 0:
                continue
            atk = attacking[combatant]
            if atk is None: continue
            dmg = combatant.dmg_to(atk)
            n_dead = dmg // atk.hp_each
            if n_dead > 0: did_damage = True
            atk.n -= n_dead
            if atk.n <= 0:
                immune_system -= {atk}
                infection -= {atk}

        if not did_damage: return None
        #print('NEW ROUND')
        #print('immune_system', immune_system)
        #print('infection', infection)
    winner = max(immune_system, infection, key=len)
    return winner

winner = run_combat(inp_imm, inp_infection)
print('Part 1:', sum(x.n for x in winner))

boost_min = 0
boost_max = 1
while get_team(run_combat(inp_imm, inp_infection, boost_max)) != 'immune':
    boost_max *= 2
    #print(boost_max)

import math
while boost_min != boost_max:
    pow = (boost_min + boost_max) // 2
    cr = run_combat(inp_imm, inp_infection, pow)
    res = get_team(cr)
    if res != 'immune':
        boost_min = math.ceil((boost_min + boost_max) / 2)
    else:
        boost_max = pow
    #print(boost_min, boost_max)
print('Boost:', boost_max)
print('Part 2:', sum(x.n for x in run_combat(inp_imm, inp_infection, boost_max)))