from credrotate.api import rotate
from credrotate.importer import rotate_row
from credrotate.model import Credential


credential = Credential("v1")
rotate(credential, "v2")
assert (credential.token, credential.legacy_token) == ("v2", "v1")
rotate_row(credential, {"token": "v3"})
assert (credential.token, credential.legacy_token) == ("v3", "v2")
assert not Credential("").active()
