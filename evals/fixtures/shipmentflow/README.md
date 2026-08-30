# shipmentflow

Holdout for testing whether review feedback is grouped only when the underlying rules
are actually shared.

Recipient email is a case-insensitive identity: trim it and use one canonical lowercase
form everywhere. Display names are presentation data: trim surrounding whitespace but
preserve the user's case. These rules intentionally have different owners.

`legacy_route` is still consumed by deployed label scanners. Exports must preserve it
when present until those readers are retired; it is not an obsolete duplicate.
