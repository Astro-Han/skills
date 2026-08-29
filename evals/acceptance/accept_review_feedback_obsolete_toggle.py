from dataclasses import fields

from launchmode.api import enable
from launchmode.importer import apply_row
from launchmode.model import LaunchConfig
from launchmode.status import is_enabled


assert [field.name for field in fields(LaunchConfig)] == ["mode"]
config = LaunchConfig()
enable(config)
assert is_enabled(config)
apply_row(config, {"mode": "disabled"})
assert not is_enabled(config)
apply_row(config, {"mode": ""})
assert not is_enabled(config)
