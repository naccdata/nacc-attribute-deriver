# Changelog

Documentation of release versions of `nacc-attribute-deriver`

## 2.0.0

Significant updates and refactorings to support:

* rest of derived variables
* missingness logic

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

* Adds ability to derive type returned by a curation rule with tool to create table of rule types - [#43](https://github.com/naccdata/nacc-attribute-deriver/pull/43)
* Adds enforcement of expected types when grabbing variables from the raw data - [#44](https://github.com/naccdata/nacc-attribute-deriver/pull/44)

## 1.4.0

* Add check for affiliated participants - [#39](https://github.com/naccdata/nacc-attribute-deriver/pull/39)
* Adds more NP variables - [#40](https://github.com/naccdata/nacc-attribute-deriver/pull/40), [#42](https://github.com/naccdata/nacc-attribute-deriver/pull/42)
    * Refactors NP functionality - added `NPMapper` (mapping functions) and `NPFormWideEvaluator` (for variables like NACCBRNN that require looking at the entire NP form)
    * Refactors to consoildate redundant cross-sectional derived variables so UDS doesn't have to redefine them, namely for NP and genetics data
* Fix `wmh` to not be required (for `SCANMRIScope.MRI_SBM`) - [#41](https://github.com/naccdata/nacc-attribute-deriver/pull/41)

## 1.3.0

Most of these changes are associated with aggregate PR [#26](https://github.com/naccdata/nacc-attribute-deriver/pull/26)

* Adds `historic_apoe` rule to support historical APOE values from sources other than NCRAD - [#27](https://github.com/naccdata/nacc-attribute-deriver/pull/27)
* Refactors the use of `subject.info.derived` for UDS NACC* variables - splits between longitudinal and cross-sectional variables, then updates the MQT rules to handle the longitudinal rules as sets
    * Adds functions to `SubjectDerivedNamespace` grab cross-sectional and longitudinal values
        * Longitudinal keeps track of sets, so value can be different across forms
        * Cross-sectional is globally updated - curator gear will handle back-propogation
    * Fixes various bugs related to this issue
    * Other attributes that use subject.info should be relooked at as well but for the most part are left alone for now
* Refactors how scopes are handled, particularly for SCAN - [#22](https://github.com/naccdata/nacc-attribute-deriver/pull/22)
* Moves `uds_namespace` to `attributes/base`
* Updates to normalize the form version, e.g. `formver: 3.2` is UDS 3
* Updates to not allow NACC* derived variables to be null
* Updates `_create_uds_primary_language` to always return None on follow-up forms - [#30](https://github.com/naccdata/nacc-attribute-deriver/pull/30)
* Updates `AttributeExpression.apply` to throw error instead of only reporting a warning, also fixes some mis-uses of `MissingRequiredError` - [#31](https://github.com/naccdata/nacc-attribute-deriver/pull/31)
* Fixes `naccint` to calculate interval in months instead of days - [#24](https://github.com/naccdata/nacc-attribute-deriver/pull/24)
* Fixes operations - [#23](https://github.com/naccdata/nacc-attribute-deriver/pull/23)
    * Fixes `set` and `list` operations to set attribute to empty list instead of not setting it
    * Fixes `latest` and `initial` operations to update if the dates are the same
    * Removes the `count` operation
* Removes regression testing related code - separating out - [#22](https://github.com/naccdata/nacc-attribute-deriver/pull/22) 
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
