#
# RUN: %print pseudocode ADD > %t
# RUN: %check %s -input-file %t
#

# CHECK: def ADD(state, rs1, rs2, rd):
# CHECK-NEXT: state.registers[rd] = state.registers[rs1] + state.registers[rs2]
