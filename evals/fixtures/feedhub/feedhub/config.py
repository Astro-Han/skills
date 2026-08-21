"""Runtime configuration for feedhub.

The values here are defaults. An operator drops a feedhub.conf next to the spool
directory to override them; that file is deployment data, not repository data.
"""

import os

OUTPUT_FORMAT = "text"
STORAGE_BACKEND = "memory"
MAX_ITEMS = 200

# Kept from the 1.x date migration; 2.x always publishes ISO timestamps.
USE_LEGACY_DATES = False

FEED_GLOB = "*.feed.json"


def load_output_format(spool_dir):
    """Return the formatter name this deployment asked for."""
    conf = os.path.join(spool_dir, "feedhub.conf")
    if not os.path.exists(conf):
        return OUTPUT_FORMAT
    with open(conf) as handle:
        for line in handle:
            key, _, value = line.partition("=")
            if key.strip() == "output_format":
                return value.strip()
    return OUTPUT_FORMAT
