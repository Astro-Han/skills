#!/usr/bin/env python3
from quoteview.api import preview
from quoteview.importer import preview_row
from quoteview.model import LineItem
from quoteview.quote import Quote


def rejects(call):
    try:
        call()
    except ValueError:
        return True
    return False


assert rejects(lambda: LineItem("bad", 10.0, 0))
assert rejects(lambda: preview("bad", 10.0, -1))
assert rejects(lambda: preview_row({"name": "bad", "unit_price": "10", "quantity": "0"}))
assert Quote([]).total() == 0
print("review feedback acceptance passed")
