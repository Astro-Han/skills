from html import escape


def render(markdown: str) -> str:
    return f"<p>{escape(markdown)}</p>"
