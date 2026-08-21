"""Reproduces the export job: builds two monthly reports in one process."""

from reportlib.builder import ReportBuilder
from reportlib.render import render_text

january = ReportBuilder("January").add_section("sales", [100, 200, 300])
february = ReportBuilder("February").add_section("returns", [50])

print(render_text(january.build()))
print()
print(render_text(february.build()))
