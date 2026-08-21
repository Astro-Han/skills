"""Acceptance: remove() is a safe no-op for missing items, still removes real ones."""
import sys

from cartlib.cart import Cart

c = Cart()
c.add("apple", 2.5)
try:
    c.remove("not-there")
except Exception as exc:
    print("FAIL: remove raised {!r}".format(exc))
    sys.exit(1)
c.remove("apple")
ok = c.subtotal() == 0.0
print("PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
