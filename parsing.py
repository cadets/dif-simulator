import itertools


def decode(opcode, operands, encoding, src):
    """
    Decode operands for a specific opcode (e.g., ['MOV', '4', '2', '3']) into
    a dictionary of named operands (e.g., {'rs1': 4, 'rs2': 2, 'rd': 3}).
    """

    operand_names = encoding.operand_names

    # Are there enough operands?
    if len(operands) < len(operand_names):
        raise ParseError(opcode, "need %d operands, got %d ('%s')" % (
            len(operand_names), len(operands), ' '.join(operands)), *src)

    # If there are more than the expected number of operands, the remainder had
    # better be comments.
    if (len(operands) > len(operand_names) and
            not operands[len(operand_names)-1].startswith('#')):
        raise ParseError(opcode, "expected %d operands, not '%s')" % (
            len(operand_names), ' '.join(operands)), *src)

    # We have the right number of operands: name the first n tokens and ignore
    # the comment token(s) at the end of the line.
    return list(zip(operand_names, [int(o) for o in operands]))


def parse(line, src):
    """
    Parse a string like 'MOV 1 2 3' into a string opcode ('MOV') and
    integer operands. The meaning of the operands is encoding-defined.
    """

    tokens = line.split()

    if len(tokens) == 0 or tokens[0].startswith('#'):
        return (None, None)

    opcode = tokens[0]

    # Convert operands to integers until we encounter a comment
    operands = [
        int(o) for o in
        itertools.takewhile(lambda t: not t.startswith('#'), tokens[1:])
    ]

    if len(operands) == 0:
        raise ParseError(opcode, "no operands", *src)

    if len(operands) > 3:
        raise ParseError(opcode, "too many operands (%d)" %
                         len(operands), *src)

    return (opcode, operands)


class ParseError(Exception):
    def __init__(self, opcode, message, filename, line_number):
        self.message = message
        self.filename = filename
        self.line_number = line_number

    def __str__(self):
        return 'Parse error: %s:%d: %s' % (
            self.filename, self.line_number, self.message)
