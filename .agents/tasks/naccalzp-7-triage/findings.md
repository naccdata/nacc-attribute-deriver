# NACCALZP = 7 with NACCALZD = 1 — Triage Findings

## Report

Data freeze 75 has 10 participants with `NACCALZD = 1` (Q12, presumptive AD
diagnosis) and `NACCALZP = 7` (Q12a, 7 = cognitively impaired but not AD
diagnosis). Expected rule: `NACCALZP = 7` only when `DEMENTED = 1`, `MCI = 1`,
or `IMPNOMCI = 1`, and `ALZDIS` is blank.

The question numbers place this in UDS V4. In the RDD, `NACCALZD`/`NACCALZP`
are question 11/11a in V3 and 12/12a in V4. The field names don't tell the
versions apart, because `ALZDIS` and `ALZDISIF` exist in both V3 and V4.

## Root cause

`_create_naccalzp` in
`nacc_attribute_deriver/attributes/derived/modules/uds/form_d1b.py`, V4 branch.

Commit `049068f` (2026-09-25, released in v2.5.1) added
`if self.has_cognitive_impairment(): return 7` to the V4 branch, so impaired
participants without an AD diagnosis would get 7 instead of 8. It didn't check
that AD was absent. A V4 record with `ALZDIS = 1` and `ALZDISIF` blank
therefore got `NACCALZD = 1` with `NACCALZP = 7`. Before that commit the V4
branch never returned 7.

It hasn't been confirmed that freeze 75 was derived with v2.5.1 or later.

## Specification (UDS RDD, Version 4, April 2026)

- `NACCALZP` allowable codes: 1 Primary, 2 Contributing, 3 Non-contributing,
  7 Cognitively impaired but not AD diagnosis, 8 Diagnosis of normal cognition.
  There is no missing code.
- "Participants who are cognitively impaired without an etiologic diagnosis of
  AD have NACCALZP = 7. Unimpaired participants ... have NACCALZP = 8."
- `NACCALZD = 0` is "cognitive impairment and no Alzheimer's disease etiologic
  diagnosis", so `NACCALZP = 7` corresponds to an impaired participant with
  `NACCALZD = 0`.
- `ALZDIS` and `ALZDISIF` are not documented in the RDD.

## V4 form rules (`nacc-draft-schemas/.../UDS/4.0`, I, F and I4 identical)

- `ALZDIS`: nullable, allowed 0 or 1.
- `ALZDISIF`: nullable, allowed 1, 2 or 3, and must be blank when `ALZDIS` is
  not 1.
- Nothing requires `ALZDISIF` when `ALZDIS = 1`, so AD diagnosed with
  `ALZDISIF` blank passes QC.

`ALZDIS` and `ALZDISIF` are both in the V4 form schema and the freeze data
model (`nacc-flywheel-metadata`).

## Fix

V4 branch only. The V1–V3 branch follows `d1structrdd.sas` and is unchanged.

- `ALZDISIF` in 1, 2 or 3 → that value.
- Otherwise 7 when the participant is cognitively impaired and
  `NACCALZD != 1`.
- Otherwise 8.

`ALZDIS = 0` and blank `ALZDIS` both give 7 for impaired participants. This
follows the RDD definition of 7. Under the form rules `ALZDISIF` is blank in
both cases.

## Open question

AD diagnosed (`ALZDIS = 1`) with `ALZDISIF` blank has no valid code. 7
contradicts `NACCALZD = 1`, 8 means normal cognition, and 1–3 would record a
role the clinician didn't give. The code returns 8 with a TODO until this is
decided. Options:

- Choose one of the allowable codes and update the RDD text to cover the case.
- Add a V4 QC rule requiring `ALZDISIF` when `ALZDIS = 1`, which would stop new
  records reaching this state. Existing records would still need a value.

## Related, not changed

- The V1–V3 branch also returns 7 when an AD diagnosis is present and the `*IF`
  fields are blank. This matches `d1structrdd.sas`, but under the RDD
  definition it is also inconsistent. No V3 QC rules are available to show
  whether V3 records reach this state.
- `_create_nacclbdp` has the same V4 pattern: it returns 7 for impaired
  participants without checking that LBD is absent.
