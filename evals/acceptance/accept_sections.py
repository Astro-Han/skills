"""Acceptance: two builders in one process stay isolated."""
import sys

from reportlib.builder import ReportBuilder

a = ReportBuilder("A").add_section("sales", [1, 2])
b = ReportBuilder("B").add_section("returns", [3])
ok = (
    a.build()["sections"] == [("sales", [1, 2])]
    and b.build()["sections"] == [("returns", [3])]
)
print("PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
