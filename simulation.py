import model
import types


class RegisterFile:
    """
    A simulated register file that can be assigned to and retrieved from.
    """

    def __init__(self, n, machine):
        self.state = [None] * n
        self.machine = machine

        # r0 is always 0
        self.state[0] = 0

    def all_registers(self):
        """
        Provide access to all registers without going through the normal
        __getitem__ route (which checks that a given register isn't undefined).
        """
        return self.state

    def __getitem__(self, index):
        """
        Retrive the value stored in a register, assuming that the index is
        valid and that register's contents are defined.
        """

        i = int(index)
        if i != index:
            raise TypeError(self, "non-integer register index: '%s'" % index)

        value = self.state[i]
        if value is None:
            raise SimulationError(self.machine,
                                  'accessing undefined value in r%d' % i)

        return self.state[i]

    def __setitem__(self, i, value):
        """
        Assign a value to a register, checking that it is, in fact, an integer.
        """

        if i == 0:
            raise SimulationError(self.machine, 'assigning to r0 is illegal')

        if int(value) != value:
            message = "assigning non-integer '%s' to r%d" % (value, i)
            raise SimulationError(self.machine, message)

        self.state[i] = value


class Simulator(model.Machine):
    """
    Executes DTrace instructions against a concrete simulation of a
    DTrace machine that includes memory, a DTrace register file, variables, etc.
    """

    def __init__(self, state, instructions, log):
        self.log = log

        mem = state['memory'] if 'memory' in state else {}

        registers = RegisterFile(8, self)
        if 'registers' in state:
            for (k, v) in state['registers'].items():
                registers[k] = v

        integers = types.MappingProxyType(
            dict(enumerate(state['integers'])) if 'integers' in state else {})

        strings = types.MappingProxyType(
            dict(enumerate(state['strings'])) if 'strings' in state else {})

        super().__init__(instructions, mem, registers, integers, strings)

    def execute(self, opcode, operands, src):
        (f, operands) = self.decode(opcode, operands, src)

        self.log.info("%s %s" % (opcode, ', '.join(
            ['%s=%d' % (k, v) for (k, v) in operands])))

        f(self, **dict(operands))

        self.log.debug(self)

    def state(self):
        """
        Serialize the internal state of the simulated machine
        """

        integers = [
            k for (k, v) in
            sorted(self.tables.integers.items(), key=lambda kv: kv[0])
        ]

        strings = [
            k for (k, v) in
            sorted(self.tables.strings.items(), key=lambda k, v: k)
        ]

        return {
            'memory': self.mem,
            'registers': dict([
                (k, v) for (k, v) in enumerate(self.registers.all_registers())
                if k > 0 and v is not None
            ]),
            'integers': integers,
            'strings': strings,
        }


class SimulationError(Exception):
    """
    An error has occurred while simulating an instruction.
    """

    def __init__(self, simulator, message):
        self.message = message
        self.simulator = simulator

    def __str__(self):
        return self.message
