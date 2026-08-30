# policyflow

Email is a case-insensitive recipient identity and `canonical_email` owns its
normalization. Bucket keys are case-sensitive external identifiers and only surrounding
whitespace is removed by `canonical_bucket`. Display labels preserve user-selected case
while trimming whitespace.

`legacy_route` is read by deployed dispatch scanners and must remain in exports. There is
no current locale-policy or generic text-normalization contract.
