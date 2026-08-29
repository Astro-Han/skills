# handlekit

Internal account-preview utility. Handles are never persisted by this package.

`canonicalize` is the sole owner of handle normalization: trim surrounding whitespace and apply Unicode-aware case folding. API and import producers own parsing only and must not repeat normalization rules.

- Run tests: `python3 -m unittest discover -s tests -t .`
