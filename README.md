# CSE 120 Homework 3 extra credit

Fork of `olonkar29/ucsc-cse120-hw3`. The starter filenames `q4a.py` and `q4b.py` are retained; these correspond to Question 5(a) and 5(b) in Homework 3.

Requires Python 3.10 or later.

```sh
python -m pip install -r requirements.txt
python q4a.py
python q4b.py
```

- `q4a.py` implements combinational branch selection and checks all 16 combinations of opcode, zero, and lt.
- `q4b.py` retains the starter's 2-bit Y register, implements reset with priority over enable, and checks all 16 combinations of current Y, reset, and enable. Arithmetic wraps modulo 4.
- The second script also runs a 13-cycle sequence and generates a terminal waveform, `waveform.vcd`, and `trace.json`.

PyRTL records the current register value in each cycle. The inputs at cycle t determine Y at cycle t+1.
