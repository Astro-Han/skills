# Frozen pull request snapshot

- PR: https://github.com/symfony/symfony/pull/65486 — `[Messenger] Remove the worker listeners when messenger:consume ends`
- Author: nicolas-grekas
- Target base head: `7ca72401f058b8319a27dd40d88f08b7cc0dc9e7`
- Comparison base: `4f5c62c34cffc818385ecff114edade82c288633`
- Exact source head: `a90082b9cff575a6a8f05b0583f82a90ebf6ef39`
- Diff: 50 additions, 4 deletions, 2 files
- Live mergeability and review state: intentionally unavailable in this historical fixture

## Pull request body

| Q             | A
| ------------- | ---
| Branch?       | 6.4
| Bug fix?      | yes
| New feature?  | no
| Deprecations? | no
| Issues        | Fix #35038
| License       | MIT

`messenger:consume` turns its `--limit`, `--failure-limit` and `--memory-limit` options into event subscribers and registers them on the event dispatcher it was given, together with the reset services listener. None of them is removed when the command returns, and that dispatcher is the shared application one.

This stays invisible for a worker started from the command line, because the process ends with the command. It does not stay invisible when several runs share one process, which is what functional tests do. The second run still carries the listeners of the first one: a run with `--limit=3` that follows a run with `--limit=1` stops after a single message, because the leftover listener of the first run stops the worker. The reset services listener is added again on every run, so services also get reset once more per run.

The listeners are now collected while the options are read, registered right before the worker runs, and removed in the `finally` block that already clears the command's worker reference. Registering them just before the run also means that an invalid `--time-limit`, which is validated after the other options, no longer leaves listeners behind.

The new test runs the command twice on one dispatcher, with `--limit=1` then `--limit=2`, and checks that the second run handles two messages and that the dispatcher holds no listener once a run is over.

Checks run:
- `./phpunit src/Symfony/Component/Messenger/Tests/Command/ConsumeMessagesCommandTest.php`: 18 tests, 61 assertions, green.
- `./phpunit src/Symfony/Component/Messenger/Tests`: 411 tests, 1142 assertions, green, with the same 9 legacy deprecation notices the base commit reports (410 tests, 1139 assertions there).
- Revert check: source change removed, test kept, the test fails on the dispatcher assertion, which prints the leftover `StopWorkerOnMessageLimitListener` with `maximumNumberOfMessages => 1` plus the `ResetServicesListener` still subscribed to `WorkerRunningEvent` and `WorkerStoppedEvent`.
- A script running the command twice on one dispatcher, `--limit=1` then `--limit=3`: 1 message then 1 message before the change, 1 message then 3 messages after it.
- Both branches of this sweep touch `ConsumeMessagesCommand::execute()`. Cherry-picking them on top of each other merges without conflict and the Messenger suite stays green (412 tests, 1144 assertions).


## Linked issues

No closing Issue was linked in the frozen PR metadata.

## Exact-head checks

- Fabbot / Checks: SUCCESS
- Integration (8.1): SUCCESS
- Psalm: SUCCESS
- Unit Tests (8.1): SUCCESS
- Verify Packages: SUCCESS
- x86 / minimal-exts / lowest-php: SUCCESS
- Unit Tests (8.4, high-deps): SUCCESS
- Unit Tests (8.2, low-deps): SUCCESS
- Unit Tests (8.3): SUCCESS
- Unit Tests (8.4): SUCCESS
- Unit Tests (8.5): SUCCESS
- Unit Tests (8.6): FAILURE
- PHPStan: SUCCESS
- Hardening tests: SUCCESS

## Changed files

- `src/Symfony/Component/Messenger/Command/ConsumeMessagesCommand.php`: +13/-4
- `src/Symfony/Component/Messenger/Tests/Command/ConsumeMessagesCommandTest.php`: +37/-0
