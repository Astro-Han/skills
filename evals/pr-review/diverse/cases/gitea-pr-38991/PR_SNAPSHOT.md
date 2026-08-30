# Frozen pull request snapshot

- PR: https://github.com/go-gitea/gitea/pull/38991 — `enhance(ui): forced colors mode enhancements`
- Author: silverwind
- Target base head: `ed4d7ea08df377463e288af7378318e198e3e34e`
- Comparison base: `ed4d7ea08df377463e288af7378318e198e3e34e`
- Exact source head: `d686146222b2b1cd02b3de91c313b8897adebb17`
- Diff: 46 additions, 0 deletions, 4 files
- Live mergeability and review state: intentionally unavailable in this historical fixture

## Pull request body

Improve various UI elements while in [forced color mode](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@media/forced-colors). Tested in Firefox and Chrome, untestable in Safari as it does not implement forced color mode currently.

Before and after screenshots from Chrome's color emulation mode:

<img width="280" alt="dark-BEFORE" src="https://github.com/user-attachments/assets/7d7579fc-3abb-40f3-8b5a-0b66565104af" />
<img width="280" alt="dark-AFTER" src="https://github.com/user-attachments/assets/d1d889e2-717a-4e4a-aa00-6b5e27c1c8b9" />

<img width="280" alt="chromium-light-BEFORE" src="https://github.com/user-attachments/assets/00172deb-1934-45a7-8fb2-07cd7cc867aa" />
<img width="280" alt="chromium-light-AFTER" src="https://github.com/user-attachments/assets/5cb04c12-bf86-45db-a476-237314fdbe61" />




## Linked issues

No closing Issue was linked in the frozen PR metadata.

## Exact-head checks

- files-changed / detect: SUCCESS
- files-changed / detect: SUCCESS
- files-changed / detect: SUCCESS
- files-changed / detect: SUCCESS
- giteabot: SUCCESS
- giteabot: SUCCESS
- giteabot: SUCCESS
- labeler: SUCCESS
- lint-backend: SKIPPED
- test-pgsql-shard-1: SKIPPED
- container-amd64: SKIPPED
- test-e2e: SUCCESS
- pr-title: SUCCESS
- test-pgsql-shard-2: SKIPPED
- container-arm64: SKIPPED
- lint-on-demand: SUCCESS
- checks-backend: SKIPPED
- test-sqlite: SKIPPED
- container-riscv64: SKIPPED
- test-unit: SKIPPED
- frontend: SUCCESS
- backend: SKIPPED
- test-mysql: SKIPPED
- test-mssql: SKIPPED
- unnamed: SUCCESS

## Changed files

- `web_src/css/base.css`: +10/-0
- `web_src/css/modules/checkbox.css`: +23/-0
- `web_src/css/modules/label.css`: +7/-0
- `web_src/css/repo.css`: +6/-0
