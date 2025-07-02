# Changelog

Documentation of release versions of `nacc-attribute-deriver`

## Working (1.5.0.dev)

* Adds rest of NP derived variables
* Adds rest of UDS derived variables:
    * Form header
        * Here some NACC derived variables compute the same thing but apply to a different operation, so curation rule may point to a different derived variable's function
            * NACVNUM - uses NACCAVST
            * NACCFDAYS - uses NACCDAYS
        * MQT's `longitudinal._create_total_uds_visits` removed and curation rule updated to use NACCAVST directly
    * A1, A2, A3, A4, and A5
        * Accounts for some forms being optional
        * For A4, adds MEDS scope
        * **NACCFAM (A3) and and MEDS V1 (A4) are still not working properly, on hold for now**
    * B1, B6, B8, and B9
    * C1/C2
        * MQT's `demographics._create_uds_education_level` moved to `form_a1` and renamed `_create_educ` as it needs to be used for variables in this form as well
    * D1 **except** NACCMCII (D1)
        * **NACCMCII is still not working properly, on hold for now**\
* Adds CLS derived variables
* Adds NACCNE4S and fixes NACCAPOE to account for ADC and ADGC genotypes not being the same
* Refactors how dated values are handled - adds `dated` configuration to curation rules to be handled at curation rule level and removes redundant `_create` functions
    * Updates longtitudinal variables to be stored as list of `DateTaggedValue`s - curation rules updated
* Refactors working/temporary variables to be written under `subject.info.working`, and updates to use kebab-case
* Updates how grabbing longitudinal values is done and and added support for grabbing dated cross-sectional and longitudinal values, related to the above refactors

## 1.4.1

* Adds ability to derive type returned by a curation rule with tool to create table of rule types.
* Adds enforcement of expected types when grabbing variables from the raw data

## 1.4.0

* Add check for affiliated participants
* Adds more NP variables
* Refactors NP functionality - added `NPMapper` (mapping functions) and `NPFormWideEvaluator` (for variables like NACCBRNN that require looking at the entire NP form)
* Refactors to consoildate redundant cross-sectional derived variables so UDS doesn't have to redefine them, namely for NP and genetics data
* Fix `wmh` to not be required (for `SCANMRIScope.MRI_SBM`)

## 1.3.0

* Adds `historic_apoe` rule to support historical APOE values from sources other than NCRAD
* Refactors the use of `subject.info.derived` for UDS NACC* variables - splits between longitudinal and cross-sectional variables, then updates the MQT rules to handle the longitudinal rules as sets
    * Adds functions to `SubjectDerivedNamespace` grab cross-sectional and longitudinal values
        * Longitudinal keeps track of sets, so value can be different across forms
        * Cross-sectional is globally updated - curator gear will handle back-propogation
    * Fixes various bugs related to this issue
    * Other attributes that use subject.info should be relooked at as well but for the most part are left alone for now
* Refactors how scopes are handled, particularly for SCAN
* Moves `uds_namespace` to `attributes/base`
* Updates to normalize the form version, e.g. `formver: 3.2` is UDS 3
* Updates to not allow NACC* derived variables to be null
* Updates `_create_uds_primary_language` to always return None on follow-up forms
* Updates `AttributeExpression.apply` to throw error instead of only reporting a warning, also fixes some mis-uses of `MissingRequiredError`
* Fixes `naccint` to calculate interval in months instead of days
* Fixes `set` and `list` operations to set attribute to empty list instead of not setting it
* Fixes `latest` and `initial` operations to update if the dates are the same
* Removes redundant code
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
