# Frozen pull request snapshot

- PR: https://github.com/home-assistant/core/pull/176857 — `Update stored host on Overkiz local gateway rediscovery`
- Author: iMicknl
- Target base head: `eccfff20b6f0c5ea44345e9545a939d967b8bc94`
- Comparison base: `eccfff20b6f0c5ea44345e9545a939d967b8bc94`
- Exact source head: `a1637a5469173a9f69672e3d647a6c2254b96bee`
- Diff: 34 additions, 3 deletions, 3 files
- Live mergeability and review state: intentionally unavailable in this historical fixture

## Pull request body

## Proposed change
<!--
  Describe the big picture of your changes here to communicate to the
  maintainers why we should accept this pull request. If it fixes a bug
  or resolves a feature request, be sure to link to that issue in the
  additional information section.
-->

When an Overkiz gateway in developer mode (`_kizboxdev` zeroconf) is rediscovered, the flow aborted as `already_configured` without refreshing the stored host. Developer mode stores the advertised host and port (rather than deriving them from the static gateway id like the `_kizbox`/DHCP paths), so a changed port left `CONF_HOST` stale.

This now passes the advertised host through `_abort_if_unique_id_configured(updates=...)` to keep it current. The derived `_kizbox`/DHCP and cloud paths are left unchanged.

## Type of change
<!--
  What type of change does your PR introduce to Home Assistant?
  NOTE: Please, check only 1! box!
  If your PR requires multiple boxes to be checked, you'll most likely need to
  split it into multiple PRs. This makes things easier and faster to code review.
-->

- [ ] Dependency upgrade
- [ ] Bugfix (non-breaking change which fixes an issue)
- [ ] New integration (thank you!)
- [ ] New feature (which adds functionality to an existing integration)
- [ ] Deprecation (breaking change to happen in the future)
- [ ] Breaking change (fix/feature causing existing functionality to break)
- [x] Code quality improvements to existing code or addition of tests

## Additional information
<!--
  Details are important, and help maintainers processing your PR.
  Please be sure to fill out additional details, if applicable.
-->

- This PR fixes or closes issue: fixes #
- This PR is related to issue: 
- Link to documentation pull request: 
- Link to developer documentation pull request: 
- Link to frontend pull request: 

## Checklist
<!--
  Put an `x` in the boxes that apply. You can also fill these out after
  creating the PR. If you're unsure about any of them, don't hesitate to ask.
  We're here to help! This is simply a reminder of what we are going to look
  for before merging your code.

  AI tools are welcome, but contributors are responsible for *fully*
  understanding the code before submitting a PR.
-->

- [x] I understand the code I am submitting and can explain how it works.
- [x] The code change is tested and works locally.
- [x] Local tests pass. **Your PR cannot be merged unless tests pass**
- [x] There is no commented out code in this PR.
- [x] I have followed the [development checklist][dev-checklist]
- [x] I have followed the [perfect PR recommendations][perfect-pr]
- [x] The code has been formatted using Ruff (`ruff format homeassistant tests`)
- [x] Tests have been added to verify that the new code works.
- [x] Any generated code has been carefully reviewed for correctness and compliance with project standards.

If user exposed functionality or configuration variables are added/changed:

- [ ] Documentation added/updated for [www.home-assistant.io][docs-repository]

If the code communicates with devices, web services, or third-party tools:

- [ ] The [manifest file][manifest-docs] has all fields filled out correctly.  
      Updated and included derived files by running: `python3 -m script.hassfest`.
- [ ] New or updated dependencies have been added to `requirements_all.txt`.  
      Updated by running `python3 -m script.gen_requirements_all`.
- [ ] For the updated dependencies a diff between library versions and ideally a link to the changelog/release notes is added to the PR description.

<!--
  This project is very active and we have a high turnover of pull requests.

  Unfortunately, the number of incoming pull requests is higher than what our
  reviewers can review and merge so there is a long backlog of pull requests
  waiting for review. You can help here!
  
  By reviewing another pull request, you will help raise the code quality of
  that pull request and the final review will be faster. This way the general
  pace of pull request reviews will go up and your wait time will go down.
  
  When picking a pull request to review, try to choose one that hasn't yet
  been reviewed.

  Thanks for helping out!
-->

To help with the load of incoming pull requests:

- [ ] I have reviewed two other [open pull requests][prs] in this repository.

[prs]: https://github.com/home-assistant/core/pulls?q=is%3Aopen+is%3Apr+-author%3A%40me+-draft%3Atrue+-label%3Awaiting-for-upstream+sort%3Acreated-desc+review%3Anone+-status%3Afailure

<!--
  Thank you for contributing <3

  Below, some useful links you could explore:
-->
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
- Run tests Python 3.14.5 (overkiz): SUCCESS
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

- `homeassistant/components/overkiz/config_flow.py`: +7/-2
- `homeassistant/components/overkiz/quality_scale.yaml`: +1/-1
- `tests/components/overkiz/test_config_flow.py`: +26/-0
