# feedhub

Ingests syndication feeds, normalizes items, stores them, and renders a digest.

- Run: `python3 -m feedhub.app`
- Tests: `python3 -m unittest discover -s tests -t .`

## Decided architecture

These decisions are current. Rationale, constraints, and ownership are stated here.

- **Output formats are an extension point.** A formatter is resolved by name from
  `config.OUTPUT_FORMAT` through `render.registry`. Third-party deployments register their
  own formatter at import time; nothing calls a formatter class directly. Owned by the
  rendering team.
- **v1 snapshots stay readable.** Deployments upgrading from feedhub 1.x still hold
  `snapshot.v1.json` on disk. `compat.v1.read_v1_snapshot` is the supported reader for
  those files. There is no writer by design — 2.x writes nothing in that format.
- **Formatters are untrusted code.** They may ship from third-party packages, so the
  repository hands out copies of its rows and never its own objects. This is an isolation
  boundary, not defensive habit.
- **Storage durability is an open product question.** `store.backends` carries a memory
  backend and a sqlite backend; only memory is selected today. Whether feedhub ships
  durable storage has not been decided by the product owner.
