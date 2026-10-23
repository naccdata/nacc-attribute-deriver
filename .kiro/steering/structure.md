# Project Structure

Source root is the repo root. Each directory that holds Python has a `BUILD`
file; add/update them with `pants_tailor` when you add files.

```
nacc_attribute_deriver/          # the library package
  attribute_deriver.py           # AttributeDeriver entry point; loads curation rules per scope
  symbol_table.py                # SymbolTable: dot-notation dict over Flywheel metadata
  attributes/                    # the plugin registry of attribute "_create_" functions
    collection/                  # AttributeCollection base + metaclass registry
      attribute_collection.py    # AttributeCollection, AttributeExpression, registry metaclass
      uds_collection.py          # UDS form attributes
      missingness_collection.py  # missingness attributes
    derived/                     # derived attributes grouped by domain
      genetics/                  # ncrad_apoe, ncrad_biomarker, ncrad_biosample, niagads
      imaging/                   # mp, mp_mri_summary, scan
      modules/                   # per-form modules (b1a, bds, ...)
  config/                        # curation rules + lookup data (CSV), shipped in the wheel
    curation_rules.csv           # scope,function,location,operation,dated rows
    *.csv                        # missingness tables, drug ids, matrices, etc.
  schema/                        # pydantic schema definitions
  utils/                         # constants, errors, helpers
tests/                           # mirrors the package layout
  conftest.py                    # shared fixtures (prefixes, uds_table, set_attribute)
  attributes/{collection,derived,missingness,mqt,namespace}/
docs/                            # index.md (concepts), operations.md (operation semantics)
```

## Conventions

- **Attribute plugins**: each derived variable is a method named
  `_create_<name>` (or `_missingness_<name>`) on an `AttributeCollection`
  subclass. Subclassing registers the collection automatically via the
  `AttributeCollectionRegistry` metaclass — no manual registration. Function
  names must be unique across all collections (duplicates raise
  `AttributeDeriverError`).
- **Wiring a new variable**:
  1. Add the `_create_<name>` method to the right collection under `attributes/`.
     Assume `file.info.*` and `subject.info` are already populated.
  2. Add the rule row(s) to `config/curation_rules.csv` (one `function` often
     maps to several `location`/`operation` pairs, e.g. earliest and latest).
  3. Add a test under the mirrored path in `tests/`, typically one test function
     per attribute.
- **Operations**: assignment semantics (update, list, sortedlist, set, initial,
  latest, min, max) are documented in `docs/operations.md`. `dated` wraps the
  value in a `DateTaggedValue` (`{"date": ..., "value": ...}`).
- **Types & docstrings**: fully type-hinted; docstrings formatted by
  docformatter. Keep imports sorted (ruff `I`).
- **SymbolTable access**: use dot-notation string keys; the table is a dict
  subclass, so prefer the fixtures in `tests/conftest.py` when writing tests.
