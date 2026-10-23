# NACCALZP = 7 vs NACCALZD = 1 — Triage Findings

**Scope:** Read-only investigation. No code was modified.
**Date file freeze:** Data Freeze 75 (10 participants with `NACCALZD = 1` and `NACCALZP = 7`).

---

## Summary answer

The bug is real and is in `_create_naccalzp` in
`nacc_attribute_deriver/attributes/derived/modules/uds/form_d1b.py`.

For form versions **V1–V3 (`formver < 4`)**, `NACCALZP` falls through to **7**
whenever the three *contribution-status* fields `probadif` / `possadif` /
`alzdisif` are all blank (or all 0). That fall-through has **no guard** that
checks either of the two conditions the reporter expects:

1. It does **not** check that an AD diagnosis is absent (the "`ALZDIS` is blank"
   / no-AD condition). So it can return 7 even when `NACCALZD = 1`.
2. It does **not** check cognitive status (`DEMENTED` / `MCI` / `IMPNOMCI`) for
   V1–V3; it only checks `normcog != 1`.

`NACCALZD` and `NACCALZP` are derived from **different source fields** that are
not cross-checked:

- `NACCALZD = 1` is driven by the AD *presence* fields `probad` / `possad` /
  `alzdis`.
- `NACCALZP` is driven by the AD *contribution-status* fields `probadif` /
  `possadif` / `alzdisif`.

A record where AD is present (`probad=1`/`possad=1`/`alzdis=1` → `NACCALZD=1`)
but the matching `*if` contribution fields are blank falls straight through to
`NACCALZP = 7`. That is exactly the impossible combination reported.

**Root cause:** the V1–V3 branch of `_create_naccalzp` returns 7
unconditionally when no contribution status is present, with no "AD is absent"
guard and no cognitive-impairment guard.

---

## Evidence

### 1. `_create_naccalzp` — the code that assigns 7

`nacc_attribute_deriver/attributes/derived/modules/uds/form_d1b.py`, method
`_create_naccalzp` (docstring cites `d1structrdd.sas`):

```python
def _create_naccalzp(self) -> int:
    """From d1structrdd.sas.

    Primary, contributing, or non-contributing cause of observed
    cognitive impairment -- Alzheimer's disease (AD)
    """
    if self.normcog == 1:
        return 8

    if self.formver < 4:
        contr_status = self.get_contr_status(["probadif", "possadif", "alzdisif"])
        if contr_status:
            return contr_status

        return 7

    alzdisif = self.uds.get_value("alzdisif", int)
    if alzdisif in [1, 2, 3]:
        return alzdisif

    if self.has_cognitive_impairment():
        return 7

    return 8
```

- **V1–V3 path (`formver < 4`):** after confirming `normcog != 1`, it computes
  `contr_status` from `probadif`/`possadif`/`alzdisif`. `get_contr_status`
  returns the first status among {1, 2, 3} found in those fields, else `None`
  (see below). If no status is found, the method returns **7 unconditionally**.
  There is no check that an AD diagnosis is absent, and no check of
  `DEMENTED`/`MCI`/`IMPNOMCI`.
- **V4 path (`formver >= 4`):** returns `alzdisif` when it is 1/2/3; otherwise
  returns 7 only if `has_cognitive_impairment()` is true, else 8. The V4 path
  therefore *does* gate the 7 on cognitive status — but still does **not**
  guard against an AD diagnosis being present.

`get_contr_status` (same file) confirms the `None` fall-through:

```python
def get_contr_status(self, fields: List[str]) -> Optional[int]:
    all_statuses = self.uds.group_attributes(fields, int)
    for status in ContributionStatus.all():   # [1, 2, 3]
        if any([x == status for x in all_statuses]):
            return status
    return None
```

So blank or 0-valued `*if` fields → `None` → `return 7` in the V1–V3 branch.

### 2. `_create_naccalzd` — the code that assigns 1

`nacc_attribute_deriver/attributes/derived/modules/uds/form_d1b.py`:

```python
def _create_naccalzd(self) -> int:
    if self.normcog == 1:
        return 8

    alzdis = self.uds.get_value("alzdis", int)

    if self.formver < 4:
        probad = self.uds.get_value("probad", int)
        possad = self.uds.get_value("possad", int)

        if any(x == 1 for x in [probad, possad, alzdis]):
            return 1

        if (probad == 0 and possad == 0) or alzdis == 0:
            return 0

    if alzdis is None:
        return 0

    return alzdis
```

- **V1–V3:** `NACCALZD = 1` when **any** of `probad`, `possad`, `alzdis` is 1.
- **V4:** `NACCALZD = alzdis` (0/1), or 0 if `alzdis` blank.

### 3. Field mapping (reporter's variables → codebase fields)

The reporter's expected rule references `DEMENTED`, `MCI`, `IMPNOMCI`, and
`ALZDIS`. In this codebase:

- **DEMENTED** → `self.demented` = `uds.get_value("demented", int)`
  (`form_d1.py`, `UDSFormDxAttribute.__init__`).
- **MCI** → `generate_mci()` (`form_d1.py`): for V4 the raw `mci` field; for
  V1–V3, `1` if any of `mciamem`/`mciaplus`/`mcinon1`/`mcinon2` == 1.
- **IMPNOMCI** → `uds.get_value("impnomci", int)`.
- **ALZDIS** → `uds.get_value("alzdis", int)`; for V1–V3 the AD-presence signal
  is `probad`/`possad`/`alzdis` collectively (same fields that drive
  `NACCALZD`).

The DEMENTED/MCI/IMPNOMCI combination is already bundled as a helper in
`form_d1.py`:

```python
def has_cognitive_impairment(self) -> bool:
    """Check DEMENTED, MCI, and IMPNOMCI for cognitive impairment."""
    impnomci = self.uds.get_value("impnomci", int)
    return self.demented == 1 or self.generate_mci() == 1 or impnomci == 1
```

This is exactly the reporter's `(DEMENTED = 1 OR MCI = 1 OR IMPNOMCI = 1)`
condition — and the V1–V3 branch of `_create_naccalzp` never calls it.

### 4. Why NACCALZD = 1 and NACCALZP = 7 co-occur (the exact gap)

`NACCALZP` (presence of AD) and `NACCALZD`'s contribution status are read from
**disjoint source fields**:

| Concept | NACCALZD source | NACCALZP source |
| --- | --- | --- |
| AD present? | `probad`, `possad`, `alzdis` | — |
| AD contribution status (1/2/3)? | — | `probadif`, `possadif`, `alzdisif` |

A V1–V3 record can have an AD diagnosis recorded (`probad=1`, `possad=1`, or
`alzdis=1`) — giving `NACCALZD = 1` — while the parallel contribution-status
fields `probadif`/`possadif`/`alzdisif` are left blank. In that case:

- `_create_naccalzd` → **1** (AD present).
- `_create_naccalzp` → `get_contr_status(...)` is `None` → **7**.

That produces the impossible pair. The V1–V3 branch returns 7 as a catch-all
for "cognitively impaired, no AD contribution status coded," but never verifies
that AD is actually absent, and never verifies cognitive status.

### 5. Does the code check that ALZDIS is blank before assigning 7?

**No.** In the V1–V3 branch there is no reference to `alzdis`, `probad`, or
`possad` at all before `return 7`. There is also no cognitive-status check. The
only precondition is `normcog != 1`. This missing "AD-absent" guard is the root
cause. (The V4 branch adds a cognitive-status guard via
`has_cognitive_impairment()` but still omits the AD-absent guard.)

### 6. Confirming behavior — the existing test encodes the bug

`tests/attributes/derived/modules/uds/test_form_d1.py`,
`TestUDSFormD1bAttribute.test_create_naccalzp` (~line 198):

```python
attr = UDSFormD1bAttribute(table)
assert attr._create_naccalzp() == 8          # normcog == 1 default

set_attribute(table, form_prefix, "normcog", 0)
attr = UDSFormD1bAttribute(table)
assert attr._create_naccalzp() == 7          # <-- asserts 7 with no *if and no AD/cog guard
```

The `table` fixture sets `probad: 1, normcog: 1, formver: 2`. The second
assertion flips only `normcog` to 0 and expects **7**, even though `probad`
remains `1` — i.e. the fixture already represents a record that would yield
`NACCALZD = 1`. **This test currently asserts the buggy behavior** and will need
to change when the fix lands.

### 7. Curation rules (no change needed here)

`nacc_attribute_deriver/config/curation_rules.csv`:

```
335: uds,naccalzp,file.info.derived.naccalzp,update,FALSE
336: uds,naccalzp,subject.info.derived.longitudinal.naccalzp,list,TRUE
363: uds,naccalzd,file.info.derived.naccalzd,update,FALSE
364: uds,naccalzd,subject.info.derived.longitudinal.naccalzd,list,TRUE
```

Both variables are wired to the `uds` scope and the `_create_naccalzp` /
`_create_naccalzd` functions. The rules are correct; the defect is purely in the
derivation logic, so the CSV needs no change.

---

## Conclusions

1. The impossible `NACCALZD = 1` + `NACCALZP = 7` pair is produced by the
   **V1–V3 (`formver < 4`) branch** of `_create_naccalzp`, which returns 7 as an
   unconditional fall-through whenever `probadif`/`possadif`/`alzdisif` carry no
   contribution status.
2. The branch is missing **both** guards the reporter expects: (a) that AD is
   absent, and (b) that the participant is cognitively impaired
   (`DEMENTED`/`MCI`/`IMPNOMCI`).
3. The absent "AD-absent" guard is the primary root cause of the specific
   reported combination; the missing cognitive-status guard is a related
   secondary gap (it could yield `NACCALZP = 7` for records that are neither
   AD-diagnosed nor cognitively impaired).
4. `has_cognitive_impairment()` already encodes the exact
   DEMENTED/MCI/IMPNOMCI condition and is reused by the V4 branch, so the fix
   can reuse it.

---

## Recommended fix (described, NOT applied)

**Target:** `_create_naccalzp` in
`nacc_attribute_deriver/attributes/derived/modules/uds/form_d1b.py`, the
`formver < 4` branch.

Enforce the reporter's rule so that `7` is only returned when
`(DEMENTED = 1 OR MCI = 1 OR IMPNOMCI = 1)` **and** AD is absent:

- After computing `contr_status` and finding it `None`, before returning 7:
  1. Compute whether AD is present using the same fields `_create_naccalzd`
     uses for V1–V3 — i.e. any of `probad`/`possad`/`alzdis` == 1 (equivalently,
     call `self._create_naccalzd() == 1`). If AD is present, 7 must **not** be
     returned; return the non-impaired code `8` (or whatever the SAS
     `d1structrdd.sas` specifies for "AD present but no contribution status").
  2. Gate the `7` on `self.has_cognitive_impairment()` for V1–V3, mirroring the
     V4 branch. If not cognitively impaired, return `8`.

   Sketch (illustrative, confirm the fall-through value against `d1structrdd.sas`):

   ```python
   if self.formver < 4:
       contr_status = self.get_contr_status(["probadif", "possadif", "alzdisif"])
       if contr_status:
           return contr_status
       if self._create_naccalzd() == 1:      # AD present -> cannot be 7
           return 8
       if self.has_cognitive_impairment():    # DEMENTED/MCI/IMPNOMCI
           return 7
       return 8
   ```

- **Also review the V4 branch:** it already gates 7 on
  `has_cognitive_impairment()` but does **not** guard against AD being present.
  Confirm whether a V4 record can have `NACCALZD = 1` (`alzdis = 1`) while
  `alzdisif` is blank; if so, the same "AD-absent" guard should be added there
  to prevent the same inconsistency in V4 data.

**Before finalizing the fall-through return value (7 vs 8 vs another code),
cross-check against the authoritative `d1structrdd.sas` logic** cited in the
docstring, since the correct code for "cognitively impaired, no AD contribution
coded, AD present" should match NACC's canonical SAS derivation.

### Tests that must be updated

- `tests/attributes/derived/modules/uds/test_form_d1.py` →
  `TestUDSFormD1bAttribute.test_create_naccalzp` (~line 198). The assertion
  `assert attr._create_naccalzp() == 7` after flipping only `normcog` to 0 is
  made against a fixture where `probad = 1` (AD present). Under the fix this
  should no longer be 7. The test needs restructuring to:
  - a case with an AD diagnosis present (`probad`/`possad`/`alzdis` = 1) and no
    `*if` status → expect the AD-present fall-through (not 7);
  - a case with no AD and cognitive impairment set
    (`demented`/`mci*`/`impnomci`) → expect 7;
  - a case with no AD and no cognitive impairment → expect 8;
  - keep the existing cases asserting the explicit contribution statuses (1/2/3).

**Verification after any fix (per workspace steering):** run the project quality
gate — `pants_fix`, then `pants_check` and `pants_test` scoped to the changed
targets — e.g. tests at
`tests/attributes/derived/modules/uds/test_form_d1.py` — and confirm they pass.
No fix has been applied here; this is a triage report only.

---

## Addendum — SAS source cross-check (correction to the framing above)

After the initial report, the authoritative SAS source
`derived-variable-scripts/sas/d1structrdd.sas` (sibling repo) was inspected
directly. This changes the characterization of the defect.

### The canonical SAS produces the same combination

`d1structrdd.sas` lines 390–396 derive NACCALZP as:

```sas
naccalzp = .;
if normcog = 1 then naccalzp = 8;
else if normcog ^= 1 then do;
 if probadif = 1 or possadif = 1 or alzdisif = 1 then naccalzp = 1;
 else if probadif = 2 or possadif = 2 or alzdisif = 2 then naccalzp = 2;
 else if probadif = 3 or possadif = 3 or alzdisif = 3 then naccalzp = 3;
 else naccalzp = 7;      /* unconditional fall-through */
end;
```

This is an unconditional fall-through to 7 when `normcog ^= 1` and none of the
`*if` fields is 1/2/3. It has **no AD-absent guard and no DEMENTED/MCI/IMPNOMCI
guard** — identical to the Python `_create_naccalzp` V1–V3 branch. NACCALZD is
derived at lines 385–388 from `probad`/`possad`/`alzdis`, disjoint from the
`*if` fields. So `NACCALZD = 1` + `NACCALZP = 7` is reproducible in the
canonical SAS itself; the Python is a faithful port, not a deviation from spec.

### The `%recode4g` preprocessing does not prevent it

The two recode calls preceding the block (lines 274–275) expand to:

```sas
if PROBAD not in (1) then do; if PROBADIF not in (-4,1) then PROBADIF = 7; end;
if POSSAD not in (1) then do; if POSSADIF not in (-4,1) then POSSADIF = 7; end;
```

These fire only when AD is **absent** (`PROBAD ^= 1`), force `PROBADIF`/
`POSSADIF` to 7, and leave `ALZDISIF` untouched. They do not guard the
AD-present case, so they do not prevent the reported pair. `naccalzp` is
assigned only once in the SAS (no later override).

### Consequence for the fix

Applying the AD-absent + cognitive-impairment guard makes the Python port
**intentionally diverge** from the current canonical `d1structrdd.sas`. This is
a deliberate decision (approved by the repo owner) to enforce the reporter's
rule — that NACCALZP = 7 requires `(DEMENTED = 1 OR MCI = 1 OR IMPNOMCI = 1)`
AND AD absent — ahead of the SAS being amended. The SAS source
(`derived-variable-scripts`) should be updated to match so the two derivations
stay in sync; until then the port is knowingly ahead of the SAS.

### Fix applied (this branch `fix/naccalzp-7-coding`)

`_create_naccalzp`, V1–V3 branch: before the fall-through `return 7`, return 8
when AD is present (`_create_naccalzd() == 1`) or when the participant is not
cognitively impaired (`not has_cognitive_impairment()`). This mirrors the gate
already present in the V4 branch and adds the AD-absent guard. The V4 branch's
missing AD-absent guard is noted but left unchanged pending confirmation that a
V4 record can present `alzdis = 1` with a blank `alzdisif`.
