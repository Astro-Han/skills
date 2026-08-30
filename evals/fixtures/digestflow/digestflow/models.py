from dataclasses import dataclass


@dataclass
class Task:
    id: str
    preset: str
    host: str
    connection: str | None
    permission: str
    state: str = "active"


@dataclass
class Session:
    id: str
    task_id: str
    preset: str
    root_id: str
    revision: int
    state: str
    artifact: str | None


class TargetCatalog:
    def __init__(self, targets):
        self.targets = set(targets)

    def is_ready(self, host, connection):
        return (host, connection) in self.targets

    def unique_connection(self, host):
        matches = [connection for target_host, connection in self.targets if target_host == host]
        return matches[0] if len(matches) == 1 else None
