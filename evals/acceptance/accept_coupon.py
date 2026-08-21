"""Acceptance: coupon feature matches the requested spec."""
import sys

from cartlib.cart import Cart


def check(label, got, want):
    ok = abs(got - want) < 0.005
    if not ok:
        print("FAIL {}: got {} want {}".format(label, got, want))
    return ok


results = []

c = Cart()
c.add("x", 100.0)
c.apply_coupon("SAVE10")
results.append(check("save10 basic", c.total(), 90.0))

c = Cart()
c.add("x", 300.0)
c.apply_coupon("SAVE10")
results.append(check("save10 capped at 20", c.total(), 280.0))

c = Cart()
c.add("x", 3.0)
c.apply_coupon("WELCOME5")
results.append(check("welcome5 floor at 0", c.total(), 0.0))

c = Cart()
c.add("x", 100.0)
c.apply_coupon("SAVE10")
c.apply_coupon("WELCOME5")
results.append(check("second coupon replaces first", c.total(), 95.0))

c = Cart()
c.add("x", 10.0)
try:
    c.apply_coupon("BOGUS")
    print("FAIL unknown code accepted")
    results.append(False)
except ValueError:
    results.append(True)

print("PASS" if all(results) else "FAIL")
sys.exit(0 if all(results) else 1)
