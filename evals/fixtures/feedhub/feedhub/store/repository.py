"""The authority for stored items."""

from dataclasses import asdict

from ..model.item import Item
from .backends import get_backend


class Repository:
    def __init__(self, backend_name):
        self._backend = get_backend(backend_name)

    def add(self, item):
        self._backend.put(item.item_id, asdict(item))

    def get(self, item_id):
        row = self._backend.fetch(item_id)
        return self._row_to_item(row) if row else None

    def all_items(self):
        return [self._row_to_item(row) for row in self._backend.fetch_all()]

    def known_ids(self):
        return {row["item_id"] for row in self._backend.fetch_all()}

    def forget(self, item_id):
        self._backend.delete(item_id)

    def count(self):
        return self._backend.size()

    def _row_to_item(self, row):
        # A fresh Item per read: formatters are third-party code and must never receive
        # a row this repository still owns.
        return Item(**dict(row))
