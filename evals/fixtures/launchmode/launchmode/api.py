from .model import LaunchConfig


def enable(config: LaunchConfig) -> None:
    config.mode = "enabled"
