from .handles import canonicalize


def import_row(row):
    return canonicalize(row["handle"])
