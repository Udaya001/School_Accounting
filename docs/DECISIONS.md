# Decisions

## Decision log

| ID | Date | Decision | Rationale | Status |
| --- | --- | --- | --- | --- |
| DEC-001 | 2026-09-22 | Treat the School Accounting Manual 2076 PDF as the authoritative source. | The project requires a definitive basis for later requirements. | Accepted |
| DEC-002 | 2026-09-22 | Maintain a verified requirements register rather than repeatedly consulting the full manual. | It makes implementation work efficient while retaining source references for exact verification. | Accepted |
| DEC-003 | 2026-09-22 | Defer application code until specification work establishes requirements and scope. | Prevents premature implementation. | Accepted |
| DEC-004 | 2026-09-24 | Keep `bank_reconciliation_items.journal_line_id` as a nullable reserved UUID and prohibit `confirmed` items until the journal slice exists. | Resolved by migration `20260926_0007`: the item now has a same-school journal-line FK and a deferred PostgreSQL validation of the immutable posted line against the bank account's effective-dated ledger binding. | Resolved |
| DEC-005 | 2026-09-24 | Support English (`en`) and Nepali (`ne`) as the initial standard locales, with locale fallback from membership preference to school default to system fallback (`en`). | Localization is a presentation concern. Canonical accounting/workflow values and user-entered text remain unchanged; normalized translation records localize only system-controlled reference display text, while official template language remains independently versioned. | Accepted |

## How to add decisions

Record decisions that materially affect scope, architecture, data handling, compliance, or user workflows. Link related requirement IDs and note replacements when a decision changes.
