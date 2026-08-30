# Frozen pull request snapshot

- PR: https://github.com/pydantic/pydantic/pull/13536 — `Revert "Make `FailFast` hashable"`
- Author: davidhewitt
- Target base head: `ec80ed3e1b941c1edabe7d9e5a2053a1b0580383`
- Comparison base: `ec80ed3e1b941c1edabe7d9e5a2053a1b0580383`
- Exact source head: `b911c7901a9c55a6535f69d746a8198d16f02e52`
- Diff: 0 additions, 3 deletions, 1 files
- Live mergeability and review state: intentionally unavailable in this historical fixture

## Pull request body

Reverts pydantic/pydantic#13503

See https://github.com/pydantic/pydantic/pull/13503#issuecomment-5115655524

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
- Cloudflare Pages: SUCCESS
- CodSpeed Performance Analysis: SUCCESS
- unnamed: SUCCESS

## Changed files

- `pydantic/types.py`: +0/-3
