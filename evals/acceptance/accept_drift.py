"""Acceptance: drift is computed correctly AND snapshots are truly isolated."""
import sys

from stocksync.store import Store
from stocksync.sync import run_cycle

results = []

s = Store()
s.receive("apples", 10)
s.receive("bananas", 8)
drift = run_cycle(s, [("apples", 12), ("bananas", -3)])
ok = drift == {"apples": 12, "bananas": -3}
if not ok:
    print("FAIL drift values: got {}".format(drift))
results.append(ok)
ok = s.quantity("apples") == 22 and s.quantity("bananas") == 5
if not ok:
    print("FAIL final quantities changed")
results.append(ok)

s2 = Store()
s2.receive("apples", 10)
held = s2.snapshot()
s2.receive("apples", 5)
s2.receive("pears", 7)
ok = held["apples"]["qty"] == 10 and "pears" not in held
if not ok:
    print("FAIL held snapshot mutated: apples={} pears_in={}".format(
        held["apples"]["qty"], "pears" in held))
results.append(ok)

print("PASS" if all(results) else "FAIL")
sys.exit(0 if all(results) else 1)
