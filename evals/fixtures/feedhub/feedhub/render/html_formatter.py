from .registry import register


class HtmlFormatter:
    def heading(self, source):
        return "<h2>{}</h2>".format(source)

    def entry(self, title, published):
        return "<li>{} <time>{}</time></li>".format(title, published)


register("html", HtmlFormatter)
