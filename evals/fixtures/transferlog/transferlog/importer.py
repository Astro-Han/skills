from .ledger import Ledger
from .model import Transfer


def commit_row(ledger: Ledger, row: dict[str, str]) -> None:
    ledger.append(Transfer(int(row["amount"])))
