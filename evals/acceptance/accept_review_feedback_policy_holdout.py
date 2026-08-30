#!/usr/bin/env python3
"""Hidden independent-policy acceptance for the policy holdout."""

from policyflow.compat import export_delivery
from policyflow.intake import (
    create_bucket_delivery,
    create_email_delivery,
    find_email_delivery,
)


email = create_email_delivery(
    "e1", " Alice@Example.COM ", " Alice McDONALD ", legacy_route="scanner-v1"
)
assert email.destination == "alice@example.com"
assert email.label == "Alice McDONALD"
assert find_email_delivery([email], "ALICE@example.com") is email

bucket = create_bucket_delivery("b1", " Reports/Quarterly ", " Finance Team ")
assert bucket.destination == "Reports/Quarterly"
assert bucket.label == "Finance Team"

record = export_delivery(email)
assert record == {
    "id": "e1",
    "destination": "alice@example.com",
    "label": "Alice McDONALD",
    "legacy_route": "scanner-v1",
}
