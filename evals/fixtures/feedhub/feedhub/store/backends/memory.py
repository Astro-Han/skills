"""In-process backend. Contents are lost when the process exits."""


class MemoryBackend:
    def __init__(self):
        self._rows = {}

    def put(self, key, row):
        self._rows[key] = row

    def fetch(self, key):
        return self._rows.get(key)

    def fetch_all(self):
        return list(self._rows.values())

    def delete(self, key):
        self._rows.pop(key, None)

    def size(self):
        return len(self._rows)
