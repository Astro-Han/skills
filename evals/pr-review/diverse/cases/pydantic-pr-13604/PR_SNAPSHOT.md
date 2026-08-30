# Frozen pull request snapshot

- PR: https://github.com/pydantic/pydantic/pull/13604 — `Fix support for callable discriminators with PEP 695 type aliases`
- Author: Viicos
- Target base head: `5922459fcf33d9a8767fd0fd25a982bbf0d7668d`
- Comparison base: `5922459fcf33d9a8767fd0fd25a982bbf0d7668d`
- Exact source head: `0575cb8e4396393420d5b4ced88da37de80e69b8`
- Diff: 47 additions, 13 deletions, 3 files
- Live mergeability and review state: intentionally unavailable in this historical fixture

## Pull request body

<!-- Thank you for your contribution! -->
<!-- Unless your change is trivial, please create an issue to discuss the change before creating a PR -->

## Change Summary

Follow up on https://github.com/pydantic/pydantic/pull/12785. Fixes https://github.com/pydantic/pydantic/issues/13599.

<!-- Please give a short summary of the changes. -->

## Related issue number

<!-- WARNING: please use "fix #123" style references so the issue is closed when this PR is merged. -->

## Checklist

* [ ] The pull request title is a good summary of the changes - it will be used in the changelog
* [ ] Unit tests for the changes exist
* [ ] Tests pass on CI
* [ ] Documentation reflects the changes where applicable
* [ ] My PR is ready to review, **please add a comment including the phrase "please review" to assign reviewers**


## Linked issues

### https://github.com/pydantic/pydantic/issues/13599 — PEP 695 type aliases don't work with callable discriminators

### Initial Checks

- [x] I confirm that I'm using Pydantic V2

### Description

New type aliases prefixed with the type keyword are not supported as the type annotation for a callable discriminator.

M1, M2, M4 ok
M3
```
pydantic.errors.PydanticUserError: `Tag` not provided for choice {'type': 'definition-ref', 'schema_ref': '__main__.TaggedAnyA:2210408548368'} used with `Discriminator`
```

Example Code from #12843 also doesn’t work.

### Example Code

```Python
import traceback
from sys import stderr

from pydantic import BaseModel, Discriminator, Field, Tag
from typing_extensions import Annotated, Any, Literal, TypeAlias


class A(BaseModel):
    type_: str

class A1(A):
    type_: Literal['A1'] = Field(alias='type')

class A2(A):
    type_: Literal['A2'] = Field(alias='type')

def _discriminator(data: Any) -> str:
    if isinstance(data, dict):
        return data['type']
    return data.type_

discriminator = Discriminator(_discriminator)

type AnyA = A1 | A2
AnyA_old: TypeAlias = A1 | A2

type TaggedAnyA = Annotated[A1, Tag('A1')] | Annotated[A2, Tag('A2')]
TaggedAnyA_old: TypeAlias = Annotated[A1, Tag('A1')] | Annotated[A2, Tag('A2')]


_data = {"a" : {'type': 'A1'}}
try:
    class M1(BaseModel):
        a: AnyA = Field(discriminator='type_')

    M1.model_validate(_data)
except Exception as e:
    traceback.print_exc()
else:
    print("OK", file=stderr)

try:
    class M2(BaseModel):
        a: AnyA_old = Field(discriminator='type_')

    M2.model_validate(_data)
except Exception as e:
    traceback.print_exc()
else:
    print("OK", file=stderr)

try:
    class M3(BaseModel):
        a: TaggedAnyA = Field(discriminator=discriminator)

    M3.model_validate(_data)
except Exception as e:
    traceback.print_exc()
else:
    print("OK", file=stderr)

try:
    class M4(BaseModel):
        a: TaggedAnyA_old = Field(discriminator=discriminator)

    M4.model_validate(_data)
except Exception as e:
    traceback.print_exc()
else:
    print("OK", file=stderr)
```

### Python, Pydantic & OS Version

```Text
pydantic version: 2.13.4
        pydantic-core version: 2.46.4
          pydantic-core build: profile=release pgo=false
               python version: 3.14.7 (tags/v3.14.7:823f032, Aug  5 2026, 10:51:32) [MSC v.1944 64 bit (AMD64)]
                     platform: Windows-11-10.0.26200-SP0
             related packages: mypy-2.3.0 typing_extensions-4.16.0
                       commit: unknown
```

## Exact-head checks

- check-assignment: SKIPPED
- Test FastAPI (main branch) on Python ${{ matrix.python-version }}: SKIPPED
- Lint 3.10: SUCCESS
- CodSpeed profiling: SUCCESS
- Lint 3.11: SUCCESS
- Lint 3.12: SUCCESS
- Lint 3.13: SUCCESS
- Lint 3.14: SUCCESS
- Lint 3.15: SUCCESS
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
- Test ubuntu-latest / 3.15: SUCCESS
- Test ubuntu-latest / 3.15t: SUCCESS
- Test ubuntu-latest / pypy3.11: SUCCESS
- Test macos-latest / 3.10: SUCCESS
- Test macos-latest / 3.11: SUCCESS
- Test macos-latest / 3.12: SUCCESS
- Test macos-latest / 3.13: SUCCESS
- Test macos-latest / 3.14: SUCCESS
- Test macos-latest / 3.15: SUCCESS
- Test macos-latest / 3.15t: SUCCESS
- Test macos-latest / pypy3.11: SUCCESS
- Test windows-latest / 3.10: SUCCESS
- Test windows-latest / 3.11: SUCCESS
- Test windows-latest / 3.12: SUCCESS
- Test windows-latest / 3.13: SUCCESS
- Test windows-latest / 3.14: SUCCESS
- Test windows-latest / 3.15: SUCCESS
- Test windows-latest / 3.15t: SUCCESS
- Test windows-latest / pypy3.11: SUCCESS
- Test macos-15-intel / 3.15: SUCCESS
- Test macos-15-intel / 3.15t: SUCCESS
- Test Redis OM Python (main branch) on Python ${{ matrix.python-version }}: SKIPPED
- Test Pydantic plugin: SUCCESS
- Test Django Ninja (main branch) on Python ${{ matrix.python-version }}: SKIPPED
- Mypy typechecking tests: SUCCESS
- Test FastDepends (main branch) on Python ${{ matrix.python-version }}: SKIPPED
- Typechecking integration tests: SUCCESS
- Test MCP Python SDK (main branch) on Python ${{ matrix.python-version }}: SKIPPED
- Test typing-extensions (`main` branch) on Python 3.10: SUCCESS
- Test typing-extensions (`main` branch) on Python 3.11: SUCCESS
- Test typing-extensions (`main` branch) on Python 3.12: SUCCESS
- Test typing-extensions (`main` branch) on Python 3.13: SUCCESS
- Test typing-extensions (`main` branch) on Python 3.14: SUCCESS
- Test typing-extensions (`main` branch) on Python 3.15: SUCCESS
- core / Test build on ${{ matrix.target }}-${{ matrix.distro }}: SKIPPED
- Test FastMCP (main branch) on Python ${{ matrix.python-version }}: SKIPPED
- core / Test build on ${{ matrix.platform.os }}: SKIPPED
- Create an issue if tests failed: SKIPPED
- Test build on PyEmscripten (Pyodide) (3.14): SUCCESS
- coverage-combine: SUCCESS
- check: SUCCESS
- coverage-pr-comment: SUCCESS
- release-pydantic-core: SKIPPED
- release-pydantic: SKIPPED
- Send tweet: SKIPPED
- Cloudflare Pages: SUCCESS
- CodSpeed Performance Analysis: SUCCESS
- Macroscope - Correctness Check: SUCCESS
- Veria AI - PR Review: SUCCESS
- unnamed: SUCCESS

## Changed files

- `pydantic/_internal/_discriminated_union.py`: +1/-1
- `pydantic/types.py`: +25/-12
- `tests/types/unions/test_discriminated_union.py`: +21/-0
