#!/usr/bin/env python3
"""Hidden projection invariants for the causal-synthesis design case."""

from digestflow.models import Session, Task
from digestflow.projection import active_conversations, activity_total, report_rows


history = [
    Session("old", "removed-task", "daily-review", "root-a", 1, "complete", "old"),
    Session("draft", "current-task", "daily-review", "root-b", 1, "running", "partial"),
    Session("rev1", "other", "conversation", "root-c", 1, "active", None),
    Session("rev2", "other", "conversation", "root-c", 2, "active", None),
]
current = Task("current-task", "daily-review", "host-a", "conn-a", "ask")
reports = report_rows(history, current)
assert [row.id for row in reports] == ["old"]
assert activity_total(history) == 2
assert [row.id for row in active_conversations(history)] == ["rev2"]
