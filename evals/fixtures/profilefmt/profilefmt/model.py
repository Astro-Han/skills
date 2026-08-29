from dataclasses import dataclass


@dataclass
class Profile:
    region: str

    def __post_init__(self):
        self.legacy_country = self.region
