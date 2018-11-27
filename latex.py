import inspect


def write(out, name, fn):
    """
    Write a LaTeX description of a single DIF instruction, specified by
    instruction name and pseudocode function.

    The emitted LaTeX conforms to a format used by the OpenDTrace Specification.
    """

    #
    # Header: instruction name and brief description
    #
    comments = inspect.getcomments(fn)
    if comments:
        (brief, *description) = [l[1:].strip() for l in comments.splitlines()]
    else:
        (brief, description) = (name, None)

    out.write(f'''
\\clearpage
\\phantomsection

\\addcontentsline{{toc}}{{subsection}}{{{name}}}
\\label{{insn:{name.lower()}}}
\\subsection*{{{name}: {brief}}}
''')

    #
    # Format: instruction, operand names and bitfield
    #

    # Instruction name and operand names:
    out.write(f'''
\\subsubsection*{{Format}}
\\texttt{{{name} {' '.join(fn.encoding.operand_names())}}}
''')

    # Bytefield (starts with opcode):
    ranges = [(hex(fn.opcode), (0, 7))]
    for (op_name, width) in fn.encoding.operands:
        bit = ranges[-1][1][1] + 1
        ranges.append((op_name, (bit, bit + width - 1)))

    out.write(f'''
\\begin{{center}}
  \\begin{{bytefield}}[endianness=big,bitformatting=\\scriptsize]{{32}}
    \\bitheader{{{",".join(['%d,%d' % bits for (name, bits) in ranges])}}}
''')

    # Output bitbox for each operand
    for (name, (begin, end)) in ranges:
        out.write(f'    \\bitbox{{{end-begin+1}}}{{{name}}}\n')

    out.write('  \\end{bytefield}\n\\end{center}')

    #
    # Longer description:
    #
    newline = '\n'

    if description:
        out.write(f'''
\\subsubsection*{{Description}}
{newline.join(description)}
''')

    #
    # Pseudocode (not including function decorators):
    #
    source = inspect.getsource(fn)
    source = [l for l in inspect.getsource(
        fn).splitlines() if not l.startswith('@')]

    out.write(f'''

\\subsubsection*{{Pseudocode}}

\\begin{{lstlisting}}[language=Python]
{newline.join(source)}
\\end{{lstlisting}}
''')
