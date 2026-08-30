# Frozen pull request snapshot

- PR: https://github.com/llvm/llvm-project/pull/212892 — `[HLSL] Generate semantic signature metadata`
- Author: inbelic
- Target base head: `63cc0c35a7c0538fa500b4d164f29d4debb92486`
- Comparison base: `f9d6bef0efd7645ce761f794f6fcbb7f88ad2ad9`
- Exact source head: `88c76edeaa7a542da9b0aac803c79ce8876bd489`
- Diff: 233 additions, 106 deletions, 9 files
- Live mergeability and review state: intentionally unavailable in this historical fixture

## Pull request body

This pr adds support to collect the signature element metadata as they are emitted and outputs them to a named metadata node.

Adds a lit test of the metadata creation.

Resolves https://github.com/llvm/llvm-project/issues/57928

## Linked issues

### https://github.com/llvm/llvm-project/issues/57928 — [CGHLSL][DirectX] Generate module metadata for input output signature

This issue tracks the work of collecting the `SemanticSignatureElement`s in `emitEntryFunction` as described in [the proposal](https://github.com/llvm/wg-hlsl/blob/main/proposals/0047-semantic-signatures-metadata-schema.md#accumulate-semanticsignatureelements).

After collecting the elements it will invoke the packing of the elements and then emit it as metadata using the interfaces from https://github.com/llvm/llvm-project/issues/204878 and https://github.com/llvm/llvm-project/issues/204889.

AC:
- [ ] `SemanticSignatureElement`s are collected in `emitEntryFunction` and wired up to emit packed metadata
- [ ] Codegen LIT tests are to be added to ensure the metadata is correctly linked to the correct `llvm.dx.load.input` and `llvm.dx.store.output` intrinsic calls

## Exact-head checks

- Build and Test Linux${{ (((startsWith(matrix.runs-on, 'depot-ubuntu-24.04-arm') && ' AArch64')) || '') }}: SKIPPED
- greeter: SKIPPED
- buildbot_comment: SUCCESS
- Build and Test Linux AArch64: SUCCESS
- Check LLVM_ABI annotations with ids: SUCCESS
- code_formatter: SUCCESS
- HLSL-Tests (hlsl-macos) / build: SUCCESS
- Build and Test Linux: SUCCESS
- Build and Test Windows: SKIPPED
- Build and Test Windows: SUCCESS
- automate-prs-labels: SUCCESS
- Compute macOS Projects: SKIPPED
- Compute macOS Projects: SUCCESS
- Build and Test macOS arm64: SKIPPED
- Build and Test macOS arm64: SUCCESS
- Graphite / mergeability_check: SUCCESS
- unnamed: SUCCESS
- unnamed: SUCCESS

## Changed files

- `clang/lib/CodeGen/CGHLSLRuntime.cpp`: +145/-43
- `clang/lib/CodeGen/CGHLSLRuntime.h`: +28/-18
- `clang/test/CodeGenHLSL/semantics/semantic.array.output.hlsl`: +5/-0
- `clang/test/CodeGenHLSL/semantics/semantic.input.hlsl`: +11/-0
- `clang/test/CodeGenHLSL/semantics/semantic.output.hlsl`: +11/-0
- `llvm/include/llvm/Analysis/DXILResource.h`: +5/-0
- `llvm/include/llvm/Frontend/HLSL/SemanticSignatures.h`: +10/-0
- `llvm/lib/Analysis/DXILResource.cpp`: +1/-1
- `llvm/unittests/Frontend/HLSLSemanticSignatureMetadataTest.cpp`: +17/-44
