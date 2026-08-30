# Frozen pull request snapshot

- PR: https://github.com/cli/cli/pull/14255 — `Make commands own attachment flag policy`
- Author: BagToad
- Target base head: `cd94f8cdffd710b41fa16df39680ee6f75069ecd`
- Comparison base: `cd94f8cdffd710b41fa16df39680ee6f75069ecd`
- Exact source head: `9dc818dca2f0043147d71fef3584559bdf0ace6c`
- Diff: 199 additions, 280 deletions, 14 files
- Live mergeability and review state: intentionally unavailable in this historical fixture

## Pull request body

<!--
Thank you for contributing to GitHub CLI!

If you are proposing a fix for a security issue, STOP and follow .github/SECURITY.md instead.
-->

Related review feedback:

- https://github.com/cli/cli/pull/14181#discussion_r3801438970
- https://github.com/cli/cli/pull/14181#discussion_r3821179636
- https://github.com/cli/cli/pull/14181#discussion_r3821179640

<!-- List related issues here. Use `fixes` or `closes` keywords to associate an issue number. -->

### Description

<!--
What's the problem? How are we addressing it?

Write for a reviewer who has not worked in this part of the codebase. Give them the
background they need before the problem makes sense, and avoid jargon.
-->

The attachment package currently registers and resolves `--attach`, but it also reads
command-owned flags such as `--web`, `--dry-run`, and `--delete-last` to enforce conflicts.
That spreads command policy into a package that should only own attachment values.

This introduces an attachment flag handle that owns registration, parsed values, changed state,
and conversion to validated assets. Each command stores that handle, resolves assets through it,
and owns its attachment conflicts using `cmdutil.MutuallyExclusive`.

The ownership and call flow change like this:

![attach-flag-flow](https://github.com/user-attachments/assets/201e37e8-382f-47cc-ad55-a9090f1e6c0d)

<sub>Uploaded with `gh pr edit --attach`</sub>

### How did you test this change?

<!--
Show how you exercised the change yourself, as a user of `gh` would.

Automated test results do not belong here. Passing unit tests, `go test ./...` output, and
coverage numbers tell a reviewer nothing they cannot see from CI, so do not paste them.

Use one or more of these, whichever communicates best:

1. Screenshots or GIFs of the real command running. Preferred whenever the change is visible
   in terminal output. If output changed, show it before and after.
2. Given/When/Then scenarios. For example:
   Given I am in a repo with no open pull requests
   When I run `gh pr list`
   Then I see "no open pull requests in cli/cli"
3. A natural language walkthrough of what you did by hand, the states you covered, and what
   you saw, including error and edge cases.

If you leave this empty, your pull request will very likely be closed.
-->

Given `--attach` named a missing file while a command also used an incompatible mode,
I ran local `gh` commands for issue creation, pull request creation, and issue comments.
Each command returned its existing attachment conflict before attempting to read the file:

```text
`--attach` is not supported when using `--web`
```

This verifies that moving conflict ownership did not change error precedence at the command
boundary.

### Key points

<!--
Tradeoffs you accepted, alternatives you rejected, and anything a reviewer would otherwise have to guess at.
-->

- The wrapper keeps the fixed `attach` name and no shorthand. It does not add unused name or
  shorthand configuration.
- Commands own conflicts with their own flags. The attachment package no longer knows about
  `web`, `dry-run`, or `delete-last`.
- Conflict checks remain ahead of filesystem validation and retain their existing messages.
- Package-level conflict cases were removed only after the existing command tables were confirmed
  to cover every conflict pair.
- This is a behavior-neutral refactor. Parsing, validation, duplicate detection, and upload
  behavior are unchanged.

### Notes for reviewers

<!--
Where should review start, and what should be read next? Call out anything you are unsure about.

Link related issues or prior discussion, with one sentence on why each matters.
-->

Review the commits in order:

1. `Add attachment flag wrapper` introduces the handle and keeps every production call site on
   the old path.
2. `Move attachment policy into commands` migrates call sites, moves conflicts, and removes the
   old command lookup API.

The main design question is whether `Flag` is the right boundary between command-owned policy and
attachment-owned values. The diff deliberately avoids storing the entire Cobra command on the
wrapper.

### Authorship and follow-up

<!--
REQUIRED - If you are an AI agent filling in this template, answer "Who wrote this" for yourself and answer honestly. For "Who answers review comments," use only a choice the human has explicitly made in the conversation. If no choice has already been established, pause and ask the human to choose one of the three options before creating or updating the pull request. Do not infer the choice from repository ownership, authorship, assignees, prior interactions, or the current operator. After the human answers, check exactly the option they chose; the last option is valid when the human explicitly chooses nobody.

Check exactly one box in each list.
-->

Who wrote this:

- [ ] A human wrote it.
- [x] An agent wrote it under close human direction.
- [ ] An agent wrote it independently, and no human has guided the implementation beyond the initial prompt.

Who answers review comments:

- [x] @BagToad will read and reply directly. Name the account.
- [ ] An agent will draft replies and @username will read them before they are posted.
- [ ] Nobody has explicitly committed to replying.


## Linked issues

No closing Issue was linked in the frozen PR metadata.

## Exact-head checks

- label-external: SKIPPED
- label-external: SKIPPED
- label-external: SKIPPED
- label-external: SKIPPED
- label-external: SKIPPED
- CodeQL-Build (go, manual, ./.github/codeql/codeql-config.yml): SUCCESS
- lint: SUCCESS
- label-external / label_issues: SUCCESS
- build (ubuntu-latest): SUCCESS
- CodeQL-Build (actions, none, security-and-quality): SUCCESS
- build (windows-latest): SUCCESS
- build (macos-latest): SUCCESS
- close-from-default-branch: SKIPPED
- close-from-default-branch: SKIPPED
- close-from-default-branch: SKIPPED
- close-from-default-branch: SKIPPED
- close-from-default-branch: SKIPPED
- close-from-default-branch / close-from-default-branch: SKIPPED
- govulncheck: SUCCESS
- integration-tests (ubuntu-latest): SUCCESS
- integration-tests (windows-latest): SUCCESS
- integration-tests (macos-latest): SUCCESS
- check-requirements / check-requirements: SKIPPED
- check-requirements / check-requirements: SKIPPED
- check-requirements / check-requirements: SKIPPED
- check-requirements / check-requirements: SKIPPED
- check-requirements / check-requirements: SKIPPED
- check-requirements / check-requirements: SKIPPED
- check-requirements / close-unmet-requirements: SKIPPED
- check-requirements / close-unmet-requirements: SKIPPED
- check-requirements / close-unmet-requirements: SKIPPED
- check-requirements / close-unmet-requirements: SKIPPED
- check-requirements / close-unmet-requirements: SKIPPED
- check-requirements / close-unmet-requirements: SKIPPED
- close-unmet-requirements: SKIPPED
- close-unmet-requirements: SKIPPED
- close-unmet-requirements: SKIPPED
- close-unmet-requirements: SKIPPED
- close-unmet-requirements: SKIPPED
- close-unmet-requirements: SKIPPED
- close-no-help-wanted: SKIPPED
- close-no-help-wanted: SKIPPED
- close-no-help-wanted: SKIPPED
- close-no-help-wanted: SKIPPED
- close-no-help-wanted: SKIPPED
- close-no-help-wanted: SKIPPED
- ready-for-review: SKIPPED
- ready-for-review: SKIPPED
- ready-for-review: SKIPPED
- ready-for-review: SKIPPED
- ready-for-review: SKIPPED
- ready-for-review: SKIPPED
- CodeQL: SUCCESS

## Changed files

- `internal/attachments/doc.go`: +3/-1
- `internal/attachments/flags.go`: +24/-41
- `internal/attachments/flags_test.go`: +77/-157
- `internal/attachments/test.go`: +2/-2
- `pkg/cmd/issue/comment/comment.go`: +1/-1
- `pkg/cmd/issue/create/create.go`: +12/-3
- `pkg/cmd/issue/create/create_test.go`: +2/-2
- `pkg/cmd/issue/edit/edit.go`: +5/-4
- `pkg/cmd/pr/comment/comment.go`: +1/-1
- `pkg/cmd/pr/create/create.go`: +20/-3
- `pkg/cmd/pr/create/create_test.go`: +2/-2
- `pkg/cmd/pr/edit/edit.go`: +5/-4
- `pkg/cmd/pr/shared/commentable.go`: +20/-4
- `pkg/cmd/pr/shared/commentable_test.go`: +25/-55
