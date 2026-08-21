"""Builds the digest document."""

from . import html_formatter, registry, text_formatter  # noqa: F401  (registration)
from .. import config


def render_digest(items, output_format=None):
    formatter = registry.resolve(output_format or config.OUTPUT_FORMAT)
    lines = []
    for source in sorted({item.source for item in items}):
        lines.append(formatter.heading(source))
        for item in items:
            if item.source == source:
                lines.append(formatter.entry(item.title, item.published))
    return "\n".join(lines)
