# Frozen pull request snapshot

- PR: https://github.com/llvm/llvm-project/pull/219348 — `[Clang][RISCV] Add packed widening add/sub intrinsics`
- Author: Michael-Chen-NJU
- Target base head: `316b0edee400b3ef72ed0a082dae9bd337ac01a0`
- Comparison base: `316b0edee400b3ef72ed0a082dae9bd337ac01a0`
- Exact source head: `82642e1638b6c98b6ec78c025aa2e972f45f0d9f`
- Diff: 553 additions, 5 deletions, 6 files
- Live mergeability and review state: intentionally unavailable in this historical fixture

## Pull request body

Add packed widening add/sub header wrappers for the RISC-V P extension using generic vector IR.

## Linked issues

No closing Issue was linked in the frozen PR metadata.

## Exact-head checks

- Build and Test Linux AArch64: CANCELLED
- Build and Test Linux${{ (((startsWith(matrix.runs-on, 'depot-ubuntu-24.04-arm') && ' AArch64')) || '') }}: SKIPPED
- greeter: SKIPPED
- buildbot_comment: SUCCESS
- Check LLVM_ABI annotations with ids: SUCCESS
- code_formatter: SUCCESS
- Build and Test Linux: SUCCESS
- Build and Test Windows: SKIPPED
- Build and Test Windows: SUCCESS
- automate-prs-labels: SUCCESS
- Compute macOS Projects: SKIPPED
- Compute macOS Projects: SUCCESS
- Build and Test macOS arm64: CANCELLED
- Build and Test macOS arm64: SKIPPED
- Graphite / mergeability_check: SUCCESS
- unnamed: SUCCESS
- unnamed: SUCCESS

## Changed files

- `clang/lib/Headers/riscv_packed_simd.h`: +17/-0
- `clang/test/CodeGen/RISCV/rvp-intrinsics.c`: +208/-0
- `cross-project-tests/intrinsic-header-tests/riscv_packed_simd.c`: +74/-0
- `llvm/lib/Target/RISCV/RISCVISelLowering.cpp`: +67/-0
- `llvm/lib/Target/RISCV/RISCVInstrInfoP.td`: +36/-0
- `llvm/test/CodeGen/RISCV/rvp-simd-32.ll`: +151/-5
