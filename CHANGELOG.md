# Changelog

Documentation of release versions of `nacc-attribute-deriver`

## 2.0.0 (not yet released)

Most of these changes are associated with aggregate PR [#66](https://github.com/naccdata/nacc-attribute-deriver/pull/66)

* Adds rest of UDS derived variables:
    * [#56](https://github.com/naccdata/nacc-attribute-deriver/pull/56) Form header
        * Here some NACC derived variables compute the same thing but apply to a different operation, so curation rule may point to a different derived variable's function
            * NACVNUM - uses NACCAVST
            * NACCFDAYS - uses NACCDAYS
        * Also adds NACCID
    * [#46](https://github.com/naccdata/nacc-attribute-deriver/pull/47), [#49](https://github.com/naccdata/nacc-attribute-deriver/pull/49) A1, A2, A3, A4, and A5
        * Accounts for some forms being optional
        * [#47](https://github.com/naccdata/nacc-attribute-deriver/pull/47), [#60](https://github.com/naccdata/nacc-attribute-deriver/pull/60) For A4, adds MEDS scope, and `config/normalized_drug_ids.csv` to map V1 write-ins
        * **NACCFAM (A3), on hold for now**
    * [#52](https://github.com/naccdata/nacc-attribute-deriver/pull/52), [#54](https://github.com/naccdata/nacc-attribute-deriver/pull/54) B1, B6, B8, and B9
    * [#51](https://github.com/naccdata/nacc-attribute-deriver/pull/51) C1/C2
        * MQT's `demographics._create_uds_education_level` moved to `form_a1` and renamed `_create_educ` as it needs to be used for variables in this form as well
    * [#55](https://github.com/naccdata/nacc-attribute-deriver/pull/55) D1
    * [#60](https://github.com/naccdata/nacc-attribute-deriver/pull/60) Adds FTLD/LBD scope and variables (just checks existence)
* [#57](https://github.com/naccdata/nacc-attribute-deriver/pull/57) Adds CLS derived variables
* [#58](https://github.com/naccdata/nacc-attribute-deriver/pull/58) Adds MILESTONE derived variables
    * Many of these are cross-form, particularly with UDS A1
* [#46](https://github.com/naccdata/nacc-attribute-deriver/pull/47) Adds rest of NP derived variables
* Adds `MissingFormAttributes` which sets a default values for certain non-UDS NACC derived variables when the corresponding source file does not exist for that subject
* Adds/fixes genetics derived variables
    * [#59](https://github.com/naccdata/nacc-attribute-deriver/pull/59) Adds NIAGADS accession number derived variables
    * Adds NACCNE4S
    * Fixes NACCAPOE to account for ADC and ADGC genotypes not being the same
    * [#67](https://github.com/naccdata/nacc-attribute-deriver/pull/67) Adds NACCNCRD
* [#68](https://github.com/naccdata/nacc-attribute-deriver/pull/68) Adds CSF derived variables
* [#68](https://github.com/naccdata/nacc-attribute-deriver/pull/68), [#70](https://github.com/naccdata/nacc-attribute-deriver/pull/70) Adds Mixed Protocol (MP) derived variables
    * Adds `DatedSetOperation` to support dated sets required for these variables (since curating across sessions)
* [#50](https://github.com/naccdata/nacc-attribute-deriver/pull/50) Refactors how dated values are handled - adds `dated` configuration to curation rules to be handled at curation rule level
    * Updates longtitudinal variables to be stored as list of `DateTaggedValue`s - curation rules updated
* Refactors working/temporary variables to be written under `subject.info.working`, and updates to use kebab-case
* Refactors testing to use a `base_uds_table` fixture
* Replaces `datetime_from_form_date` with just `date_from_form_date` since we don't use time here - removes confusion of converting every time
* Updates how grabbing longitudinal values is done and and added support for grabbing dated cross-sectional and longitudinal values, related to the above refactors
* Removes redundant `_create rules`
    * `cognitive._create_etpr` - use NACCETPR
    * `cognitive._create_cognitive_status` - use NACCUDSD
    * `demographics._create_age_at_death` - use NACCDAGE
    * `demographics._np_available` - use NACCAUTP (check not 0 or 8)
    * `demographics._create_uds_age` - use NACCAGE
    * `longitudinal._create_total_uds_visits` - use NACCAVST
* Minor optimization tweaks

## 1.4.3

Under PR [#65](https://github.com/naccdata/nacc-attribute-deriver/pull/65) 

* Fix mutability bug caused by empty nested tables

## 1.4.2

Under PR [#64](https://github.com/naccdata/nacc-attribute-deriver/pull/64)

* Allows attribute deriver to expose curation rules by scope
* Account for all kinds of invalid string text
* Defines `pop` for SymbolTable (done more for optimization the attribute-curator gear)
* Fixes `ngdsexome` typo to `ngdsexom`

## 1.4.1

* [#43](https://github.com/naccdata/nacc-attribute-deriver/pull/43) Adds ability to derive type returned by a curation rule with tool to create table of rule types.
* [#44](https://github.com/naccdata/nacc-attribute-deriver/pull/44) Adds enforcement of expected types when grabbing variables from the raw data

## 1.4.0

* [#39](https://github.com/naccdata/nacc-attribute-deriver/pull/39) Add check for affiliated participants
* [#40](https://github.com/naccdata/nacc-attribute-deriver/pull/40), [#42](https://github.com/naccdata/nacc-attribute-deriver/pull/42) Adds more NP variables
    * Refactors NP functionality - added `NPMapper` (mapping functions) and `NPFormWideEvaluator` (for variables like NACCBRNN that require looking at the entire NP form)
    * Refactors to consoildate redundant cross-sectional derived variables so UDS doesn't have to redefine them, namely for NP and genetics data
* [#41](https://github.com/naccdata/nacc-attribute-deriver/pull/41) Fix `wmh` to not be required (for `SCANMRIScope.MRI_SBM`)

## 1.3.0

Most of these changes are associated with aggregate PR [#26](https://github.com/naccdata/nacc-attribute-deriver/pull/26)

* [#27](https://github.com/naccdata/nacc-attribute-deriver/pull/27) Adds `historic_apoe` rule to support historical APOE values from sources other than NCRAD
* Refactors the use of `subject.info.derived` for UDS NACC* variables - splits between longitudinal and cross-sectional variables, then updates the MQT rules to handle the longitudinal rules as sets
    * Adds functions to `SubjectDerivedNamespace` grab cross-sectional and longitudinal values
        * Longitudinal keeps track of sets, so value can be different across forms
        * Cross-sectional is globally updated - curator gear will handle back-propogation
    * Fixes various bugs related to this issue
    * Other attributes that use subject.info should be relooked at as well but for the most part are left alone for now
* [#22](https://github.com/naccdata/nacc-attribute-deriver/pull/22) Refactors how scopes are handled, particularly for SCAN
* Moves `uds_namespace` to `attributes/base`
* Updates to normalize the form version, e.g. `formver: 3.2` is UDS 3
* Updates to not allow NACC* derived variables to be null
* [#30](https://github.com/naccdata/nacc-attribute-deriver/pull/30) Updates `_create_uds_primary_language` to always return None on follow-up forms
* [#31](https://github.com/naccdata/nacc-attribute-deriver/pull/31) Updates `AttributeExpression.apply` to throw error instead of only reporting a warning, also fixes some mis-uses of `MissingRequiredError`
* [#24](https://github.com/naccdata/nacc-attribute-deriver/pull/24) Fixes `naccint` to calculate interval in months instead of days
* [#23](https://github.com/naccdata/nacc-attribute-deriver/pull/23) Fixes operatoins
    * Fixes `set` and `list` operations to set attribute to empty list instead of not setting it
    * Fixes `latest` and `initial` operations to update if the dates are the same
    * Removes the `count` operation
* [#22](https://github.com/naccdata/nacc-attribute-deriver/pull/22) Removes regression testing related code - separating out
* Removes redundant code

## 1.2.2

Under PR [#20](https://github.com/naccdata/nacc-attribute-deriver/pull/20)

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
