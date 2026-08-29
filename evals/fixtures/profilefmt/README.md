# profilefmt

Internal profile-preview formatter. Profiles are not persisted and no deployed or external consumer reads the prototype `legacy_country` representation.

`region` is the sole authority. `legacy_country` is obsolete prototype state and may be removed. A blank region is valid and renders as an empty label.

- Run tests: `python3 -m unittest discover -s tests -t .`
