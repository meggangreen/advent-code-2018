import re
from copy import deepcopy

class Instruction:
    def __init__(self, data, before=None, after=None):
        self.data = data
        self.before = before
        self.after = after


    def __repr__(self):
        return f"{self.__class__.__name__} {self.data!r}"


class Opcode:
    def __init__(self, title, operation, num=-1):
        self.title = title          # 'addi'
        self.operation = operation  # 'regs[a] + b'
        self.num = num              # integer 0 to 15


    def __repr__(self):
        return (f"{self.__class__.__name__} {self.title} {self.num!r}")


class Registers:
    def __init__(self, data):
        self.data = data


    def __repr__(self):
        return f"{self.__class__.__name__} {self.data!r}"


    def operate(self, instruction, opcode=None):
        regs = self.data
        n, a, b, c = instruction.data
        if not opcode:
            opcode = opcodes[n]

        self.data[c] = eval(opcode.operation)


def get_instructions():
    pattern = re.compile(r'[\d], [\d], [\d], [\d]')
    with open('day-16.txt') as file:
        lines = [line.strip() for line in file.readlines()]
        divide = lines.index('=================')

    samples = []
    for i in range(0, divide, 4):
        before = [int(n) for n in re.search(pattern, lines[i])[0].split(', ')]
        after = [int(n) for n in re.search(pattern, lines[i+2])[0].split(', ')]
        data = tuple(int(n) for n in lines[i+1].split())
        samples.append(Instruction(data, Registers(before), Registers(after)))

    actuals = []
    for i in range(divide+1, len(lines)):
        actuals.append(Instruction(tuple(int(n) for n in lines[i].split())))

    return samples, actuals


def make_opcodes():
    opcodes = {}
    opcodes['addr'] = Opcode('addr', 'regs[a] + regs[b]')
    opcodes['addi'] = Opcode('addi', 'regs[a] + b')
    opcodes['mulr'] = Opcode('mulr', 'regs[a] * regs[b]')
    opcodes['muli'] = Opcode('muli', 'regs[a] * b')
    opcodes['banr'] = Opcode('banr', 'regs[a] & regs[b]')
    opcodes['bani'] = Opcode('bani', 'regs[a] & b')
    opcodes['borr'] = Opcode('borr', 'regs[a] | regs[b]')
    opcodes['bori'] = Opcode('bori', 'regs[a] | b')
    opcodes['setr'] = Opcode('setr', 'regs[a]')
    opcodes['seti'] = Opcode('seti', 'a')
    opcodes['gtir'] = Opcode('gtir', '1 if a > regs[b] else 0')
    opcodes['gtri'] = Opcode('gtri', '1 if regs[a] > b else 0')
    opcodes['gtrr'] = Opcode('gtrr', '1 if regs[a] > regs[b] else 0')
    opcodes['eqir'] = Opcode('eqir', '1 if a == regs[b] else 0')
    opcodes['eqri'] = Opcode('eqri', '1 if regs[a] == b else 0')
    opcodes['eqrr'] = Opcode('eqrr', '1 if regs[a] == regs[b] else 0')

    return opcodes


def process_samples():
    """ Part One """

    more_than_3 = 0

    while samples:
        sample = samples.pop()
        if test_opcodes(sample) >=3:
            more_than_3 += 1

    return more_than_3


def test_opcodes(sample):
    if sample.data[0] not in mapping.keys():
        mapping[sample.data[0]] = set()

    orig_regs = deepcopy(sample.before.data)

    opcode_matches = 0
    for o in opcodes:
        sample.before.data = [d for d in orig_regs]
        sample.before.operate(sample, opcodes[o])
        if sample.before.data == sample.after.data:
            opcode_matches += 1
            mapping[sample.data[0]].add(o)

    return opcode_matches


def map_opcodes():
    # and if there is no number with only one opcode? idk
    used = set()
    while mapping:
        num, titles = sorted(mapping.items(), key = lambda kv: len(kv[1]))[0]
        if len(titles) == 1:
            active = titles.pop()
            used.update([active, num])
            assign_num(active, num)
            for others in mapping.values():
                others.discard(active)


def assign_num(opcode_title, num):
    opcodes[opcode_title].num = num
    opcodes[num] = opcodes[opcode_title]
    del mapping[num]


def run_actual_sequence():
    """ Part Two """

    regs = Registers([0, 0, 0, 0])
    for instruction in actuals:
        regs.operate(instruction)

    return regs


###############################

if __name__ == '__main__':
    samples, actuals = get_instructions()
    opcodes = make_opcodes()
    mapping = {}
    pt1 = process_samples()
    map_opcodes()
    pt2 = run_actual_sequence()
    print("\n\n\n")
    print(f"Part 1: {pt1}")
    print(f"Part 2: {pt2}")
