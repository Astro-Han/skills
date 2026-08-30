# digestflow

Small scheduled-digest pipeline used to evaluate whether review feedback is resolved
through system invariants instead of a queue of suggested patches.

Released legacy snapshots already carry a mutable `retired` boolean. `False` means the
legacy snapshot is still the authority; successful one-way migration sets it to `True`.
`Task.preset` is the stable product identity across task recreation.

Every task created without an explicit user permission must use `ask`, regardless of
whether it came from migration, normal creation, or cloning. Activity includes the latest
revision of complete reports and active conversations, but excludes running partial
reports. A requested date range must never be changed silently: an old bridge that cannot
carry it must reject the trigger.
