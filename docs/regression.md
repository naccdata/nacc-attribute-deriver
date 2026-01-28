# V4 Notes

## V4 Typing

Currently, V4 data is saved in FW metadata as strings. This causes issues in the data model validation, which explicitly looks at the source type. As an interim solution, the current code enforces typing on everything defined in the `*missingness.csv` files, since those are the "rules" that get curated and already have typing attached.

**THAT BEING SAID**, this is not comprehensive, and only includes variables explicitly needed for QAF generation at the moment. As such, there still may be numerical/integer values in `file.info.resolved` that are _still strings_ since they are not explicitly handled here. Ideally this typing issue gets resolved further upstream (especially because doing this significnatly increases the runtime), but for now this is a brute-force solution to get things going.

# Regression

The following are known and notable issues and inconsistencies in how the legacy code derived variables and what we are changing it to going forward starting with the new system and V4. You may also find `# REGRESSION` comments in the code for more context.

## Generally

* For missingness, there are a lot of inconsistencies on when things are set to -4 based on relevance to the form version. The legacy had to hardcode all of these, and it seems several slipped through the cracks/accidentally got set to something anyways. Going forward, we are using `config/uds_ded_matrix.csv` to explicitly set something to the missingness value (-4/-4.4/blank) if it is not applicable to the version.
	* In the matrix, 1 = collected in that version, 2 = collected only at IVP and automatically brought across, 0/blank = not applicable 

## Form A3

* `NACCFAM`, `NACCMOM`, and `NACCDAD` (all cross-sectional) followed a rule that if any visit ever set it to 1, it would stay 1, but 0 and 9 could flip/flop. Going forward, we instead allow it to flip-flop between 0 and 1, but 9 will never override the other two.
	* On that note, the legacy code for these variables is particularly incomprehensible. The current code doesn't really help, as it was written to reproduce/interpret the legacy output before applying the above change. But at least it's in Python now and not SAS :)

## Form A4

### V1

In V1, the A4 form was very different and all medications were written in by hand. The legacy code did _something_ to translate these to drug IDs (e.g. d00000 codes), but is extremely unclear how it was doing that mapping, and the general consensus was that it was quite unreliable anyways.

Because we were unable to identify the mechanism used for that mapping, we somewhat rather brute-forced its migration it to the current codebase. Using what seemed like a text file containing all the write-in values ever submitted for this version of the form, we had ClaudeAI "spellcheck" the write-ins so that they could be more directly mapped to the UDSMEDS table (now dumped to `config/UDSMEDS.csv`) to get the respective drug IDs, and then the results were stored in `config/normalized_drug_ids_v1.csv`.

This file is used as to do the mapping instead. It originally did not match the legacy mapping, so we compared the computed results between the new and legacy QAFs to update the mapping to whatever the legacy code did before. Since this is only a V1 issue, and we have long since stopped collectin V1, we settled on basically having every possible value hardcoded.

### MEDS vs Drugs List

In the legacy system there were two tables related to A4:

* FRMCA4G, which records whether the participant has any medications for a visit and what indicates that a corresponding MEDS file should exist in Flywheel
* FRMCA4D, which supplies the actual list of drugs for a visit.

Unfortunately, it seems that there are a handful of cases where for a given visit there was only data in one table but not the other. The legacy code would directly query FRMCA4D (drugs list) to calculate most of the derived variables related to A4, as well as set/adjust the `ANYMEDS` variable. The new system, however, relies on the existence of the MEDS file for the same derived/missingness variables.

As such, for these handful of visits with inconsistent data, their derived/missingness values are equally inconsistent between the old and new derivations (e.g. new system cannot find any drugs so sets all variables correspondingly, while the legacy system was able to find drugs and sets it correspondingly, or vice versa). Again, at this point we have decided for this to be an acceptable discrepancy, since such inconsistencies should not have allowed a packet to be finalized to begin with.

## Form B9

* `NACCBEHF`, `NACCBEFX`, `NACCCGFX`, `NACCCOGF`, and `NACCMOTF` are all supposed to be cross-sectional, but the legacy code was treating them as longitudinal values (e.g. they have different values across visits). This will be fixed to enforce the intended cross-sectional nature going forward.

## Form D1a

* `NACCMCII`: Legacy code seems to not have been correctly considering the 8 condition, especially in regards to the initial visit - for example, even if there was MCI at the initial visit, it would NOT set it to 8. I'm still investigating exactly what it's doing wrong just for regression testing, but it will be fixed going forward.
