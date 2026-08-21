from .registry import register


class TextFormatter:
    def heading(self, source):
        return "== {} ==".format(source)

    def entry(self, title, published):
        return "- {} ({})".format(title, published)


register("text", TextFormatter)
