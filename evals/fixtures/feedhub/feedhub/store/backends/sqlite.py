"""Durable backend. Not selected by any current configuration."""

import json
import sqlite3


class SqliteBackend:
    def __init__(self, path=":memory:"):
        self._conn = sqlite3.connect(path)
        self._conn.execute("CREATE TABLE IF NOT EXISTS items (key TEXT PRIMARY KEY, row TEXT)")

    def put(self, key, row):
        self._conn.execute("INSERT OR REPLACE INTO items VALUES (?, ?)", (key, json.dumps(row)))
        self._conn.commit()

    def fetch(self, key):
        cur = self._conn.execute("SELECT row FROM items WHERE key = ?", (key,))
        found = cur.fetchone()
        return json.loads(found[0]) if found else None

    def fetch_all(self):
        return [json.loads(r[0]) for r in self._conn.execute("SELECT row FROM items")]

    def delete(self, key):
        self._conn.execute("DELETE FROM items WHERE key = ?", (key,))
        self._conn.commit()

    def size(self):
        return self._conn.execute("SELECT COUNT(*) FROM items").fetchone()[0]
