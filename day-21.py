""" Notes

    I can put any non-negative int in Registers.data[0]
    soooo ... change banr, bori, or borr to halt system? I have a bori ...

    apparently we weren't supposed to hack anything, but figure out the instructions
    again. reddit marcusandrews understood. and obviously had my same input.
    https://www.reddit.com/r/adventofcode/comments/a86jgt/2018_day_21_solutions/ec8lyck

"""

# import re

# class Instruction:
#     def __init__(self, data, before=None, after=None):
#         self.data = data
#         self.before = before
#         self.after = after

#     def __repr__(self):
#         return f"{self.__class__.__name__} {self.data!r}"


# class Registers:
#     def __init__(self, data, ip_reg):
#         self.data = data
#         self.ip = ip_reg
#         self.halted = False

#     def __repr__(self):
#         return f"{self.__class__.__name__} {self.data!r} ip{self.ip!r}"

#     def operate(self, instruction, ip_val):
#         self.data[self.ip] = ip_val
#         title, a, b, c = instruction.data

#         if title in ["bori", "borr", "banr"]:
#             self.halted = True

#         regs = self.data
#         self.data[c] = eval(opcodes[title].operation)


# class Opcode:
#     def __init__(self, title, operation):
#         self.title = title          # 'addi'
#         self.operation = operation  # 'regs[a] + b'

#     def __repr__(self):
#         return (f"{self.__class__.__name__} {self.title} {self.num!r}")


# def make_opcodes():
#     opcodes = {}
#     opcodes['addr'] = Opcode('addr', 'regs[a] + regs[b]')
#     opcodes['addi'] = Opcode('addi', 'regs[a] + b')
#     opcodes['mulr'] = Opcode('mulr', 'regs[a] * regs[b]')
#     opcodes['muli'] = Opcode('muli', 'regs[a] * b')
#     opcodes['banr'] = Opcode('banr', 'regs[a] & regs[b]')
#     opcodes['bani'] = Opcode('bani', 'regs[a] & b')
#     opcodes['borr'] = Opcode('borr', 'regs[a] | regs[b]')
#     # opcodes['bori'] = Opcode('bori', 'regs[a] | b')  # original
#     opcodes['bori'] = Opcode('bori', 'regs[a] | b')  # modified to halt?
#     opcodes['setr'] = Opcode('setr', 'regs[a]')
#     opcodes['seti'] = Opcode('seti', 'a')
#     opcodes['gtir'] = Opcode('gtir', '1 if a > regs[b] else 0')
#     opcodes['gtri'] = Opcode('gtri', '1 if regs[a] > b else 0')
#     opcodes['gtrr'] = Opcode('gtrr', '1 if regs[a] > regs[b] else 0')
#     opcodes['eqir'] = Opcode('eqir', '1 if a == regs[b] else 0')
#     opcodes['eqri'] = Opcode('eqri', '1 if regs[a] == b else 0')
#     opcodes['eqrr'] = Opcode('eqrr', '1 if regs[a] == regs[b] else 0')

#     return opcodes


# def get_instructions(puzzle):
#     op_patt = re.compile(r'[\w]{4}')
#     cd_patt = re.compile(r'[\d]+ [\d]+ [\d]+')
#     with open(puzzle) as file:
#         lines = [line.strip() for line in file.readlines()]

#     ip = int(re.search(r'[\d]+', lines[0])[0])


#     instructions = []
#     for line in lines[1:]:
#         op_title = [re.match(op_patt, line)[0]]
#         code = [int(n) for n in re.search(cd_patt, line)[0].split()]
#         instructions.append(Instruction(tuple(op_title + code)))

#     return ip, instructions


# def run_sequence(registers, instructions):
#     """  """

#     i = registers.data[registers.ip]
#     count = 1
#     while 0 <= i < len(instructions) and count <= 100000 and registers.halted is False:
#         # print(count, registers, i, instructions[i])
#         registers.operate(instructions[i], i)
#         # print(registers)
#         i = registers.data[registers.ip] + 1
#         count += 1

#     # print(f"{registers}")
#     return count-1  # registers

def run_activation_system(magic_number, is_part_1):
    seen = set()
    c = 0
    last_unique_c = -1

    while True:
        a = c | 65536
        c = magic_number

        while True:
            c = (((c + (a & 255)) & 16777215) * 65899) & 16777215

            if 256 > a:
                if is_part_1:
                    return c
                else:
                    if c not in seen:
                        seen.add(c)
                        last_unique_c = c
                        break
                    else:
                        return last_unique_c
            else:
                a //= 256




###############################

if __name__ == '__main__':
    # opcodes = make_opcodes()
    # ip, instructions = get_instructions('day-21.txt')

    # cheat = 7902108
    # for r in range(cheat, cheat+1):
    #     registers = Registers([r, 0, 0, 0, 0, 0], ip)
    #     count = run_sequence(registers, instructions)
    #     # if count <= 6:
    #     print(f"r: {r}, count: {count}, {registers}")

    # pt1 = None  # process_samples()
    # # map_opcodes()
    # pt2 = None  # run_actual_sequence()
    # print("\n\n\n")
    # print(f"Part 1: {pt1}")
    # print(f"Part 2: {pt2}")

    magic_number = int(open("day-21.txt", "r").readlines()[8].split()[1])
    print("Part 1:", run_activation_system(magic_number, True))
    print("Part 2:", run_activation_system(magic_number, False))
