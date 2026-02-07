# Changelog

Documentation of release versions of `nacc-attribute-deriver`

## 2.1.2 (unreleased)

* Update MEDS and A4 form to date drugs based on UDS visitdates (which must be unique) since `frmdatea4` is not reliable and may conflict with another visit
* Fixes FTLD `ftdratio` if set as 88 to 88.88

## 2.1.1

* Adds a more specific V1 drug mapping based on raw data and legacy output
* Fixes bug where we were assuming longitudinal data was properly sorted, but it may not be in some cases (namely for the drugs list)

## 2.1.0

* Adds logic to correlate standalone forms (COVID, CLS) to the closest UDS visit - assumes all UDS visits have been curated already
    * Original `visitdate` moved to `c19visitdate` and `clsvisitdate`, respectively
* Updates to standardize all UDS `FRMDATEX` variables to `YYYY-MM-DD` format
* Updates to enforce ranges for several variables
* Updates NP `NACCBRNN` to always return 9 for missing/unknown (previously mix of 8 and 9 depending on version)
* Updates COVID `C19TxYR` variables to fix 88 to 8888 and 99 to 9999
* Updates LBD to handle the 0 prev code for `LBSPSYM` and `SCCOFRST` 
* Updates the V1 drug mappings to align further with legacy results
* Allows affiliate status to change
    * Also removes `justification` column as it isn't needed
* Fixes MQT's `SEX MAPPING` value 9 from "Don't know" to "Unknown"

## 2.0.1

* Upgrade to Python 3.12 and Pants 2.29.0

## 2.0.0

Significant updates and refactorings to support:

* rest of derived variables
* missingness logic

#### RCs:

* rc2: Adds V4 header variables
* rc3:
    * Updates B1a-related variables to not throw error when missing - data currently not available in FW
    * Updates to handle NP form date being `npformdate` instead of `visitdate` in the new system
    * Updates to not throw error if missing UDS in cross-module calculations, as it may have just been an MDS/BDS participant
    * Updates to support `yyyy/mm/dd` and `mm-dd-yyyy` date formats
* rc4:
    * Updates to handle float NP `formver`
* rc5
    * Fix various typing/range issues encountered when running ETL
* rc6/final release of 2.0.0
    * Adds BDS scope, although no actual BDS rules, and combines COVID scopes to handle how its being imported into Flywheel
    * Updates to support the same headers across all form scopes (missingness)
    * Makes -4.0 the default for floats except in NP which stays at -4.4
        * Removes `missingness_b4.py` which forced this for B4; should be done automatically now
    * Fixes known discrepancies
        * Majorly affects A5D2, which updates legacy behavior to rely on gates (previously this logic was skipped using the `skip_gate_on_legacy` argument, which is now removed)
    * Makes `pentagon` an honorary v1 variable
    * Supports missingness for header variables across all form scopes

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
