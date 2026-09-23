# Requirements Coverage Audit

## Scope and method

Audited `docs/REQUIREMENTS.md` against its navigation index, requirement/form/annex records, and the existing printed-page source references. The audit did not re-extract the manual. The manual was reopened only at printed page 11 to check the apparent Chapter 6 numbering irregularity.

Audit date: 2026-09-23

## Coverage result

| Area | Indexed/expected | Verified representation | Result |
| --- | ---: | ---: | --- |
| Navigation index | 85 source-area rows | 85 marked VERIFIED | Complete |
| Chapters 1–11 | 11 chapters | 276 atomic requirement records | Complete |
| Indexed chapter subsections | 70 subsection rows | All represented under their chapter records and marked VERIFIED | Complete |
| Annex 1 | Income-code classification | 17 code/title/meaning records | Complete |
| Annex 2 | Expense-code classification | 45 code/title/meaning records | Complete |
| Annex 3 | Forms 1–40 | 40 form-index rows and 40 detailed form records | Complete |
| Annex 4 | Practical accounting scenarios | 12 numbered scenarios plus completed record/report samples | Complete |

Every atomic chapter requirement has a printed-page source reference and VERIFIED status. Every detailed Form 1–40 record and every numbered Annex 4 scenario has a source page/status field marked VERIFIED. No `TO_EXTRACT` status remains in `docs/REQUIREMENTS.md`.

## Consistency checks

| Check | Result |
| --- | --- |
| Duplicate atomic chapter requirement IDs | None found |
| Duplicate form index IDs | None found |
| Form numbering | Continuous from `SAM-F01` through `SAM-F40`, with matching `SAM-FORM-01` through `SAM-FORM-40` details |
| Annex 1/2 code records | 62 records total; no duplicate extracted code IDs found |
| Annex 4 scenario numbering | Continuous from `SAM-ANN-04-001` through `SAM-ANN-04-012` |
| Missing source page/status on atomic requirements, detailed forms, or numbered Annex 4 scenarios | None found |

## Fixed documentation errors

- Updated all 85 navigation-index source-area statuses to VERIFIED. The underlying extractions were already present; the index had retained stale `TO_EXTRACT` values.
- Updated the index description so it no longer states that indexed content has not been extracted.

## Preserved source and structural inconsistencies

These items are deliberately not corrected in `docs/REQUIREMENTS.md`.

- `SAM-01` has no atomic IDs `SAM-01-003` or `SAM-01-004`, and `SAM-06` has no atomic IDs `SAM-06-003` through `SAM-06-006`. The cited Chapter 6 source text was checked: its four accounting-basis treatments are represented by existing `SAM-06-028` through `SAM-06-031`. The identifier gaps are retained to avoid renumbering stable IDs.
- `SAM-ANN-04-004` records the source narrative's insurance deduction of 8,000.00 and the displayed voucher's insurance-fund deduction of 16,000.00 (printed pages 93–95).
- `SAM-ANN-04-008` records the source situation date of २०७६ कार्तिक १५ गते and the first displayed voucher date of 2076/08/06 (printed pages 100–101).
- `SAM-ANN-04-010` records the voucher's displayed debit total of 70,000.00 and credit total of 700000.00, alongside the two displayed credit components of 20,000.00 and 50,000.00 (printed page 103).

## Remaining gaps

No coverage, source-page, status, duplicate-ID, or form-numbering gaps remain. The non-contiguous legacy atomic identifiers above are an audit-traceability note, not a missing manual extraction.
