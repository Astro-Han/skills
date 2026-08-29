from dataclasses import dataclass


@dataclass
class Credential:
    token: str
    legacy_token: str = ""

    def active(self) -> bool:
        return bool(self.token)
