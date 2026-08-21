# feedhub — answer key

Ground truth for the `simplify-audit` fixture. Kept outside `feedhub/` so an audit run
never reads it. Audit target: `evals/fixtures/feedhub`.

## Should be reported (7)

| id | Concept | Where | Rule it exercises |
| --- | --- | --- | --- |
| P1 | `StoreGateway` delegates every method to `Repository` | `store/gateway.py` | pass-through layer |
| P2 | `ItemDTO` + `to_dto`/`from_dto` duplicate `Item`, converted and converted back | `model/dto.py` | duplicate representation. **Cascade**: its only consumer is P1 |
| P3 | `USE_LEGACY_DATES` is never true and has no producer | `config.py`, `ingest/normalizer.py` | config branch with one live value |
| P4 | `collect_render_metrics` has no production caller | `metrics.py` | production API kept alive by tests |
| P5 | `Deduper._seen` is a second authority on known ids, written in three places; rollback forgets in the repository only, so the two diverge — visible as `items seen: 3 / stored: 0` | `ingest/dedupe.py`, `app.py`, `scheduler.py` | mirrored state kept consistent by synchronization |
| P6 | `HEADLINE` re-parses the rendered digest for a value the items already carry | `app.py` | serialize-then-reparse |
| P7 | `match_glob` hand-rolls `fnmatch` | `util/globbing.py` | hand-rolled infrastructure |

## Must survive (4)

| id | Looks deletable because | Why it stays |
| --- | --- | --- |
| T1 | Nothing constructs `HtmlFormatter`; it only registers itself by name | `spool/feedhub.conf` sets `output_format = html`, so the shipped run renders HTML. Reachable only by checking configuration, not the call graph |
| T2 | `read_v1_snapshot` has no writer and no snapshot file in the spool | README states 1.x deployments still hold `snapshot.v1.json`; a persisted-data obligation with no writer by design |
| T3 | `_cancelled` and `_applied` look like two mechanisms for one lifecycle fact | Only `_applied` can undo a partial batch. `app.run` catches `BatchCancelled` and still renders the digest, so a missing rollback would show up in the output |
| T4 | `Repository._row_to_item` builds a fresh object on every read | README declares formatters untrusted third-party code; this is an isolation boundary, not a same-process defensive habit |

## Must be escalated, not deleted (1)

`SqliteBackend` is implemented and never selected. The README states durable storage is an
open product question. Correct placement is the decision-gate tier; reporting it as a closed
candidate is the failure this item exists to catch.

## Scoring

Free-text audit reports resist regex scoring — heading formats vary and models mix scratch
reasoning into the report. Score with a judge model against this table and state the method
alongside the number. Expect per-item noise; differences of two or three hits across eight
reps are not results.

`Item.body` is carried end-to-end and never rendered. It was not planted; it is real and
correctly reported.
