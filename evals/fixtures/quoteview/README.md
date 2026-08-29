# quoteview

Internal, preview-only quote calculator. Results are displayed immediately and are never persisted, charged, or sent outside the process.

`LineItem` is the shared domain type used by every current producer and is the sole owner of intrinsic line-item validity. A line item quantity must be positive. Producers own parsing only; `Quote` owns aggregation only.

- Run tests: `python3 -m unittest discover -s tests -t .`
