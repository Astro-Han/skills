from dataclasses import dataclass, field


@dataclass
class Subscription:
    id: str
    state: str
    legacy_channel: str | None = None
    history: list[str] = field(default_factory=list)

    def transition(self, new_state: str) -> None:
        self.state = new_state


@dataclass
class Session:
    id: str
    root_id: str
    revision: int
    state: str
