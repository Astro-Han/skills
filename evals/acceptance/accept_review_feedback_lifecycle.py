#!/usr/bin/env python3
from jobflow.api import complete
from jobflow.model import Job
from jobflow.worker import fail


completed = Job()
complete(completed)
assert completed.status == "done"
assert completed.history == ["pending", "done"]

failed = Job()
fail(failed)
assert failed.status == "failed"
assert failed.history == ["pending", "failed"]

direct = Job()
direct.transition("done")
direct.transition("done")
assert direct.history == ["pending", "done", "done"]
print("review feedback lifecycle acceptance passed")
