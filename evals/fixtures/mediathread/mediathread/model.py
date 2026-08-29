from dataclasses import dataclass


@dataclass(frozen=True)
class Session:
    messages: tuple[str, ...]
    ledger: tuple[str, ...]
