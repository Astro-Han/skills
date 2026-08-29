# mediathread

Small message rendering package used by the review-feedback cumulative-diff fixture.

The fixture begins at a stable text-only baseline. The eval harness applies a committed
feature patch before the agent starts so the agent must review the whole PR rather than a
single isolated comment.
