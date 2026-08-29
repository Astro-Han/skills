from dataclasses import dataclass


@dataclass
class LaunchConfig:
    mode: str = "disabled"
    legacy_enabled: bool = False
