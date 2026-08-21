def audit_totals(store):
    """Take an end-of-day snapshot and its total for the audit log."""
    snap = store.snapshot()
    return snap, sum(item["qty"] for item in snap.values())
