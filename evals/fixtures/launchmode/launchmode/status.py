from .model import LaunchConfig


def is_enabled(config: LaunchConfig) -> bool:
    return config.legacy_enabled
