def run_cycle(store, deltas):
    """Apply the day's deltas and return the observed drift per item."""
    before = store.snapshot()
    for name, change in deltas:
        if change >= 0:
            store.receive(name, change)
        else:
            store.ship(name, -change)
    after = store.snapshot()
    return {
        name: after[name]["qty"] - before.get(name, {"qty": 0})["qty"]
        for name in after
    }
