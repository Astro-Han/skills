# batchplan

`normalize_size` is the sole owner of the batch-size policy. Every producer must receive a positive integer from it. Preview functions are in-memory helpers only: they persist nothing and have no external side effects.

`BatchPlan.total_items()` must return zero for an empty plan; Python's built-in `sum([])` already provides that behavior.
