# Accounting Engine Contract

## Purpose and boundary

The Accounting Engine is a deterministic Python domain component that turns an approved financial document and its verified business facts into a balanced proposed journal. It implements debit-credit derivation; it does not authorize a document, allocate voucher numbers, persist rows, reconcile a bank statement, or render reports.

It accepts plain immutable values/dataclasses and returns plain immutable values/dataclasses or structured validation errors. It imports neither FastAPI, SQLAlchemy, repositories, database sessions, nor PostgreSQL types. The application layer loads the facts and versions, calls the engine, and atomically persists the returned pinned result, journal entry, lines, and idempotency completion.

## Contract

### Inputs

`PostingCommand` must contain: school and document identity; fiscal year; accounting date; document type/status; source facts and source-line facts; approved authority/evidence outcome; selected `bank_account_id` for a bank transaction or an explicit physical-cash destination where applicable; request idempotency key; and correction context where applicable.

`PostingReferences` must contain already-loaded, effective-dated system references: one published rule-set version, applicable Annex code versions, canonical ledger-account definitions, and the school's active effective ledger-account bindings. It must also contain the applicable bank-to-ledger binding for bank-affecting entries.

The engine must never accept caller-authored journal debit/credit lines as input.

### Outputs

On success, return a `DerivedPosting`: journal header and ordered journal lines; an explainable derivation trace; and a complete audit/derivation reference set. The set pins every reference actually used: rule-set version/context, Annex-code versions/context, ledger-account definitions, school ledger accounts, and the effective bank-account ledger binding when a bank is involved. These preserve derivation evidence, not new accounting identities. Each line has exactly one positive `Decimal` side. The output is valid only when total debits equal total credits. The persistence layer assigns database IDs and hashes; hashes are integrity aids, never operation identity.

On failure, return typed errors identifying missing facts, an invalid status/date/fiscal year, unavailable effective reference, unsupported treatment, or an unbalanced derivation. It must not partially derive a journal.

## Preconditions and common validation

- The document is approved before posting; a successful persistence transaction changes it to `posted` or `locked`.
- The document, request, and journal use one school, fiscal year, and accounting date. Accounting date must fall in the fiscal year.
- Amounts are `Decimal`, finite, and non-negative. Source values use the explicit precision permitted by their source/rule; floating point is prohibited. The engine never relies on Python's ambient `Decimal` context or default rounding. Percentage, tax, and deduction calculations use an explicit scale and rounding mode pinned in rule context. Final NPR journal lines are explicitly quantized to fixed two-decimal precision and sums compare exactly. The statutory rounding method is **UNRESOLVED** where the verified requirements do not define it.
- Income lines require a published effective Annex 1 (`income`) code; expenditure lines require a published effective Annex 2 (`expense`) code. Annex classifications remain separate dimensions from ledger accounts.
- The selected rule-set version is published and effective on accounting date. A ledger definition and its school ledger account must be active and effective on accounting date. Resolution is deterministic: semantic key → exactly one applicable school ledger account. A bank transaction instead resolves through its selected `bank_account_id` and exactly one effective `BankAccountLedgerBinding`; physical cash, where applicable, resolves through a distinct `physical_cash` semantic and school-ledger mapping. Zero or multiple applicable mappings is an error.
- Required workflow facts, supporting-document/approval status, budget conditions, and bank evidence are validated by the application/domain boundary before derivation. The engine rechecks only facts supplied to its contract.

The catalogue version and every resolved reference ID are pinned in output; later reference changes cannot reinterpret a posting.

## Canonical semantic catalogue

The following semantic keys are implementation necessities, not an alternate chart of accounts. A school maps each key to its own effective `school_ledger_accounts` row.

| Semantic | Basis | Use |
| --- | --- | --- |
| `bank` | Directly supported: bank-only school transactions and bank cash book (`SAM-02-006`, `SAM-06-038`, `SAM-06-048`) | Resolved only through selected bank account and effective binding. |
| `physical_cash` | Inferred distinction required by cash-receipt facts | Separate cash ledger mapping when an applicable rule permits physical cash; control/timing policy is **UNRESOLVED**. |
| `income` | Directly supported: income headings and debit-credit rules (`SAM-03-001`–`004`, `SAM-06-009`) | Credit income, dimensioned by Annex 1 code. |
| `expense` | Directly supported: expenditure headings/general vouchers (`SAM-06-042`) | Debit expense, dimensioned by Annex 2 code. |
| `advance` | Directly supported: advance subsidiary account (`SAM-06-067`–`070`) | Advance asset and settlement. |
| `deposit_liability` | Directly supported: general/individual deposit accounts (`SAM-06-071`–`077`) | Deposit receipt/refund. |
| `income_receivable`, `payment_liability` | Directly supported by `SAM-06-029`, `SAM-06-031` | Required for earned-unreceived income and incurred-unbilled expenditure. Exact triggering policy is **UNRESOLVED**. |
| `withholding_tax_liability`, `retention_liability`, `payroll_deduction_liability` | Inferred necessity from Annex 4 withholding/deduction entries | Separate liabilities pending payment. |
| `payroll_expense`, `petty_cash`, `fixed_asset_or_inventory` | Inferred implementation necessities | Need rule-set mapping; capitalization versus expense is **UNRESOLVED**. |

## Posting lifecycle, idempotency, and corrections

One successful operation owns one request, result, and journal entry. Retrying the same tenant-scoped operation key resolves that completed result; it never derives another journal. A failed attempt owns no authoritative result/journal and may be retried with a new request/key. Database constraints are the final concurrency guard.

Corrections append a new approved document, posting, and journal. `reversal` applies the exact original journal with debit/credit sides swapped; `adjustment` and `replacement` require explicit approved corrected facts and an explicit rule branch. The original is never changed. A correction link must name matching original/correcting documents and entries, cannot self-link or cycle, and remains append-only. The exact conditions selecting adjustment versus replacement are **UNRESOLVED**. Reversing after the original ledger or Annex versions are no longer effective is also **UNRESOLVED**: exact historical reversal and normal effective-date validation must not silently conflict.

## Workflow rules

Each pattern below is a derivation pattern, not permission to post without its listed facts. Liability, receivable, asset, withholding, retention, and deduction lines appear only when supplied facts and the pinned rule mapping select that branch. A document can produce multiple lines whenever it has multiple headings, deductions, recipients, or settlement components.

| Workflow | Required facts and classification | Semantic pattern / journal shape | Branches and status |
| --- | --- | --- | --- |
| Fee/cash income | Receipt issue, payer/student where applicable, amount, receipt/bank evidence, Annex 1 income code (`SAM-06-007`–`023`, `027`–`029`) | Debit the selected bank binding; credit `income` for each heading. | Physical cash needs the distinct `physical_cash` mapping. Cash receipt control is evidence/projection, not a journal line. |
| Other income | Bank voucher/statement, amount(s), Annex 1 code (`SAM-06-008`–`009`) | Debit the selected bank binding; credit `income` per classified amount. | Release-heading semantic treatment is **UNRESOLVED**. |
| Normal expense/payment | Approved order/evidence, budget availability, payee, payment amount, Annex 2 code, withholding facts (`SAM-06-032`–`042`) | Debit `expense`; credit selected bank binding for net paid; credit a liability only when the rule/facts select withholding or retention. | A remittance branch debits that liability and credits selected bank binding. |
| Payroll | Approved salary report, gross components, deductions, employee payment facts, Annex 2 codes (`SAM-06-041`) | Debit `payroll_expense`; credit selected bank binding for net pay and deduction liabilities only when selected by facts/rule. | Remittance debits selected liabilities and credits selected bank binding. Scenario 004 remains discrepancy-only. |
| Advances | Approved recipient/purpose, amount, bank payment, advance subledger identity (`SAM-06-067`–`070`) | Debit `advance`; credit selected bank binding. | Annex 4 scenario 009 is a candidate golden test. |
| Advance settlement | Linked advance, approved settlement facts and amounts | Debit resulting `expense`/asset semantic; credit `advance`; refund/excess handling is **UNRESOLVED**. | Must preserve the linked advance history. |
| Deposits | Depositor, deposit purpose, bank receipt (`SAM-06-071`–`077`) | Debit selected bank binding; credit `deposit_liability`. | Long-unclaimed legal recognition as income is **UNRESOLVED**. |
| Deposit refund | Linked deposit, eligibility/completion facts, bank payment | Debit `deposit_liability`; credit selected bank binding. | Partial-refund policy is **UNRESOLVED**. |
| Travel claim/payment | Approved travel order, submitted travel report/bill, budget availability, classified claim and bank payment (`SAM-06-082`–`085`) | Debit `expense`; credit selected bank binding. | Advance/netting treatment is **UNRESOLVED**. |
| Petty cash | Fund type, approved small expenditure or replenishment facts (`SAM-06-086`–`087`) | Spending: debit `expense`, credit `petty_cash`; replenishment: debit `petty_cash`, credit selected bank binding. | Current workflow evidence and physical-cash mapping remain **UNRESOLVED**. |

## Annex 4 test fixtures

Use internally balanced, internally consistent displayed scenarios as candidate golden tests: 001 (release receipt), 002/006 (expense plus withholding remittance), 003/007 (expense payment), 005 (income receipt), and 009 (advance). A golden test asserts the displayed amounts, debit/credit side, code context, and multi-line shape only after the corresponding semantic mapping is approved.

Never silently normalize discrepancies. Annex 4 scenario 004 has a stated insurance/deduction inconsistency; scenario 008 has conflicting source and voucher dates; scenario 010 displays an inconsistent credit total. They remain explicit discrepancy fixtures and cannot become authoritative expected engine outputs until resolved.

## Unresolved accounting decisions

1. Rule mappings from Annex income/expense codes to canonical ledger semantics, including funding/release headings.
2. Recognition timing and journal treatment for fee receivables, payment liabilities, grants/releases, assets/inventory, and petty-cash workflow details.
3. Advance-settlement refunds/excess, travel advances/netting, partial deposit refunds, and long-standing deposit legal recognition.
4. The approved rule-set treatment for withholding, retention, payroll deductions, and their statutory remittance details.
5. Resolution of Annex 4 scenarios 004, 008, and 010 before they become golden outputs, and reversal policy after original references expire.
