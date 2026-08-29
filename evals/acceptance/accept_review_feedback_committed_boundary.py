from transferlog.api import commit
from transferlog.importer import commit_row
from transferlog.ledger import Ledger


ledger = Ledger()
for producer in (lambda: commit(ledger, 0), lambda: commit_row(ledger, {"amount": "-2"})):
    try:
        producer()
    except ValueError:
        pass
    else:
        raise AssertionError("non-positive transfer was accepted")
assert ledger.count() == 0
