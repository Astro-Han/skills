"""Storage backends. Only one is selected at a time by config.STORAGE_BACKEND."""

from .memory import MemoryBackend
from .sqlite import SqliteBackend

_BACKENDS = {"memory": MemoryBackend, "sqlite": SqliteBackend}


def get_backend(name):
    try:
        return _BACKENDS[name]()
    except KeyError:
        raise ValueError("unknown storage backend: {}".format(name))
