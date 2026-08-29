from .model import Session


def clone_session(session: Session) -> Session:
    return Session(tuple(session.messages), tuple(session.ledger))
