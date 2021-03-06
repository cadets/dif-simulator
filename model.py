import parsing
import types


class Machine:
    """
    Base class for DTrace machine models
    """

    def __init__(self, instructions, mem, registers, integers, strings):
        self.instructions = instructions
        self.mem = mem
        self.registers = registers

        self.tables = types.SimpleNamespace()
        self.tables.integers = integers
        self.tables.strings = strings

    def copy(self):
        return Machine(self.mem.copy(), self.registers.copy())

    def decode(self, opcode, operands, src):
        f = self.instructions.instructions[opcode]
        operands = parsing.decode(opcode, operands, f.encoding, src)

        return (f, operands)

    def execute(self, opcode, operands, src):
        raise Exception('Machine.execute() not implemented')

    def __str__(self):
        s = 'Registers:'

        for (i, r) in enumerate(self.registers.all_registers()):
            rstr = 'undefined' if r is None else '0x%016x' % r
            s += '\n  r%d:  %s' % (i, rstr)

        return s
