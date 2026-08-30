def canonical_email(value: str) -> str:
    return value.strip()


def canonical_bucket(value: str) -> str:
    return value.strip().lower()


def clean_label(value: str) -> str:
    return value.strip().lower()
