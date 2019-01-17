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
        # return regs


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
    'regs[a] + b'
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


def map_opcodes():
    mapping = {}
    for sample in samples:
        orig_regs = deepcopy(sample.before.data)
        if sample.data[0] not in mapping.keys():
            mapping[sample.data[0]] = set()
        for o in opcodes:
            sample.before.data = [d for d in orig_regs]
            sample.before.operate(sample, opcodes[o])
            if sample.before.data == sample.after.data:
                mapping[sample.data[0]].add(o)

    # and if there is no number with only one opcode? idk
    used = set()
    while mapping:
        n, titles = sorted(mapping.items(), key = lambda kv: len(kv[1]))[0]
        if len(titles) == 1:
            active = titles.pop()
            used.update([active, n])
            opcodes[active].num = n
            opcodes[n] = opcodes[active]
            del mapping[n]
            for others in mapping.values():
                others.discard(active)
        elif len(titles) == 0:
            missing = n
            del mapping[n]


def solve_pt2():
    regs = Registers([0, 0, 0, 0])
    for instruction in actuals:
        regs.operate(instruction)

    return regs


###############################
if __name__ == '__main__':
    samples, actuals = get_instructions()
    opcodes = make_opcodes()
    map_opcodes()
    print(solve_pt2())