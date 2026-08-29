from dataclasses import dataclass, field

from .model import Transfer


@dataclass
class Ledger:
    entries: list[Transfer] = field(default_factory=list)

    def append(self, transfer: Transfer) -> None:
        self.entries.append(transfer)

    def count(self) -> int:
        return len(self.entries)
