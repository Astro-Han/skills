from .policy import normalize_size


def preview_row(row: dict[str, str]) -> int:
    return normalize_size(row["batch_size"])
