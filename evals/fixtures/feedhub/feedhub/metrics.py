"""Digest size accounting."""


def collect_render_metrics(digest):
    return {
        "lines": len(digest.splitlines()),
        "characters": len(digest),
        "sections": sum(1 for line in digest.splitlines() if line.startswith("== ")),
    }
