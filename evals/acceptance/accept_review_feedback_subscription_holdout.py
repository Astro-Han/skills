#!/usr/bin/env python3
"""Hidden mixed-root acceptance for the subscription holdout."""

from subscriptionflow.actions import cancel_from_row, pause, resume_after_payment
from subscriptionflow.compat import export_subscription
from subscriptionflow.models import Session, Subscription
from subscriptionflow.projection import active_rows, active_total


subscription = Subscription("s1", "active", legacy_channel="renewal-v1")
pause(subscription)
cancel_from_row(subscription, {})
resume_after_payment(subscription)
subscription.transition("active")
assert subscription.history == ["paused", "cancelled", "active", "active"]

sessions = [
    Session("a1", "root-a", 1, "active"),
    Session("a2", "root-a", 2, "closed"),
    Session("b1", "root-b", 1, "closed"),
    Session("b2", "root-b", 2, "active"),
]
assert [row.id for row in active_rows(sessions)] == ["b2"]
assert active_total(sessions) == 1

record = export_subscription(subscription)
assert record == {
    "id": "s1",
    "state": "active",
    "legacy_channel": "renewal-v1",
}
