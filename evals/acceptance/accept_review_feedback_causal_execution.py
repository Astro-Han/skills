#!/usr/bin/env python3
"""Hidden execution and unmentioned-sibling invariants for causal synthesis."""

from digestflow.execution import clone_task, create_task, recover_task, trigger_task
from digestflow.models import TargetCatalog, Task


catalog = TargetCatalog({("host-a", "conn-a")})
task = create_task(
    {"host-a": {"primary": "conn-a"}, "host-b": {"primary": "conn-b"}},
    "host-b",
    "host-a",
    "primary",
)
assert task.host == "host-b" and task.connection == "conn-b" and task.permission == "ask"
assert clone_task(task, "clone").permission == "ask"

recoverable = Task("old", "daily-review", "host-a", None, "ask")
assert recover_task(recoverable, catalog).connection == "conn-a"
ambiguous = TargetCatalog({("host-a", "conn-a"), ("host-a", "conn-b")})
paused = Task("ambiguous", "daily-review", "host-a", None, "ask")
assert recover_task(paused, ambiguous).state == "paused"

try:
    trigger_task(task, "last-30-days", bridge_version=1)
except (RuntimeError, ValueError):
    pass
else:
    raise AssertionError("old bridge must not silently discard intent")
