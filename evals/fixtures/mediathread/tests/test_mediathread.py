import unittest

from mediathread import Session, clone_session, export_blob, render


class MediaThreadTests(unittest.TestCase):
    def test_text_rendering_escapes_markup(self):
        self.assertEqual(render("<hello>"), "<p>&lt;hello&gt;</p>")

    def test_clone_preserves_both_text_authorities(self):
        source = Session(("hello",), ("hello",))
        self.assertEqual(clone_session(source), source)

    def test_export_preserves_payload(self):
        self.assertEqual(export_blob(b"payload"), b"payload")


if __name__ == "__main__":
    unittest.main()
