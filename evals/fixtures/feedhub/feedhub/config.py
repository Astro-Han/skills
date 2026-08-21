"""Runtime configuration for feedhub."""

OUTPUT_FORMAT = "text"
STORAGE_BACKEND = "memory"
MAX_ITEMS = 200

# Kept from the 1.x date migration; 2.x always publishes ISO timestamps.
USE_LEGACY_DATES = False

FEED_GLOB = "*.feed.json"
