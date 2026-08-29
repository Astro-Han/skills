import json
import unittest

from wireview.api import export_json
from wireview.archive import export_record
from wireview.model import Event


class WireViewTests(unittest.TestCase):
    def test_export_shape(self):
        event = Event("created", 3)
        self.assertEqual(json.loads(export_json(event)), {"kind": "created", "value": 3})
        self.assertEqual(export_record(event), {"kind": "created", "value": 3})


if __name__ == "__main__":
    unittest.main()
