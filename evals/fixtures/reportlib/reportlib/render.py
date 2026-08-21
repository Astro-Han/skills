_RENDER_CACHE = {}


def render_text(report):
    cache_key = (
        report["title"],
        tuple((name, len(rows)) for name, rows in report["sections"]),
    )
    if cache_key in _RENDER_CACHE:
        return _RENDER_CACHE[cache_key]
    lines = ["# " + report["title"]]
    for name, rows in report["sections"]:
        lines.append("## {} ({} rows)".format(name, len(rows)))
    text = "\n".join(lines)
    _RENDER_CACHE[cache_key] = text
    return text
