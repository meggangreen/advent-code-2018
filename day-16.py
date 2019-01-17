import re
from copy import deepcopy

class Instruction:
    def __init__(self, before, after, data):
        self.before = Registers(before)
        self.after = Registers(after)
        self.data = data


    def __repr__(self):
        return f"{self.__class__.__name__} {self.data!r}"


class Opcode:
    def __init__(self, title, operation, num=-1):
        self.title = title            # 'addi'
        self.operation = operation  # 'regs[a] + b'
        self.num = num              # integer 1 to 16


    def __repr__(self):
        return (f"{self.__class__.__name__} {self.title} {self.num!r}")


class Registers:
    def __init__(self, data):
        self.data = data


    def __repr__(self):
        return f"{self.__class__.__name__} {self.data!r}"


    def operate(self, opcode, instruction):
        regs = deepcopy(self.data)
        _, a, b, c = instruction.data

        regs[c] = eval(opcode.operation)
        return regs


def get_instructions():
    pattern = re.compile(r'[\d], [\d], [\d], [\d]')
    with open('day-16.txt') as file:
        lines = [line.strip() for line in file.readlines()]
        divide = lines.index('=================')

    pt1_input = []
    for i in range(0, divide, 4):
        before = [int(n) for n in re.search(pattern, lines[i])[0].split(', ')]
        after = [int(n) for n in re.search(pattern, lines[i+2])[0].split(', ')]
        data = tuple(int(n) for n in lines[i+1].split())
        pt1_input.append(Instruction(before, after, data))

    # pt2_input here

    return pt1_input  #, pt2_input


def make_opcodes():
    'regs[a] + b'
    opcodes = []
    opcodes.append(Opcode('addr', 'regs[a] + regs[b]'))
    opcodes.append(Opcode('addi', 'regs[a] + b'))
    opcodes.append(Opcode('mulr', 'regs[a] * regs[b]'))
    opcodes.append(Opcode('muli', 'regs[a] * b'))
    opcodes.append(Opcode('banr', 'regs[a] & regs[b]'))
    opcodes.append(Opcode('bani', 'regs[a] & b'))
    opcodes.append(Opcode('borr', 'regs[a] | regs[b]'))
    opcodes.append(Opcode('bori', 'regs[a] | b'))
    opcodes.append(Opcode('setr', 'regs[a]'))
    opcodes.append(Opcode('seti', 'a'))
    opcodes.append(Opcode('gtir', '1 if a > regs[b] else 0'))
    opcodes.append(Opcode('gtri', '1 if regs[a] > b else 0'))
    opcodes.append(Opcode('gtir', '1 if regs[a] > regs[b] else 0'))
    opcodes.append(Opcode('eqir', '1 if a == regs[b] else 0'))
    opcodes.append(Opcode('eqri', '1 if regs[a] == b else 0'))
    opcodes.append(Opcode('eqir', '1 if regs[a] == regs[b] else 0'))

    return opcodes


def solve_pt1():
    instructions = get_instructions()
    opcodes = make_opcodes()

    more3 = 0
    for i in instructions:
        m = 0
        for o in opcodes:
            new_reg = i.before.operate(o, i)
            if new_reg == i.after.data:
                m += 1
            if m == 3:
                more3 += 1
                break

    return more3
