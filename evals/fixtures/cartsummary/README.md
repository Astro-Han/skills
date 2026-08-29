# cartsummary

`Cart.lines` is the sole authority for cart contents. `cached_total` is a prototype-era derived mirror with no persisted producer, compatibility consumer, or deployed reader; totals must be derived from lines instead of synchronizing the cache in every producer.

These APIs are in-memory preview helpers only. Python's `len([])` is valid and returns zero.
