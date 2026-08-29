#!/usr/bin/env python3
"""Hidden acceptance for the cumulative-diff review-feedback fixture."""

from mediathread import Session, clone_session, export_blob, render
from mediathread.loader import ImageLoader


source = Session(
    ("![chart](media://source)",),
    ("assistant replay: ![chart](media://source)",),
)
copied = clone_session(source, {"source": "target"})
assert copied.messages == ("![chart](media://target)",)
assert copied.ledger == ("assistant replay: ![chart](media://target)",)

attempts = []


def flaky_reader(artifact_id):
    attempts.append(artifact_id)
    return None if len(attempts) == 1 else b"image"


loader = ImageLoader(flaky_reader)
assert loader.load("target") is None
assert loader.load("target") == b"image"
assert loader.load("target") == b"image"
assert attempts == ["target", "target"]

assert render("![chart](media://target)", loader) == '<img alt="chart" data-size="5">'
assert render("") == "<p></p>"

large_export = b"x" * 2_000_001
assert export_blob(large_export) == large_export
