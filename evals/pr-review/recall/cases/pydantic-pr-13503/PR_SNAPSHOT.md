# Frozen pull request snapshot

- PR: https://github.com/pydantic/pydantic/pull/13503 — `Make `FailFast` hashable`
- Author: LuShadowX
- Target base head: `a2a6577d4c329dd574a45dbb01a8feaa16b1ad3d`
- Comparison base: `a2a6577d4c329dd574a45dbb01a8feaa16b1ad3d`
- Exact source head: `e9e156709a6fd42ce0d14bfd9d0c3988f9380916`
- Diff: 3 additions, 0 deletions, 1 files
- Live mergeability and review state: intentionally unavailable in this historical fixture

## Pull request body

## Change Summary

`FailFast` is a `@dataclass` with `eq=True` and no `__hash__`, so Python sets `__hash__ = None` and instances are unhashable. Its siblings in `types.py` all define one — `Strict` hashes `self.strict`, `AllowInfNan` hashes `self.allow_inf_nan` — so `FailFast` looks like an oversight rather than a decision.

It matters because `FailFast` is used as `Annotated` metadata, and anything that hashes the annotation then breaks. Parametrising a generic model is the easiest way to hit it:

```python
from typing import Annotated, Generic, TypeVar
from pydantic import BaseModel, FailFast, Strict

T = TypeVar('T')

class Foo(BaseModel, Generic[T]):
    a: T

Foo[Annotated[list[int], Strict()]]    # fine
Foo[Annotated[list[int], FailFast()]]  # TypeError: unhashable type: 'FailFast'
```

`functools.lru_cache` over a function taking the annotation fails the same way.

This adds `__hash__` to `FailFast`, matching `Strict` and `AllowInfNan`.

## Related issue number

None.

## Checklist

* [x] The pull request title is a good summary of the changes - it will be used in the changelog
* [x] Unit tests for the changes exist
* [x] Tests pass on CI
* [ ] Documentation reflects the changes where applicable — N/A
* [ ] My PR is ready to review, **please add a comment including the phrase "please review" to assign reviewers**


## Linked issues

No closing Issue was linked in the frozen PR metadata.

## Exact-head checks

- Test FastAPI (main branch) on Python ${{ matrix.python-version }}: SKIPPED
- Lint 3.10: SUCCESS
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
- CodSpeed Performance Analysis: FAILURE

## Changed files

- `pydantic/types.py`: +3/-0
