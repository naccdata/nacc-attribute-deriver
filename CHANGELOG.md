# Changelog

Documentation of release versions of `nacc-attribute-deriver`

## 1.2.3

* Refactors how scopes are handled, particularly for SCAN
* Moves `uds_namespace` to `attributes/base`
* Updates to normalize the form version, e.g. `formver: 3.2` is UDS 3
* Fixes `naccint` to calculate interval in months instead of days
* Fixes issue with UDS Form D1 cognitive variables where the default changes (e.g. `normcog != 1` vs `normcog == 1`). Affected variables:
    * `naccalzp`
    * `naccetpr`
* Fixes else/if condition on `naccppa` and removes checking of subject default (not applicable here)
* Fixes `set` and `list` operations to set attribute to empty list instead of not setting it
* Fixes `latest` and `initial` operations to update if the dates are the same
* Removes regression testing related code - separating out
* Removes the `count` operation

## 1.2.2

* Adds ability for UDS NACC derived variables to account for follow-up forms
    * If a raw value is not specified, checks the subject-level derived value as well before setting to the missing/null case
    * Adds rules to the config for UDS NACC derived variables to write to `subject.info.derived`
    * Updates the following 9 variables to support this:
        * Form A1: `naccnihr`
        * Form D1: `naccalzp`, `nacclbde`, `nacclbdp`, `naccudsd`, `naccetpr`, `naccppa`, `naccbvft`, `nacclbds`
* Updates `uds_primary_language` rule to return `None` (handles case where subsequent visits do not re-specify the value)
* Fixes `total_uds_visits` rule
* Fixes missing import for `mds` and `milestone` NACC rules

## 1.2.1

* Allows for `subject.info.derived.np_death_age` to be unset when verifying existence of NP data

## 1.2.0

* Includes MQT V2.1 attributes over NP data

## 1.1.0

* Refines MQT V2 variables, namely making sure code aligns with the FW data model

## 1.0.0

* Initial version, handles up to MQT V2
