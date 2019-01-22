import re

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
    def __init__(self, data, ip_reg):
        self.data = data
        self.ip = ip_reg


    def __repr__(self):
        return f"{self.__class__.__name__} {self.data!r} ip{self.ip!r}"


    def operate(self, instruction, ip_val, opcode=None):
        self.data[self.ip] = ip_val
        regs = self.data

        title, a, b, c = instruction.data
        if not opcode:
            opcode = opcodes[title]

        self.data[c] = eval(opcode.operation)


def get_instructions(puzzle):
    op_patt = re.compile(r'[\w]{4}')
    cd_patt = re.compile(r'[\d]+ [\d]+ [\d]+')
    with open(puzzle) as file:
        lines = [line.strip() for line in file.readlines()]

    ip = int(re.search(r'[\d]+', lines[0])[0])


    instructions = []
    for line in lines[1:]:
        op_title = [re.match(op_patt, line)[0]]
        code = [int(n) for n in re.search(cd_patt, line)[0].split()]
        instructions.append(Instruction(tuple(op_title + code)))

    return ip, instructions


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


def run_sequence(registers, instructions):
    """ Part One """

    used = set()

    i = registers.data[registers.ip]
    count = 1
    while 0 <= i < len(instructions) and count <= 10000:
        # part one answer requires 6,383,176 iterations
        registers.operate(instructions[i], i)
        i = registers.data[registers.ip] + 1
        if i == 1:
        # if i == registers.ip and registers.data[4] > 893:
            print(registers, count)
            # import pdb; pdb.set_trace()
            break
        count += 1

    # print(f"Count: {count-1}")
    return registers


if __name__ == '__main__':
    opcodes = make_opcodes()

    # testing
    ip, instructions = get_instructions('day-19-test.txt')
    registers = Registers([0, 0, 0, 0, 0, 0], ip)
    test = run_sequence(registers, instructions)
    # assert test.data==[6,5,6,0,0,9]
    print("\n\n\n")
    print("Test Successful")

    ip, instructions = get_instructions('day-19.txt')

    registers = Registers([0, 0, 0, 0, 0, 0], ip)
    pt1 = run_sequence(registers, instructions)
    print(f"P1: {pt1}")

    registers = Registers([1, 0, 0, 0, 0, 0], ip)
    pt2 = run_sequence(registers, instructions)
    print(f"P2: {pt2}")