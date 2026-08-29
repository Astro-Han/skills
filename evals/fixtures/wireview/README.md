# wireview

`Event.to_wire()` is the sole owner of the wire representation. All exporters must serialize that representation unchanged. The wire contract requires a case-insensitive normalized `kind`, while the in-memory event retains the producer's spelling.

Python's `json.dumps({})` is valid and returns an empty JSON object.
