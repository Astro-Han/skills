class Section:
    def __init__(self, name, rows):
        self.name = name
        self.rows = rows


class ReportBuilder:
    def __init__(self, title, sections=[]):
        self.title = title
        self.sections = sections

    def add_section(self, name, rows):
        self.sections.append(Section(name, rows))
        return self

    def build(self):
        return {
            "title": self.title,
            "sections": [(s.name, list(s.rows)) for s in self.sections],
        }
