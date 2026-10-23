# Product

The NACC Attribute Deriver derives variable values ("attributes") from NACC
study data for the National Alzheimer's Coordinating Center. It is a Python
library packaged as the `nacc-attribute-deriver` wheel/sdist and consumed by the
Attribute Curation gear in
[flywheel-gear-extensions](https://github.com/naccdata/flywheel-gear-extensions).

## What it does

- Reads file and subject metadata from a Flywheel `SymbolTable` (a dict that
  understands dot-notation keys like `file.info.forms.json.visitdate`).
- Applies **curation rules** (defined in `config/curation_rules.csv`) to compute
  **derived attributes** and writes them back into the same table.
- Each rule names a `_create_`/`_missingness_` function in the attribute
  registry, a target `location`, an `operation` (update, latest, min, set, ...),
  and whether the value is `dated`.

## Core concepts

- **Raw attributes**: values that come directly from a file, under
  `file.info.forms` (forms) or `file.info.raw` (external data). Not modified.
- **Derived attributes**: computed from other attributes. A subject attribute is
  prefixed `subject.info`; a file attribute is prefixed `file.info`.
- **Scope**: each rule belongs to a scope that determines which files it runs on.
  Curation order matters — many UDS variables assume earlier scopes already ran,
  and the UDS namespace is curated last.
- **NACC vs MQT attributes**: MQT attributes depend on NACC attributes being
  derived first.

See `docs/index.md` and `docs/operations.md` for the full model. This project is
actively in development and subject to change.
