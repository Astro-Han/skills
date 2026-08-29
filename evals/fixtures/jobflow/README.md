# jobflow

Internal, in-memory job preview. No state is persisted or sent externally.

`Job.transition` is the sole owner of lifecycle changes and their history. API and worker layers issue transition commands only. Every transition request, including a same-state transition, is recorded in history.

- Run tests: `python3 -m unittest discover -s tests -t .`
