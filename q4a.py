"""Homework 3 Q5(a), using the provided q4a.py filename."""
import pyrtl


def datapath(zero, lt, opcode):
    # 00: blt, 01: bge, 10: beq, 11: bne.
    # Bit 1 selects the comparison and bit 0 inverts it.
    comparison = pyrtl.select(opcode[1], truecase=zero, falsecase=lt)
    branch = comparison ^ opcode[0]
    return branch


if __name__ == "__main__":
    pyrtl.reset_working_block()
    zero = pyrtl.Input(1, "zero")
    lt = pyrtl.Input(1, "lt")
    opcode = pyrtl.Input(2, "opcode")
    branch = pyrtl.Output(1, "branch")
    branch <<= datapath(zero, lt, opcode)
    sim = pyrtl.Simulation()
    tests = 0
    for op in range(4):
        for z in range(2):
            for l in range(2):
                sim.step({"zero": z, "lt": l, "opcode": op})
                expected = (l, 1-l, z, 1-z)[op]
                actual = sim.inspect("branch")
                assert actual == expected, (op, z, l, expected, actual)
                tests += 1
    print(f"PASS: {tests}/16 branch cases (all opcode, zero, lt combinations)")
