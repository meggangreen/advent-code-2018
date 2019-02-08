""" Notes

    side < army < group < unit, effective power

    side = immune sys or infection

    unit:
        - hit points: amount of damage withstood -- health
        - attack damage: amount of damage dealt -- damage
        - attack type: eg radiation, fire, cold, slashing, etc -- weapon
        - initiative: attack order and tie winner
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
from copy import deepcopy

class Unit:
    """ information for one unit """

    def __init__(self, health, damage, weapon, initiative=0,
                                               weaknesses=None,
                                               immunities=None):
        self.health = health
        self.damage = damage
        self.weapon = weapon
        self.initiative = initiative
        self.weaknesses = weaknesses
        self.immunities = immunities

    def __repr__(self):
        health = f"H:{self.health}"
        damage = f"D:{self.damage}"
        weapon = self.weapon
        initi = f"I:{self.initiative}"
        weak = self.weaknesses
        immun = self.immunities

        return f'<Unit {health} {damage} {weapon} {initi} {weak} {immun}>'


class Group:
    """ one group has 1+ identical units """

    def __init__(self, quantity, unit):
        self.quantity = quantity
        self.unit = unit
        self.initiative = self.quantity * self.unit.initiative
        self.efficacy = self.quantity * self.unit.damage

    def __repr__(self):
        return f'<Group Q:{self.quantity} I:{self.initiative} E:{self.efficacy}>'

    def _select_target(self, targets):
        """ called by Fight """
        # return target? self.target? both
        pass

    def _attack_target(self, target):
        """ called by Fight """
        pass

    def _defend(self):
        """ updates quanity, initiative, efficacy in an attack """
        pass

    def _lose_unit(self):
        self.quantity += -1


class Army:
    """ each side has an Army; each army has 1+ Groups """

    def __init__(self, banner, groups=None):
        self.banner = banner    # immune system or infection
        self.groups = groups if groups else set()

    def _tally_groups(self):
        if not self.groups:
            print(f"{self.banner} is no more.")
            return

        for group in self.groups:
            if group.quantity < 1:
                self.groups.remove(group)


class Fight:

    def __init__(self, armies):
        self.armies = armies

    def select_targets(self):
        # get all groups
        groups = set([group for army in self.armies for group in army.groups])
        # choose selection order -- a PQ!
        select_q = _make_selection_queue(groups)
        # get avail targets -- all groups
        targets = deepcopy(groups)  # is deepcopy necessary?
        # for each Group:
        while not select_q.empty():
            _, _, selector = select_q.get()
            # call G._select_target and pass avail targets
            target = selector._select_target(targets)
            # remove selected from avail
            targets.remove(target)

    def _make_selection_queue(self, groups):
        select_q = PriorityQueue()
        for group in groups:
            select_q.put((-group.efficacy, -group.initiative, group))

        return select_q



    def attack_targets():
        pass
