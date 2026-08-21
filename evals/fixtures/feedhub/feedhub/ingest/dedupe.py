"""Tracks which item ids the pipeline knows about."""


class Deduper:
    def __init__(self):
        self._seen = set()

    def seed(self, item_ids):
        self._seen.update(item_ids)

    def is_new(self, item_id):
        return item_id not in self._seen

    def remember(self, item_id):
        self._seen.add(item_id)

    def count(self):
        return len(self._seen)
