# Frozen pull request snapshot

- PR: https://github.com/django/django/pull/21690 — `Fixed #37224 -- Skipped questioner for changes on unmanaged model fields.`
- Author: vishy0
- Target base head: `cef2346abf8d6e9e61a5a3599fbcf72163e6a6e5`
- Comparison base: `3d34265d5d1b83fee5df3c1b6f55087b1a6a1ded`
- Exact source head: `34248cdceba3d8155f60dd6b33b0ca87b004239f`
- Diff: 64 additions, 1 deletions, 2 files
- Live mergeability and review state: intentionally unavailable in this historical fixture

## Pull request body

#### Trac ticket number
<!-- Replace XXXXX with the corresponding Trac ticket number. -->
<!-- Or delete the line and write "N/A - typo" for typo fixes. -->

ticket-37224

#### Branch description
Short-circuits the migration questioner for unmanaged models when adding NOT NULL fields or altering null to NOT NULL, since unmanaged models don't own their database schema and no DDL is executed for them.

#### AI Assistance Disclosure (REQUIRED)
<!-- Select exactly ONE of the following: -->
- [x] **No AI tools were used** in preparing this PR.
- [ ] **If AI tools were used**, I have disclosed which ones, and fully reviewed and verified their output.
<!-- If AI tools were used, provide which tools were used here. -->

#### Checklist
- [x] This PR follows the [contribution guidelines](https://docs.djangoproject.com/en/stable/internals/contributing/writing-code/submitting-patches/).
- [x] This PR **does not** disclose a security vulnerability (see [vulnerability reporting](https://docs.djangoproject.com/en/stable/internals/security/)).
- [x] This PR targets the `main` branch. <!-- Backports will be evaluated and done by mergers, when necessary. -->
- [x] The commit message is written in past tense, mentions the ticket number (if applicable), and ends with a period (see [guidelines](https://docs.djangoproject.com/en/dev/internals/contributing/committing-code/#committing-guidelines)).
- [x] I have not requested, and will not request, an automated AI review for this PR. <!-- You are welcome to do so in your own fork. -->

<!-- Leave the following items unchecked if not applicable. -->
- [x] I have checked the "Has patch" ticket flag in the Trac system.
- [x] I have added or updated relevant tests.
- [x] I have added or updated relevant docs, including release notes if applicable.
- [ ] I have attached screenshots in both light and dark modes for any UI changes.


## Linked issues

No closing Issue was linked in the frozen PR metadata.

## Exact-head checks

- Run_benchmarks: SKIPPED
- check-commit-prefix: SKIPPED
- Coverage Tests (PostgreSQL): SKIPPED
- PostgreSQL ${{ matrix.pg_major }}, Python ${{ matrix.python }}: SKIPPED
- define-matrix: SKIPPED
- SQLite: SKIPPED
- Screenshots: SKIPPED
- Check test migrations: SUCCESS
- flake8: SUCCESS
- Run Quality Checks on a PR: SUCCESS
- Windows, SQLite, Python 3.14: SUCCESS
- python: SKIPPED
- PostgreSQL: SKIPPED
- check-commit-suffix: SUCCESS
- isort: SUCCESS
- Ubuntu, SQLite, Python 3.14t: SUCCESS
- black: SUCCESS
- JavaScript tests: SUCCESS
- zizmor: SUCCESS
- Scripts tests: SUCCESS
- biome: SUCCESS
- unnamed: SUCCESS
- unnamed: SUCCESS
- unnamed: SUCCESS
- unnamed: SUCCESS
- unnamed: SUCCESS
- unnamed: SUCCESS
- unnamed: SUCCESS
- unnamed: SUCCESS
- unnamed: SUCCESS
- unnamed: SUCCESS
- unnamed: SUCCESS
- unnamed: SUCCESS
- unnamed: SUCCESS
- unnamed: SUCCESS
- unnamed: SUCCESS
- unnamed: SUCCESS
- unnamed: SUCCESS
- unnamed: SUCCESS
- unnamed: SUCCESS
- unnamed: SUCCESS
- unnamed: SUCCESS
- unnamed: SUCCESS
- unnamed: SUCCESS
- unnamed: SUCCESS
- unnamed: SUCCESS

## Changed files

- `django/db/migrations/autodetector.py`: +14/-1
- `tests/migrations/test_autodetector.py`: +50/-0
