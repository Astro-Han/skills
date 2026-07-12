---
name: wrap-up
description: Close a session cleanly by resolving session-owned loose ends and reporting the final state. Use when the session is ending or the user asks to wrap up or audit its end.
---

# Wrap Up

Finish the current workstream without opening another. Resolve session-owned loose ends before summarizing.

## Reconstruct the footprint

Use the conversation and known artifacts to identify promised outcomes, repositories touched in this session, changed files, worktrees, verification, commits or PRs, background processes or servers, browser sessions, and temporary artifacts. Inspect only what is needed to establish their final state. Do not sweep unrelated repositories, project history, documentation, or memory.

## Close loose ends

1. Confirm every promised outcome is complete and backed by the strongest available verification. Finish missing in-scope work before wrapping up.
2. Run `git status` in every touched repository. Separate work this session does not own from session-owned changes. Finish, verify, and commit session-owned changes when the request and project rules call for it; never stage or alter unrelated work.
3. Stop background processes or servers and browser sessions started by this session unless the user asked to keep them running.
4. Clean session-created temporary artifacts and worktrees when they are no longer needed and contain no valuable, uncommitted, or unpushed work. Move deletions to Trash by default.
5. Fix drift directly caused by this session in documentation or configuration, such as a path, command, status, or workflow note made stale by the change. Do not broaden this into a general audit.
6. Wrap-up does not grant new authority. Complete only already authorized actions. Ask before destructive, remote, public, privacy-sensitive, or materially expanded work.

Run final verification after cleanup: re-run the smallest checks that prove the delivered result, then confirm the touched repositories contain no unexplained session-owned residue. If something cannot be resolved safely, state exactly what remains and why.

## Output

### Session Summary

State what was completed, the important decisions, and the strongest verification evidence.

### Cleanup

Include only actions taken or unresolved state that matters: commits, stopped processes, removed artifacts or worktrees, documentation fixes, and remaining dirty files with their ownership. Omit this section when there is nothing to report.

### Next Steps

Include only concrete unfinished actions, blockers, or decisions. Omit this section when nothing remains.

### Session Name

Suggest exactly one short, natural, searchable title for the dominant workstream. Follow active project naming rules and prefer a PR or issue anchor when one exists.

Keep the whole wrap-up proportional to the session. Use `handoff` instead when the user needs a portable continuation document.
