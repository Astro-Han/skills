# Offline pull request packet

- Title: `fix(buffer): flush a single queued item`
- Author: river
- Base: main
- Reviewed content: the attached `PATCH.diff`, exported from a pull request
- Head SHA: unavailable in the export
- PR URL: not included
- Linked Issue: none
- CI, mergeability, reviews, and unresolved threads: unavailable
- Diff: 10 additions, 1 deletion, 2 files
- Split: production 1 addition, 1 deletion; tests 9 additions, 0 deletions

A support report includes a reproduction: enqueue one item, close the producer, and observe that
the consumer receives nothing. Enqueuing two items flushes both. The attached log shows
`pending=1` immediately before shutdown and no later write.

The patch changes the buffer owner to flush whenever at least one item is pending and adds one
regression test for the single-item case. Review the supplied change even though the export has no
live repository metadata. Do not assume that it matches the current pull-request head.
