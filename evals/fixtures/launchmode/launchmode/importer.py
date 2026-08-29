from .model import LaunchConfig


def apply_row(config: LaunchConfig, row: dict[str, str]) -> None:
    config.mode = row["mode"]
