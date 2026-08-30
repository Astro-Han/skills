# Frozen pull request snapshot

- PR: https://github.com/home-assistant/core/pull/180627 — `Migrate the Lyngdorf number platform to the lyngdorf 2.0 API`
- Author: fishloa
- Target base head: `8094598c2fe8f6ea13322d4ceb294841ee85f2f0`
- Comparison base: `8094598c2fe8f6ea13322d4ceb294841ee85f2f0`
- Exact source head: `8259f5f576ab2e67d048f12995759c55a363d1f8`
- Diff: 110 additions, 60 deletions, 4 files
- Live mergeability and review state: intentionally unavailable in this historical fixture

## Pull request body

## Proposed change

Trims are a mapping of controls in lyngdorf 2.0 rather than a per-band triple
of attributes, so the six trims become one lookup each and the entity
description loses a field. Writes are awaited.

Entity creation still keys off `range_fn`: on 1.11 `lipsync` is `None` until
the device reports, so keying off the control would drop the entity at
startup. New test covers that.

Diagnostics snapshot: `lipsync` 50 -> 50.0, the library returns a float there.

## Type of change

- [ ] Dependency upgrade
- [ ] Bugfix (non-breaking change which fixes an issue)
- [ ] New integration (thank you!)
- [ ] New feature (which adds functionality to an existing integration)
- [ ] Deprecation (breaking change to happen in the future)
- [ ] Breaking change (fix/feature causing existing functionality to break)
- [x] Code quality improvements to existing code or addition of tests

## Additional information

- This PR fixes or closes issue: fixes #
- This PR is related to issue: 
- Link to documentation pull request: 
- Link to developer documentation pull request: 
- Link to frontend pull request: 

The 1.11.0 bump this builds on merged in #180528.

## Checklist

- [x] I understand the code I am submitting and can explain how it works.
- [x] The code change is tested and works locally.
- [x] Local tests pass. **Your PR cannot be merged unless tests pass**
- [x] There is no commented out code in this PR.
- [x] I have followed the [development checklist][dev-checklist]
- [x] I have followed the [perfect PR recommendations][perfect-pr]
- [x] The code has been formatted using Ruff (`ruff format homeassistant tests`)
- [x] Tests have been added to verify that the new code works.
- [ ] Any generated code has been carefully reviewed for correctness and compliance with project standards.

If user exposed functionality or configuration variables are added/changed:

- [ ] Documentation added/updated for [www.home-assistant.io][docs-repository]

If the code communicates with devices, web services, or third-party tools:

- [ ] The [manifest file][manifest-docs] has all fields filled out correctly.  
      Updated and included derived files by running: `python3 -m script.hassfest`.
- [ ] New or updated dependencies have been added to `requirements_all.txt`.  
      Updated by running `python3 -m script.gen_requirements_all`.
- [ ] For the updated dependencies a diff between library versions and ideally a link to the changelog/release notes is added to the PR description.

To help with the load of incoming pull requests:

- [ ] I have reviewed two other [open pull requests][prs] in this repository.

[prs]: https://github.com/home-assistant/core/pulls?q=is%3Aopen+is%3Apr+-author%3A%40me+-draft%3Atrue+-label%3Awaiting-for-upstream+sort%3Acreated-desc+review%3Anone+-status%3Afailure

[dev-checklist]: https://developers.home-assistant.io/docs/development_checklist/
[manifest-docs]: https://developers.home-assistant.io/docs/creating_integration_manifest/
[quality-scale]: https://developers.home-assistant.io/docs/integration_quality_scale_index/
[docs-repository]: https://github.com/home-assistant/home-assistant.io
[perfect-pr]: https://developers.home-assistant.io/docs/review-process/#creating-the-perfect-pr


## Linked issues

No closing Issue was linked in the frozen PR metadata.

## Exact-head checks

- Collect information & changes data: SUCCESS
- Run prek checks: SUCCESS
- Check GitHub Actions workflows: SUCCESS
- Check Dockerfile: SUCCESS
- Check Dockerfile.dev: SUCCESS
- Check script/hassfest/docker/Dockerfile: SUCCESS
- Prepare dependencies (3.14.5): SUCCESS
- Check copilot instructions: SUCCESS
- Check recorder database versions: SKIPPED
- Check hassfest: SUCCESS
- Check all requirements: SUCCESS
- Dependency review: SKIPPED
- Audit licenses: SKIPPED
- Check pylint: SUCCESS
- Check pylint on tests: SUCCESS
- Check mypy: SUCCESS
- Split tests for full run: SKIPPED
- Run ${{ matrix.mariadb-group }} tests Python ${{ matrix.python-version }}: SKIPPED
- Run ${{ matrix.postgresql-group }} tests Python ${{ matrix.python-version }}: SKIPPED
- Run SQLite ${{ matrix.sqlite-group.version }} tests Python ${{ matrix.python-version }}: SKIPPED
- Run tests Python 3.14.5 (lyngdorf): SUCCESS
- Run tests Python ${{ matrix.python-version }} (${{ matrix.group }}): SKIPPED
- Upload test coverage to Codecov (partial suite): SUCCESS
- Upload test coverage to Codecov (full suite): SKIPPED
- Upload test results to Codecov: SKIPPED
- unnamed: SUCCESS
- unnamed: SUCCESS
- unnamed: SUCCESS
- unnamed: SUCCESS
- codecov/patch: SUCCESS
- unnamed: SUCCESS
- codecov/patch/required: SUCCESS
- unnamed: SUCCESS
- codecov/project: SUCCESS
- unnamed: SUCCESS
- codecov/project/required: SUCCESS
- unnamed: SUCCESS
- unnamed: SUCCESS
- unnamed: SUCCESS

## Changed files

- `homeassistant/components/lyngdorf/number.py`: +33/-31
- `tests/components/lyngdorf/conftest.py`: +38/-4
- `tests/components/lyngdorf/snapshots/test_diagnostics.ambr`: +1/-1
- `tests/components/lyngdorf/test_number.py`: +38/-24
