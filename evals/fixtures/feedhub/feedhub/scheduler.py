"""Runs ingest batches so a cancelled batch leaves no half-applied state."""


class BatchCancelled(Exception):
    pass


class BatchRunner:
    def __init__(self, repository, deduper):
        self._repository = repository
        self._deduper = deduper
        self._cancelled = False
        self._applied = []

    def cancel(self):
        self._cancelled = True

    def run(self, items):
        self._applied = []
        try:
            for item in items:
                if self._cancelled:
                    raise BatchCancelled(item.item_id)
                self._repository.add(item)
                self._deduper.remember(item.item_id)
                self._applied.append(item.item_id)
        except BatchCancelled:
            self._roll_back()
            raise
        return len(self._applied)

    def _roll_back(self):
        # _cancelled says a stop was requested; _applied says what this batch actually
        # wrote. Only the second can undo a partial batch, and only the first arrives
        # from another thread.
        for item_id in reversed(self._applied):
            self._repository.forget(item_id)
        self._applied = []
