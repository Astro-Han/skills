"""Composition root for a digest run."""

import os
import re
import signal
import sys

from . import config
from .compat.v1 import read_v1_snapshot
from .ingest import fetcher
from .ingest.dedupe import Deduper
from .ingest.normalizer import normalize
from .model.dto import from_dto, to_dto
from .render.digest import render_digest
from .scheduler import BatchCancelled, BatchRunner
from .store.gateway import StoreGateway
from .store.repository import Repository

HEADLINE = re.compile(r"^(?:== (?P<text>.+) ==|<h2>(?P<html>.+)</h2>)$", re.MULTILINE)


def bootstrap(spool_dir):
    repository = Repository(config.STORAGE_BACKEND)
    gateway = StoreGateway(repository)
    snapshot = os.path.join(spool_dir, "snapshot.v1.json")
    if os.path.exists(snapshot):
        for item in read_v1_snapshot(snapshot):
            gateway.save(to_dto(item))
    deduper = Deduper()
    deduper.seed(repository.known_ids())
    return repository, gateway, deduper


def collect(deduper, spool_dir):
    accepted = []
    for path in fetcher.discover(spool_dir):
        document = fetcher.read(path)
        for record in document["items"]:
            item = normalize(record, document["source"])
            if not deduper.is_new(item.item_id):
                continue
            deduper.remember(item.item_id)
            accepted.append(item)
            if len(accepted) >= config.MAX_ITEMS:
                return accepted
    return accepted


def run(spool_dir):
    repository, gateway, deduper = bootstrap(spool_dir)
    accepted = collect(deduper, spool_dir)
    runner = BatchRunner(repository, deduper)
    previous = signal.signal(signal.SIGTERM, lambda *_: runner.cancel())
    try:
        runner.run(accepted)
    except BatchCancelled as cancelled:
        # The run continues after a cancelled batch: the digest below is rendered from
        # whatever the store holds, so a half-applied batch would show up in the output.
        print("batch cancelled at {}; store rolled back".format(cancelled))
    finally:
        signal.signal(signal.SIGTERM, previous)

    digest = render_digest([from_dto(dto) for dto in gateway.load_all()],
                           config.load_output_format(spool_dir))

    first = HEADLINE.search(digest)
    lead = (first.group("text") or first.group("html")) if first else "(empty)"
    print("digest lead section: {}".format(lead))
    print("items seen: {} / stored: {}".format(deduper.count(), gateway.size()))
    return digest


if __name__ == "__main__":
    print(run(sys.argv[1] if len(sys.argv) > 1 else "spool"))
