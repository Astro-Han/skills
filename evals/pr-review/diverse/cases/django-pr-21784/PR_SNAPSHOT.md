# Frozen pull request snapshot

- PR: https://github.com/django/django/pull/21784 — `Fixed #37278 -- Made QuerySet.totally_ordered understand aliases to pure Col/ColPairs.`
- Author: jacobtylerwalls
- Target base head: `3436cf9bce84bb1f6877ad96819637366b27b719`
- Comparison base: `3436cf9bce84bb1f6877ad96819637366b27b719`
- Exact source head: `ea088d64c2c437f7c79f10b6b641b47fe252c052`
- Diff: 75 additions, 14 deletions, 4 files
- Live mergeability and review state: intentionally unavailable in this historical fixture

## Pull request body

#### Trac ticket number
ticket-37278

#### Branch description
If an annotation is a pure alias to a field (e.g., no transform), then `totally_ordered` can understand it and possibly return `True`. Before, these annotations were skipped, so the property always returned `False`.

#### AI Assistance Disclosure (REQUIRED)
<!-- Please select exactly ONE of the following: -->
- [x] **No AI tools were used** in preparing this PR.
- [ ] **If AI tools were used**, I have disclosed which ones, and fully reviewed and verified their output.

#### Checklist
- [x] This PR follows the [contribution guidelines](https://docs.djangoproject.com/en/stable/internals/contributing/writing-code/submitting-patches/).
- [x] This PR **does not** disclose a security vulnerability (see [vulnerability reporting](https://docs.djangoproject.com/en/stable/internals/security/)).
- [x] This PR targets the `main` branch. <!-- Backports will be evaluated and done by mergers, when necessary. -->
- [x] The commit message is written in past tense, mentions the ticket number, and ends with a period (see [guidelines](https://docs.djangoproject.com/en/dev/internals/contributing/committing-code/#committing-guidelines)).
- [x] I have not requested, and will not request, an automated AI review for this PR. <!-- You are welcome to do so in your own fork. -->
- [x] I have checked the "Has patch" ticket flag in the Trac system.
- [x] I have added or updated relevant tests.
- [x] I have added or updated relevant docs, including release notes if applicable.
- [x] I have attached screenshots in both light and dark modes for any UI changes.

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

- `django/db/models/query.py`: +36/-14
- `tests/composite_pk/test_order_by.py`: +6/-0
- `tests/ordering/models.py`: +2/-0
- `tests/ordering/tests.py`: +31/-0
