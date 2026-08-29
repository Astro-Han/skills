# credrotate

`Credential.rotate()` owns token rotation. `legacy_token` must remain because a deployed rolling-version reader consumes the previous token; it is live compatibility state, not an obsolete mirror. API and importer are in-memory helpers with no external side effects.

Every rotation stores the prior current token in `legacy_token`. Python's `bool("")` is valid and returns `False`.
