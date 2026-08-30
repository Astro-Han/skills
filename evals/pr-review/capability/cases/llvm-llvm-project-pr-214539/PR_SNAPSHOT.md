# Frozen pull request snapshot

- PR: https://github.com/llvm/llvm-project/pull/214539 — `[mlir][linalg] TileUsingFor - variadic tiles and interchange`
- Author: adam-smnk
- Target base head: `7c31d55c29ae0eb60f3ddcec5e1bf35942f6ed94`
- Comparison base: `849c51e082b0958524246a0a880f46d468a55147`
- Exact source head: `5740cf3fca1ede16e83b9b1258bc350e99476ee3`
- Diff: 682 additions, 75 deletions, 7 files
- Live mergeability and review state: intentionally unavailable in this historical fixture

## Pull request body

Extends the 'structured.tile_using_for' op to accept packed handle containing variable number of tile sizes, and dynamic and packed loop interchange values.

Packed handles allows for runtime tiling decisions which improves transform schedule flexibility and reusability.
The extension follows the existing approach used by other tiling ops.

Assisted-by: Claude

## Linked issues

No closing Issue was linked in the frozen PR metadata.

## Exact-head checks

- Build and Test Linux${{ (((startsWith(matrix.runs-on, 'depot-ubuntu-24.04-arm') && ' AArch64')) || '') }}: SKIPPED
- greeter: SKIPPED
- buildbot_comment: SUCCESS
- Build and Test Linux AArch64: SUCCESS
- Check LLVM_ABI annotations with ids: SUCCESS
- code_formatter: SUCCESS
- Build and Test Linux: SUCCESS
- Build and Test Windows: SKIPPED
- Build and Test Windows: SUCCESS
- automate-prs-labels: SUCCESS
- Compute macOS Projects: SKIPPED
- Compute macOS Projects: SUCCESS
- Build and Test macOS arm64: SKIPPED
- Build and Test macOS arm64: SKIPPED
- Graphite / mergeability_check: SUCCESS
- unnamed: SUCCESS
- unnamed: SUCCESS

## Changed files

- `mlir/include/mlir/Dialect/Linalg/TransformOps/LinalgTransformOps.td`: +35/-4
- `mlir/include/mlir/Dialect/Transform/Utils/Utils.h`: +51/-4
- `mlir/lib/Dialect/Linalg/TransformOps/LinalgTransformOps.cpp`: +185/-45
- `mlir/lib/Dialect/Transform/Utils/Utils.cpp`: +12/-4
- `mlir/python/mlir/dialects/transform/structured.py`: +46/-13
- `mlir/test/Dialect/Linalg/transform-op-tile.mlir`: +304/-5
- `mlir/test/python/dialects/transform_structured_ext.py`: +49/-0
