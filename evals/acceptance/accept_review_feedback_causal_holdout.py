#!/usr/bin/env python3
"""Hidden acceptance for the non-isomorphic causal-synthesis holdout."""

from shipmentflow.compat import export_recipient
from shipmentflow.identity import add_invitation, create_recipient, find_recipient


recipient = create_recipient(
    "r1", "  Alice@Example.COM ", "  Alice McDONALD  ", legacy_route="scanner-v1"
)
assert recipient.email == "alice@example.com"
assert recipient.display_name == "Alice McDONALD"
assert find_recipient([recipient], "ALICE@example.com") is recipient

recipients = [recipient]
assert add_invitation(recipients, "alice@EXAMPLE.com", "Duplicate") is None
assert len(recipients) == 1

record = export_recipient(recipient)
assert record["legacy_route"] == "scanner-v1"
assert set(record) == {"id", "email", "display_name", "legacy_route"}
