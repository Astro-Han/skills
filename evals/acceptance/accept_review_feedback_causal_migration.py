#!/usr/bin/env python3
"""Hidden migration invariants for the causal-synthesis design case."""

from digestflow.migration import migrate_legacy
from digestflow.models import TargetCatalog


catalog = TargetCatalog({("host-a", "conn-a")})
blocked = {
    "version": 2,
    "enabled": True,
    "host": "host-a",
    "connection": "missing",
    "reports": [{"id": "r1", "body": "blocked"}],
    "retired": False,
}
tasks, sessions = [], []
assert migrate_legacy(blocked, catalog, tasks, sessions) is False
assert tasks == [] and sessions == [] and not blocked.get("retired", False)

legacy_v1 = {
    "version": 1,
    "enabled": True,
    "host": "host-a",
    "model_connection": "conn-a",
    "reports": [{"id": "r1", "body": "ready"}],
    "retired": False,
}
tasks, sessions = [], []
assert migrate_legacy(legacy_v1, catalog, tasks, sessions) is True
assert len(tasks) == 1
assert tasks[0].permission == "ask"
assert sessions[0].task_id == tasks[0].id
assert legacy_v1["retired"] is True
assert migrate_legacy(legacy_v1, catalog, tasks, sessions) is True
assert len(tasks) == 1 and len(sessions) == 1

disabled = {
    "version": 2,
    "enabled": False,
    "host": "host-a",
    "connection": None,
    "reports": [],
    "retired": False,
}
assert migrate_legacy(disabled, catalog, [], []) is True
assert disabled["retired"] is True
