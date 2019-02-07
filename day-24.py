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

class Unit:
    """ docstring for Unit """

    def __init__(self, health, damage, weapon, initiative=0,
                                               weaknesses=None,
                                               immunities=None):
        self.health = health
        self.damage = damage
        self.weapon = weapon
        self.initiative = initiative
        self.weaknesses = weaknesses
        self.immunities = immunities

