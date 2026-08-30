# subscriptionflow

`Subscription.transition` owns lifecycle state and history. Every requested transition,
including a same-state transition, is recorded. API, import, and recovery paths must use
that owner.

Activity projections show only the latest revision of each session root. `legacy_channel`
is still consumed by deployed renewal workers and must remain in exported records. There
is no product requirement for future state aliases.
