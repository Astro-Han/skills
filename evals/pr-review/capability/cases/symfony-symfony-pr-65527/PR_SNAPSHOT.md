# Frozen pull request snapshot

- PR: https://github.com/symfony/symfony/pull/65527 — `[Mailer] Fix emails reported twice when they are queued and sent in the same process`
- Author: nicolas-grekas
- Target base head: `7ca72401f058b8319a27dd40d88f08b7cc0dc9e7`
- Comparison base: `4f5c62c34cffc818385ecff114edade82c288633`
- Exact source head: `f35974eb84c57a97f85e5dc4fb1ad52d65358cd2`
- Diff: 114 additions, 3 deletions, 2 files
- Live mergeability and review state: intentionally unavailable in this historical fixture

## Pull request body

| Q             | A
| ------------- | ---
| Branch?       | 6.4
| Bug fix?      | yes
| New feature?  | no
| Deprecations? | no
| Issues        | Fix #54161
| License       | MIT

When the mailer is wired to a message bus, every email produces two `MessageEvent` instances: one dispatched by `Mailer::send()` before the email goes to the bus, with `queued` set to true, and one dispatched by the transport when the email is really sent. As soon as the bus handles `SendEmailMessage` synchronously, which is what happens by default once `symfony/messenger` is installed and no routing is configured, both events happen in the same process.

`MessageEvents::getMessages()`, which backs `getMailerMessages()` and `getMailerMessage()` in `MailerAssertionsTrait`, returned one message per event. Tests therefore saw every email twice, and `getMailerMessage(1)` returned the queued copy of the first email instead of the second one. `assertEmailCount()` did not have the problem because the `EmailCount` constraint already ignores queued events, which is why the two disagreed.

`getMessages()` now reports each email once. An email that was queued and then sent in the same process is reported through its sent message, which is the rendered one the transport received. An email that is still in the queue keeps being reported through its queued message, so tests that route emails to a real asynchronous transport are unaffected. `getMailerEvents()` still exposes both events, so `assertQueuedEmailCount()` and the profiler panel are unchanged.

The pairing is positional: a queued email is folded into the next email sent after it. The queued event and the sent event cannot be correlated by identity, because both carry a different clone of the message. The one case this cannot tell apart is an application that leaves an email in a queue and then sends an unrelated email through the same transport in the same process, which requires two differently wired mailer services.

Checks run on PHP 8.5 with PHPUnit 9.6:

* new `Symfony\Component\Mailer\Tests\Event\MessageEventsTest`, which drives a real `Mailer`, a synchronous `MessageBus` and the `MessageLoggerListener`: fails on the base commit with `Failed asserting that actual size 4 matches expected size 2`, passes with the fix.
* `./phpunit src/Symfony/Component/Mailer/Tests`: 169 tests, 8 skipped, no failure.
* `./phpunit src/Symfony/Bundle/FrameworkBundle/Tests`: 1374 tests, 5 skipped, no failure. The 31 legacy deprecation notices are reported on the base commit as well.



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

- `src/Symfony/Component/Mailer/Event/MessageEvents.php`: +13/-3
- `src/Symfony/Component/Mailer/Tests/Event/MessageEventsTest.php`: +101/-0
