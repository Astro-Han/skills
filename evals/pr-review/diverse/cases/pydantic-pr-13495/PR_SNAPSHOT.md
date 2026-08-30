# Frozen pull request snapshot

- PR: https://github.com/pydantic/pydantic/pull/13495 — `Return `NotImplemented` from URL ordering comparisons with foreign types`
- Author: chinesepowered
- Target base head: `a2a6577d4c329dd574a45dbb01a8feaa16b1ad3d`
- Comparison base: `a2a6577d4c329dd574a45dbb01a8feaa16b1ad3d`
- Exact source head: `7e46eea237f3149ed723c6879b5a369b728f2768`
- Diff: 34 additions, 4 deletions, 2 files
- Live mergeability and review state: intentionally unavailable in this historical fixture

## Pull request body

## Change Summary

The ordering comparisons on `_BaseUrl` (`__lt__`, `__gt__`, `__le__`, `__ge__`) returned `False` when the other operand was a different class, rather than `NotImplemented`. Returning `False` from all four breaks the ordering contract in two visible ways:

```python
from pydantic import AnyUrl, HttpUrl

a, b = AnyUrl('https://a.com'), HttpUrl('https://b.com')

a < b    # False
a >= b   # False   ← both False is impossible for a total order

sorted([AnyUrl('https://z.com'), HttpUrl('https://b.com')])
# ['https://z.com/', 'https://b.com/']  — silently unsorted, no TypeError
```

Comparing against an unrelated type such as `str` or `int` had the same problem: `AnyUrl(...) < 'x'` returned `False` instead of raising.

Returning `NotImplemented` when the classes differ lets Python try the reflected operation and then raise `TypeError` if neither side can order the pair — the standard protocol for rich comparisons. Same-class ordering is unchanged.

`__eq__` is deliberately left as-is: equality against a foreign type is well defined and correctly returns `False`, so it should keep doing so. Only the four ordering methods were wrong.

## Related issues

No existing issue or PR — found none open or closed covering URL ordering.

## Checklist

* [x] The pull request title is a good summary of the changes
* [x] Unit tests for the changes exist
* [x] Documentation reflects the changes where applicable
* [x] `pydantic-cli` / changes are backwards compatible where possible


## Linked issues

No closing Issue was linked in the frozen PR metadata.

## Exact-head checks

- Test FastAPI (main branch) on Python ${{ matrix.python-version }}: SKIPPED
- Lint 3.10: SUCCESS
- check-assignment: SUCCESS
- CodSpeed profiling: SUCCESS
- Lint 3.11: SUCCESS
- Lint 3.12: SUCCESS
- Lint 3.13: SUCCESS
- Lint 3.14: SUCCESS
- Test SQLModel (main branch) on Python ${{ matrix.python-version }}: SKIPPED
- core / Build sdist: SUCCESS
- core / Build on ${{ matrix.os }} (${{ matrix.target }} - ${{ (matrix.interpreter || 'all') }}${{ (((matrix.os == 'linux') && format(' - {0}', (((matrix.manylinux == 'auto') && 'manylinux') || matrix.manylinux))) || '') }}): SKIPPED
- Test Beanie (main branch) on Python ${{ matrix.python-version }}: SKIPPED
- core / Build PGO-optimized on ${{ matrix.platform.os }} / ${{ matrix.interpreter }}: SKIPPED
- Test openapi-python-client (main branch) on Python ${{ matrix.python-version }}: SKIPPED
- Test Pandera (main branch) on Python ${{ matrix.python-version }}: SKIPPED
- core / Build PyEmscripten (3.14): SUCCESS
- Test ODMantic (main branch) on Python ${{ matrix.python-version }}: SKIPPED
- core / Run Rust benchmarks: SUCCESS
- Test Polar (main branch) on Python ${{ matrix.python-version }}: SKIPPED
- core / Test on ubuntu: SUCCESS
- core / Test on macos: SUCCESS
- core / Test on windows: SUCCESS
- Test BentoML (main branch) on Python ${{ matrix.python-version }}: SKIPPED
- core / Test MSRV: SUCCESS
- Test Semantic Kernel (main branch) on Python ${{ matrix.python-version }}: SKIPPED
- core / Test with debug build (3.13): SUCCESS
- core / Test with debug build (pypy3.11): SUCCESS
- build-pydantic: SKIPPED
- Test LangChain (main branch) on Python ${{ matrix.python-version }}: SKIPPED
- Test Dify (main branch) on Python ${{ matrix.python-version }}: SKIPPED
- docs-build: SUCCESS
- Test Cadwyn (main branch) on Python ${{ matrix.python-version }}: SKIPPED
- Test memray: SUCCESS
- Test pydantic-xml (main branch) on Python ${{ matrix.python-version }}: SKIPPED
- Test ubuntu-latest / 3.10: SUCCESS
- Test ubuntu-latest / 3.11: SUCCESS
- Test ubuntu-latest / 3.12: SUCCESS
- Test ubuntu-latest / 3.13: SUCCESS
- Test ubuntu-latest / 3.14: SUCCESS
- Test ubuntu-latest / 3.14t: SUCCESS
- Test ubuntu-latest / pypy3.11: SUCCESS
- Test macos-latest / 3.10: SUCCESS
- Test macos-latest / 3.11: SUCCESS
- Test macos-latest / 3.12: SUCCESS
- Test macos-latest / 3.13: SUCCESS
- Test macos-latest / 3.14: SUCCESS
- Test macos-latest / 3.14t: SUCCESS
- Test macos-latest / pypy3.11: SUCCESS
- Test windows-latest / 3.10: SUCCESS
- Test windows-latest / 3.11: SUCCESS
- Test windows-latest / 3.12: SUCCESS
- Test windows-latest / 3.13: SUCCESS
- Test windows-latest / 3.14: SUCCESS
- Test windows-latest / 3.14t: SUCCESS
- Test windows-latest / pypy3.11: SUCCESS
- Test macos-15-intel / 3.14: SUCCESS
- Test macos-15-intel / 3.14t: SUCCESS
- Test Redis OM Python (main branch) on Python ${{ matrix.python-version }}: SKIPPED
- Test Pydantic plugin: SUCCESS
- Test Django Ninja (main branch) on Python ${{ matrix.python-version }}: SKIPPED
- Mypy typechecking tests: SUCCESS
- Test FastDepends (main branch) on Python ${{ matrix.python-version }}: SKIPPED
- Typechecking integration tests: SUCCESS
- Create an issue if tests failed: SKIPPED
- Test typing-extensions (`main` branch) on Python 3.10: SUCCESS
- Test typing-extensions (`main` branch) on Python 3.11: SUCCESS
- Test typing-extensions (`main` branch) on Python 3.12: SUCCESS
- Test typing-extensions (`main` branch) on Python 3.13: SUCCESS
- Test typing-extensions (`main` branch) on Python 3.14: SUCCESS
- core / Test build on ${{ matrix.target }}-${{ matrix.distro }}: SKIPPED
- core / Test build on ${{ matrix.platform.os }}: SKIPPED
- Test build on PyEmscripten (Pyodide) (3.14): SUCCESS
- coverage-combine: SUCCESS
- check: SUCCESS
- coverage-pr-comment: SUCCESS
- release-pydantic-core: SKIPPED
- release-pydantic: SKIPPED
- Send tweet: SKIPPED
- CodSpeed Performance Analysis: SUCCESS

## Changed files

- `pydantic/networks.py`: +12/-4
- `tests/test_networks.py`: +22/-0
