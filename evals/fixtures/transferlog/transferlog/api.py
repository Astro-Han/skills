from .ledger import Ledger
from .model import Transfer


def commit(ledger: Ledger, amount: int) -> None:
    ledger.append(Transfer(amount))
