import json

from wireview.api import export_json
from wireview.archive import export_record
from wireview.model import Event


event = Event("UserCreated", 3)
assert json.loads(export_json(event))["kind"] == "usercreated"
assert export_record(event)["kind"] == "usercreated"
assert event.kind == "UserCreated"
assert json.dumps({}) == "{}"
