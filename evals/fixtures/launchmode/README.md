# launchmode

`mode` is the sole persisted authority. `legacy_enabled` has no persisted producer, compatibility consumer, or deployed reader; it is an obsolete representation left from a removed prototype and should not be synchronized.

Status is derived from `mode`. Python's `bool("")` is valid and returns `False`; blank mode must remain disabled rather than receiving a new fallback.
