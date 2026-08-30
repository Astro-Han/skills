# Frozen pull request snapshot

- PR: https://github.com/home-assistant/core/pull/180405 — `Fix timeout of endpoint does not crash Portainer update`
- Author: erwindouna
- Target base head: `855850cd2f78803970d62b4af41ea62bd1577037`
- Comparison base: `855850cd2f78803970d62b4af41ea62bd1577037`
- Exact source head: `4b50350be6d957e13c5a5bd40718ce04f1d7bbb3`
- Diff: 298 additions, 164 deletions, 3 files
- Live mergeability and review state: intentionally unavailable in this historical fixture

## Pull request body

<!--
  You are amazing! Thanks for contributing to our project!
  Please, DO NOT DELETE ANY TEXT from this template! (unless instructed).
-->
## Breaking change
<!--
  If your PR contains a breaking change for existing users, it is important
  to tell them what breaks, how to make it work again and why we did this.
  This piece of text is published with the release notes, so it helps if you
  write it towards our users, not us.
  Note: Remove this section if this PR is NOT a breaking change.
-->


## Proposed change
<!--
  Describe the big picture of your changes here to communicate to the
  maintainers why we should accept this pull request. If it fixes a bug
  or resolves a feature request, be sure to link to that issue in the
  additional information section.
-->
Fix for when there's a listed endpoint, but it's unreachable (local vs remote), it would cause timeouts. This fix prevents the update cycle from crashing and can continue on the reachable endpoints.
Users should disable the entry they don't want to have actively monitored in Portainer (to follow the HA standard).

## Type of change
<!--
  What type of change does your PR introduce to Home Assistant?
  NOTE: Please, check only 1! box!
  If your PR requires multiple boxes to be checked, you'll most likely need to
  split it into multiple PRs. This makes things easier and faster to code review.
-->

- [ ] Dependency upgrade
- [x] Bugfix (non-breaking change which fixes an issue)
- [ ] New integration (thank you!)
- [ ] New feature (which adds functionality to an existing integration)
- [ ] Deprecation (breaking change to happen in the future)
- [ ] Breaking change (fix/feature causing existing functionality to break)
- [ ] Code quality improvements to existing code or addition of tests

## Additional information
<!--
  Details are important, and help maintainers processing your PR.
  Please be sure to fill out additional details, if applicable.
-->

- This PR fixes or closes issue: fixes https://github.com/home-assistant/core/issues/156745
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
  understanding the code before submitting a PR. Please follow our AI policy:
  https://developers.home-assistant.io/docs/ai_policy
-->

- [ ] I understand the code I am submitting and can explain how it works.
- [ ] The code change is tested and works locally.
- [ ] Local tests pass. **Your PR cannot be merged unless tests pass**
- [ ] There is no commented out code in this PR.
- [ ] I have followed the [development checklist][dev-checklist]
- [ ] I have followed the [perfect PR recommendations][perfect-pr]
- [ ] The code has been formatted using Ruff (`ruff format homeassistant tests`)
- [ ] Tests have been added to verify that the new code works.
- [ ] Any generated code has been carefully reviewed for correctness and compliance with project standards.

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

### https://github.com/home-assistant/core/issues/156745 — Portainer doesn't support multiple environments

### The problem

I run portainer and have 2 environments setup within it - a local one and a remote one.
This integration only seems to find the first one in the environments list, which in my case is the remote one, and won't connect to it.
You need to be able to specify which environment to connect to.

### What version of Home Assistant Core has the issue?

core-2025.11.2

### What was the last working version of Home Assistant Core?

_No response_

### What type of installation are you running?

Home Assistant Container

### Integration causing the issue

Portainer

### Link to integration documentation on our website

https://www.home-assistant.io/integrations/portainer

### Diagnostics information

_No response_

### Example YAML snippet

```yaml

```

### Anything in the logs that might be useful for us?

```txt
2025-11-17 11:34:57.418 ERROR (MainThread) [homeassistant.components.portainer.coordinator] Unexpected error fetching portainer data
Traceback (most recent call last):
  File "/usr/local/lib/python3.13/site-packages/pyportainer/pyportainer.py", line 125, in _request
    response = await self._session.request(
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    ...<5 lines>...
    )
    ^
  File "/usr/local/lib/python3.13/site-packages/aiohttp/client.py", line 779, in _request
    resp = await handler(req)
           ^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.13/site-packages/aiohttp/client.py", line 757, in _connect_and_send_request
    await resp.start(conn)
  File "/usr/local/lib/python3.13/site-packages/aiohttp/client_reqrep.py", line 539, in start
    message, payload = await protocol.read()  # type: ignore[union-attr]
                       ^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.13/site-packages/aiohttp/streams.py", line 680, in read
    await self._waiter
asyncio.exceptions.CancelledError
The above exception was the direct cause of the following exception:
Traceback (most recent call last):
  File "/usr/local/lib/python3.13/site-packages/pyportainer/pyportainer.py", line 124, in _request
    async with asyncio.timeout(timeout):
               ~~~~~~~~~~~~~~~^^^^^^^^^
  File "/usr/local/lib/python3.13/asyncio/timeouts.py", line 116, in __aexit__
    raise TimeoutError from exc_val
TimeoutError
The above exception was the direct cause of the following exception:
Traceback (most recent call last):
  File "/usr/src/homeassistant/homeassistant/helpers/update_coordinator.py", line 403, in _async_refresh
    self.data = await self._async_update_data()
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/src/homeassistant/homeassistant/components/portainer/coordinator.py", line 136, in _async_update_data
    containers = await self.portainer.get_containers(endpoint.id)
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.13/site-packages/pyportainer/pyportainer.py", line 199, in get_containers
    containers = await self._request(f"endpoints/{endpoint_id}/docker/containers/json?all=1")
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.13/site-packages/pyportainer/pyportainer.py", line 135, in _request
    raise PortainerTimeoutError(msg) from err
pyportainer.exceptions.PortainerTimeoutError: Timeout error while accessing GET http://192.168.1.14:9000/api/endpoints/3/docker/containers/json?all=1:
```

### Additional information

In my instance, this seems to be trying to access environment 3, but my local portainer environment is environment 5.

http://192.168.1.14:9000/api/endpoints/3/docker/containers/json?all=1

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
- Run tests Python 3.14.5 (portainer): FAILURE
- Run tests Python ${{ matrix.python-version }} (${{ matrix.group }}): SKIPPED
- Upload test coverage to Codecov (partial suite): SKIPPED
- Upload test coverage to Codecov (full suite): SKIPPED
- Upload test results to Codecov: SKIPPED
- unnamed: SUCCESS
- unnamed: SUCCESS
- unnamed: SUCCESS
- unnamed: SUCCESS
- unnamed: SUCCESS
- unnamed: SUCCESS

## Changed files

- `homeassistant/components/portainer/coordinator.py`: +180/-160
- `tests/components/portainer/test_binary_sensor.py`: +52/-1
- `tests/components/portainer/test_sensor.py`: +66/-3
