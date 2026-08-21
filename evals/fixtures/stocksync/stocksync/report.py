def format_drift(drift):
    lines = ["drift report"]
    for name in sorted(drift):
        value = drift[name]
        sign = "+" if value > 0 else ""
        lines.append("  {}: {}{}".format(name, sign, value))
    return "\n".join(lines)
