#!/usr/bin/env python3
from handlekit.api import register
from handlekit.handles import canonicalize
from handlekit.importer import import_row


assert canonicalize("  Straße  ") == "strasse"
assert register("  ADA  ") == "ada"
assert import_row({"handle": "  MiXeD  "}) == "mixed"
assert canonicalize("") == ""
print("review feedback normalization acceptance passed")
