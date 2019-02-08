""" Notes

    side < army < group < unit, effective power

    side = immune sys or infection

    unit:
        - hit points: amount of damage withstood -- health
        - attack damage: amount of damage dealt -- damage
        - attack type: eg radiation, fire, cold, slashing, etc -- weapon
        - initiative: attack order and tie winner -- drive
        - weaknesses: attack types
        - immunities: attack types

    group:
        - units: [(quantity, unit)]
        - effective power: sum(unit_quantity * unit_attack_damage)
        - select_target(possible_targets)
        - attack_target(target)

    fight: 2 phases: target selection, attacking
        - target selection:
            in decreasing order of effective power, group targets enemy group to
            which it deals most damage, after accounting for weakness and immunity
                - each group has chosen up to 1 group to attack
                - each group is being attacked by up to 1 group
        - attacking:


"""

from queue import PriorityQueue
import re

# class Unit:
#     """ information for one unit """

#     def __init__(self, health, damage, weapon, weaknesses=None, immunities=None):
#         self.health = health
#         self.damage = damage
#         self.weapon = weapon
#         self.weaknesses = weaknesses
#         self.immunities = immunities

#     def __repr__(self):
#         health = f"H:{self.health}"
#         damage = f"D:{self.damage}"
#         weapon = self.weapon
#         # initi = f"I:{self.initiative}"
#         weak = self.weaknesses
#         immun = self.immunities

#         return f'<Unit {health} {damage} {weapon} {weak} {immun}>'


class Group:
    """ A Group is the smallest as a the trait for each unit can be extrapolated
        to the group. A unit is just 1 member who lives or is lost in an attack.
    """

    def __init__(self, banner, units, drive, health, damage, weapon, weaknesses=None,
                                                                     immunities=None):
        self.banner = banner
        self.units = units
        self.drive = drive  # self.drive  # * self.units
        self.health = health
        self.damage = damage
        self.weapon = weapon
        self.weaknesses = weaknesses if weaknesses else []
        self.immunities = immunities if immunities else []
        self._set_efficacy()

    def __repr__(self):
        return f'<G - {self.banner} - Units: {self.units} - Drive: {self.drive} - Effic: {self.efficacy} >'

    def _set_efficacy(self):
        self.efficacy = self.damage * self.units

    def _select_target(self, targets):
        """ called by Fight; returns the target """
        target_q = PriorityQueue()  # my new fave
        impact = 0
        for t in targets:
            if t.banner == self.banner:
                continue
            impact = self._calc_impact_on(t)
            target_q.put((-impact, -t.efficacy, -t.drive, t))

        target = None if target_q.empty() else target_q.get()[3]
        return target

    def _calc_impact_on(self, target):
        if self.units < 1:
            impact = 0
        else:
            impact = self.efficacy
            if self.weapon in target.immunities:
                impact += -self.efficacy
            elif self.weapon in target.weaknesses:
                impact += self.efficacy

        return impact

    def _defend(self, impact):
        """ updates units, drive, efficacy in an attack """
        self.units += -(impact // self.health)
        if self.units < 1:
            self.units = 0
            # print("group lost")
        self._set_efficacy()


class Army:
    """ Each side has an Army; each army has 1+ Groups """

    def __init__(self, banner, groups=None):
        self.banner = banner    # immune system or infection
        self.groups = groups if groups else set()

    def __repr__(self):
        groups = '\n    '.join([g.__repr__() for g in self.groups])
        return f'<Army {self.banner} with\n    {groups} />'

    def _exists(self):
        if not self.groups:
            # print(f"{self.banner} is no more.")
            return False

        for group in self.groups:
            if group.units < 1:
                self.groups.remove(group)

        return True


class Fight:
    """ A full turn of play. """

    def __init__(self, armies):
        self.armies = armies
        self.face_offs = {}

    def fight(self):
        self._select_targets()
        self._attack_targets()
        return self.armies

    def _select_targets(self):
        # get all groups
        groups = set([group for army in armies.values() for group in army.groups])
        # choose selection order -- a PQ!
        select_q = self._make_selection_queue(groups)
        # for each Group:
        while not select_q.empty():
            _, _, selector = select_q.get()
            # call G._select_target and pass avail targets
            target = selector._select_target(groups)
            if target:
                # add to face_offs
                self.face_offs[selector] = target
                # remove selected from avail
                groups.remove(target)

    def _make_selection_queue(self, groups):
        select_q = PriorityQueue()
        for group in groups:
            select_q.put((-group.efficacy, -group.drive, group))

        return select_q

    def _attack_targets(self):
        # get attack order
        attack_q = self._make_attack_queue()
        # carry out attacks
        while not attack_q.empty():
            _, offense = attack_q.get()
            defense = self.face_offs[offense]
            impact = offense._calc_impact_on(defense)
            # remove old defense
            self.armies[defense.banner].groups.remove(defense)
            # apply impact
            defense._defend(impact)
            # add modified defense if not lost
            if defense.units > 0:
                self.armies[defense.banner].groups.add(defense)

    def _make_attack_queue(self):
        attack_q = PriorityQueue()
        for offense in self.face_offs:
            attack_q.put((-offense.drive, offense))

        return attack_q


class Battle:
    """ A full game of Fights, with Armies. """

    def __init__(self, armies):
        self.armies = armies

    def fight(self):
        while True:
            lost = []
            for a, army in self.armies.items():
                if army._exists() is False:
                    lost.append(a)
            for a in lost:
                self.armies.pop(a)
            if len(self.armies) > 1:
                self.armies = Fight(self.armies).fight()
            elif len(self.armies) == 1:
                army = [army for army in armies.values()][0]
                units = sum([g.units for g in army.groups])
                return f"Winner: {army.banner} with {units} units."
            else:
                return "Everyone loses in war."



def parse_input(filepath):
    p_army = re.compile(r'(?<=^Army: )[\w\s]+(?=\n)')
    p_units = re.compile(r'^[\d]+(?= units)')
    p_health = re.compile(r'[\d]+(?= hit points)')
    p_weaks = re.compile(r'(?<=weak to )[\w,\s]+(?=[;|\)])')
    p_immuns = re.compile(r'(?<=immune to )[\w,\s]+(?=[;|\)])')
    p_damage_weapon = re.compile(r'(?<=does )[\d]+ [\w]+(?= damage)')
    p_drive = re.compile(r'(?<=initiative )[\d]+(?=\n)')

    with open(filepath) as file:
        lines = file.readlines()

    # find armies and groups
    armies = {}
    for i, line in enumerate(lines):
        # army?
        is_army = re.search(p_army, line)
        if is_army:
            banner = is_army[0]
            armies[banner] = Army(banner)

        # group?
        is_group = re.search(p_units, line)
        if is_group:
            units = is_group[0]
            drive = re.search(p_drive, line)[0]
            health = re.search(p_health, line)[0]
            damage, weapon = re.search(p_damage_weapon, line)[0].split()
            weaks = re.search(p_weaks, line)
            if weaks:
                weaks = weaks[0].split(', ')
            immuns = re.search(p_immuns, line)
            if immuns:
                immuns = immuns[0].split(', ')
            armies[banner].groups.add(Group(banner,
                                            int(units),
                                            int(drive),
                                            int(health),
                                            int(damage),
                                            weapon,
                                            weaks,
                                            immuns))

    return armies


################################################################################

if __name__ == '__main__':

    # testing
    armies = parse_input('day-24-test.txt')
    battle = Battle(armies)
    assert battle.fight() == 'Winner: Infection with 5216 units.'

    armies = parse_input('day-24.txt')
    battle = Battle(armies)
    pt1 = battle.fight()

    print(f"Part 1: {pt1}")
