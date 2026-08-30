# Frozen pull request snapshot

- PR: https://github.com/django/django/pull/21750 — `Fixed #37260 -- Avoided DDL when altering only Python-level on_delete options.`
- Author: adamchainz
- Target base head: `4ee04972e7f9163dbdf5a7c36330e3379187e187`
- Comparison base: `4ee04972e7f9163dbdf5a7c36330e3379187e187`
- Exact source head: `e4900fe6743fd262e30b2d6a88d986644649fe07`
- Diff: 88 additions, 1 deletions, 4 files
- Live mergeability and review state: intentionally unavailable in this historical fixture

## Pull request body

#### Trac ticket number

ticket-37260

#### Branch description

Regression in 0c487aa3a7b2417481bf48c1e5355c855873e210.

Support for database-level delete options removed "on_delete" from `Field.non_db_attrs` because changes to or from the new `DB_CASCADE`, `DB_SET_DEFAULT`, and `DB_SET_NULL` options require schema changes. As a consequence, an `AlterField` changing only a Python-level `on_delete` option (such as `CASCADE` to `PROTECT`) performs unnecessary schema changes when it was previously a no-op at the database level.

This commit makes `ForeignObject.non_db_attrs` a property that includes `"on_delete"`only when the option is not a database-level one, so that:

- Python-level to Python-level changes skip DDL again,
- changes to, from, or between database-level options still alter the field.

#### AI Assistance Disclosure (REQUIRED)

- [ ] **No AI tools were used** in preparing this PR.
- [x] **If AI tools were used**, I have disclosed which ones, and fully reviewed and verified their output.

Claude 5 Fable did nearly all the work here, discovering the bug and writing the commit. I made minor edits. I agree with the report and approach.

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
- docs: SUCCESS
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
- unnamed: PENDING
- unnamed: PENDING
- unnamed: PENDING
- unnamed: PENDING
- unnamed: PENDING
- unnamed: PENDING
- unnamed: PENDING
- unnamed: PENDING
- unnamed: PENDING
- unnamed: PENDING
- unnamed: PENDING
- unnamed: PENDING
- unnamed: PENDING
- unnamed: PENDING
- unnamed: PENDING
- unnamed: PENDING
- unnamed: PENDING
- unnamed: PENDING
- unnamed: PENDING
- unnamed: PENDING
- unnamed: PENDING
- unnamed: PENDING
- unnamed: PENDING
- unnamed: PENDING
- unnamed: SUCCESS

## Changed files

- `django/db/models/fields/related.py`: +8/-0
- `docs/releases/6.1.1.txt`: +5/-0
- `tests/migrations/test_operations.py`: +27/-0
- `tests/schema/tests.py`: +48/-1
