def export_blob(data: bytes) -> bytes:
    """Return an export payload without applying renderer preview policy."""
    return bytes(data)
