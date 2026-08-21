"""Reads raw feed documents from the spool directory."""

import json
import os

from .. import config
from ..util.globbing import match_glob


def discover(spool_dir):
    if not os.path.isdir(spool_dir):
        return []
    return sorted(
        os.path.join(spool_dir, name)
        for name in os.listdir(spool_dir)
        if match_glob(config.FEED_GLOB, name)
    )


def read(path):
    with open(path) as handle:
        return json.load(handle)
