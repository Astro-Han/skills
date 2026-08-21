"""Reproduces the nightly sync: applies deltas, prints the drift report."""

from stocksync.report import format_drift
from stocksync.store import Store
from stocksync.sync import run_cycle

store = Store()
store.receive("apples", 10)
store.receive("bananas", 8)

drift = run_cycle(store, [("apples", 12), ("bananas", -3)])
print(format_drift(drift))
print("final apples:", store.quantity("apples"))
print("final bananas:", store.quantity("bananas"))
