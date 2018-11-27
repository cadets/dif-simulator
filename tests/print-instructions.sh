#
# RUN: %print instructions > %t
# RUN: %check %s -input-file %t
#

# CHECK-DAG: ADD    Encoding 'R'
# CHECK-DAG: CMP    Encoding 'R'
# CHECK-DAG: LDGS   Encoding 'W'
