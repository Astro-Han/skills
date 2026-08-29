from .policy import normalize_size


def preview(raw: str) -> int:
    return normalize_size(raw)
