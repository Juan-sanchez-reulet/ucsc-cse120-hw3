"""Homework 3 Q5(b), using the provided q4b.py filename."""
from pathlib import Path
import json
import pyrtl


def main():
    enable = pyrtl.Input(1, "enable")
    reset = pyrtl.Input(1, "reset")
    y = pyrtl.Register(2, "y")
    # Reset has priority; the 2-bit register wraps modulo 4.
    y.next <<= pyrtl.select(reset, truecase=0,
                           falsecase=pyrtl.select(enable, truecase=y + 1,
                                                  falsecase=y))
    return y


def test_transitions():
    count = 0
    for initial in range(4):
        for r in range(2):
            for e in range(2):
                pyrtl.reset_working_block()
                y = main()
                sim = pyrtl.Simulation(register_value_map={y: initial})
                sim.step({"reset": r, "enable": e})
                expected = 0 if r else ((initial + 1) % 4 if e else initial)
                # inspect() shows the current cycle, so step again to see next Y.
                sim.step({"reset": 0, "enable": 0})
                assert sim.inspect(y) == expected, (initial, r, e, expected)
                count += 1
    print(f"PASS: {count}/16 state transitions (all Y, reset, enable combinations)")


if __name__ == "__main__":
    test_transitions()
    pyrtl.reset_working_block()
    y = main()
    trace = pyrtl.SimulationTrace()
    sim = pyrtl.Simulation(tracer=trace)
    # Hold, increment, hold at nonzero Y, wraparound, reset with both enable values.
    inputs = [(1,0), (0,0), (0,1), (0,1), (0,0), (0,1),
              (0,1), (0,1), (1,1), (0,1), (0,1), (1,0), (0,0)]
    expected = 0
    for reset_value, enable_value in inputs:
        sim.step({"reset": reset_value, "enable": enable_value})
        assert sim.inspect(y) == expected
        expected = 0 if reset_value else ((expected + 1) % 4 if enable_value else expected)
    trace.render_trace(trace_list=["reset", "enable", "y"])
    directory = Path(__file__).resolve().parent
    with (directory / "waveform.vcd").open("w") as f:
        trace.print_vcd(f)
    (directory / "trace.json").write_text(json.dumps(
        {name: list(trace.trace[name]) for name in ["reset", "enable", "y"]}, indent=2))
    print("PASS: 13-cycle waveform sequence; waveform.vcd and trace.json written")
