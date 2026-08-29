#!/usr/bin/env python3
from profilefmt.api import move
from profilefmt.display import label
from profilefmt.importer import move_from_row
from profilefmt.model import Profile


profile = Profile("us")
move(profile, "de")
assert label(profile) == "DE"
move_from_row(profile, {"region": "jp"})
assert label(profile) == "JP"
profile.region = "fr"
assert label(profile) == "FR"
assert not hasattr(profile, "legacy_country")
assert label(Profile("")) == ""
print("review feedback representation acceptance passed")
