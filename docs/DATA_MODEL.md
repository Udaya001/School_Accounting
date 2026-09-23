# Conceptual Data Model

This model translates the existing architecture, workflows, permissions, screens, traceability, and verified requirements into conceptual domain data. It defines names, ownership, relationships, and history rules only. It does not select database indexes, exact types, endpoint contracts, ORM classes, migration order, or table layout.

## Ownership and tenant scope

`School` is the tenant root. Every school-owned entity below carries `school_id` and belongs to exactly one school. Normal repositories and query services require explicit school context for all reads, writes, reports, exports, evidence access, jobs, and audit-history access; they expose no routine unscoped path. The frontend never supplies tenant isolation through filtering.

| Ownership | Conceptual entities | Scope |
| --- | --- | --- |
| System-owned control-plane/reference data | `User`, `School`, `PermissionPreset`, `PlatformAdministrator`, `PlatformAuthorizationGrant`, `RuleSetVersion`, `AccountCodeVersion`, `LedgerAccountDefinition`, `OfficialTemplateVersion`, `SupportedLocale`, `PlatformAuditEvent` | Global, except `School` is the tenant root rather than a school-owned record. `PlatformAdministrator` and `PlatformAuthorizationGrant` govern school provisioning, publication of system rule/account-code/template versions, and other platform administration. `PlatformAuditEvent` is append-only history for those actions. Platform authority does not automatically grant routine access to tenant financial data. |
| School-owned operational data | Every aggregate listed under domain modules below, including memberships, documents, postings, projections, evidence links, outputs, and audit events | **`school_id` required on every record.** A cross-school reference is prohibited except a system-owned entity reference. |

`User` is a global identity and may belong to multiple schools through separate `SchoolMembership` records. Each membership belongs to exactly one school and is school-owned (`school_id` required). Each request/session operates in exactly one explicit school tenant context selected through a membership. `PermissionAssignment` is school-owned (`school_id` required), belongs to a membership, and assigns one or more system-owned `PermissionPreset` values. Presets remain defaults, not a substitute for documented authority or decision evidence.

## Shared concepts

All school-owned aggregates have a stable internal identity, `school_id`, creation/update attribution, and lifecycle history where relevant. Lifecycle timestamps are UTC. A separate `accounting_date` records the business date, and `fiscal_year_id` identifies the fiscal year. The input/display Bikram Sambat date may be retained with its converted accounting date; it is not inferred from an event timestamp.

`ReceiptSeries`/`ReceiptBook` and `ReceiptIssue` provide school-owned (`school_id` required) receipt/serial control: series or book identity, fiscal-year control, issued number, and issued/cancelled/spoiled state with its reason and replacement link where applicable. `DocumentSequence` is school-owned (`school_id` required) generic sequence control for school/fiscal-year documents such as vouchers, requisitions, orders, receipt reports, transfers, forms, and reports. Exact numbering formats, reservation behavior, collision handling, and reissue policies remain unresolved where the manual does not specify them.

Lightweight school-owned (`school_id` required) reference concepts support existing work without creating a school-management system: `StudentAccount` for fee-register transactions, `StaffPerson` for salary/payroll transactions, and structured `Party` records for payer, payee, supplier, contractor, bank, grant body, depositor, advance recipient, auditor, or other external body. `Party` can carry relevant identifiers such as PAN. Each can retain an external/import reference for later integration with another system. Exact fields, synchronization behavior, and whether some one-off parties remain document-local are unresolved.

Common mutable workflow status is `Draft`, `Submitted/Review`, `Returned/NeedsInformation`, `Approved/Verified`, `Posted`, and `Locked`, plus workflow-specific states such as `Cancelled`, `Reconciled`, `Settled`, or `Expired`. Posted financial documents are locked. They may be corrected only through linked, new business documents and postings.

## Domain aggregates

| Module | School-owned aggregates and key concepts | Relationships and boundaries |
| --- | --- | --- |
| School administration | `FiscalYear`, `SchoolSettings`, `SchoolFund`, `BankAccount`, `ReceiptSeries`/`ReceiptBook`, `ReceiptIssue`, `DocumentSequence` | **`school_id` required.** `FiscalYear` has an explicit identity, Nepali start/end dates, reporting periods, and close state. `SchoolFund` is the school’s operational fund concept; exactly one exists per school unless a future verified rule changes that requirement. `BankAccount` represents a school bank account; bank statements/reconciliations belong to one bank account, and related payments/releases may reference it. Settings hold school/fiscal metadata only; they do not own rules or account codes. |
| Identity & authorization | `SchoolMembership`, `PermissionAssignment`, `AuthorizationDecision` | **`school_id` required.** Membership owns access within one school; assignments link it to system presets. `AuthorizationDecision` records approval, certification, joint-authorization evidence, self-approval exception if ever authorized, or return action against an aggregate. |
| Financial documents | `IncomeReceipt`, `IncomeVoucher`, `ExpenseVoucher`, `PaymentRequest`, `PayrollRun`, `Advance`, `AdvanceSettlement`, `Deposit`, `DepositRefund`, `TravelOrder`, `TravelClaim`, `PettyCashEntry`, `BankStatement`, `BankStatementLine`, `BankReconciliation` | **`school_id` required.** These aggregates own entered business facts, selected classification codes, accounting date, workflow state, parties, evidence links, approval/history links, and references to their posting result. They do **not** own authoritative debit/credit lines. `BankStatement` and `BankReconciliation` belong to a `BankAccount`; reconciliation owns statement matching and explanations, not cash-book balances. |
| Budget & funding | `Budget`, `BudgetRevision`, `BudgetAllocation`, `FundingReleaseRequest`, `FundingRelease`, `BudgetTransfer` | **`school_id` required.** A budget belongs to one fiscal year and has versions/revisions; allocations belong to a budget version and verified code/version context. Release requests and transfers link to the budget/fiscal year, decision evidence, and any posted result. |
| Procurement & inventory | `Requisition`, `PurchaseOrder`, `GoodsReceipt`, `InventoryItem`, `InventoryMovement`, `InventoryHolding`, `InventoryIssue`, `InventoryTransfer`, `InventoryInspection`, `AssetRecord` | **`school_id` required.** Requisition/order/receipt form a procurement chain. `InventoryMovement` is immutable history for receipt, issue, transfer, adjustment, and other custody/quantity changes. `InventoryHolding` is rebuildable quantity/custody state derived from movement history. Transfers and inspections carry condition and decision/verification evidence. Related financial documents link to this chain but remain separate aggregates. |
| Governance & compliance | `DecisionEvidence`, `MeetingRecord`, `InternalControlPlan`, `ControlAction`, `AuditEngagement`, `AuditFinding`, `FindingSettlement`, `SocialAudit`, `BankGuarantee`, `GuaranteeVerification` | **`school_id` required.** `DecisionEvidence` can link to budget, spending, inventory transfer, control, or another authorized aggregate without changing its lifecycle. Audit findings own dated responses and settlements. Guarantees own issuing-bank verification history. |
| Evidence | `EvidenceFile`, `EvidenceFileVersion`, `EvidenceLink` | **`school_id` required.** A file has immutable content identity and metadata; each replacement is a new version. An evidence link associates a file version with one permitted aggregate or history event and states its role, such as bill, receipt, decision minute, bank statement, or audit response. |
| Reporting & forms | `ReportRequest`, `ReportSnapshot`, `GeneratedOutput`, `OutputArchive` | **`school_id` required.** A request selects a report/form, fiscal period, locale, and source scope. A snapshot records the projection/source history used. Generated output links to a system-owned official template version and is retained as an issued artifact; it never becomes editable financial source data. |
| Accounting | `PostingRequest`, `PostingResult`, `JournalEntry`, `JournalLine`, `CorrectionLink`, `IdempotencyRecord`, `SchoolLedgerAccount` | **`school_id` required.** These are detailed below; journal entries and lines are immutable financial source-of-truth records. `SchoolLedgerAccount` provides school-specific ledger accounts where needed. |
| Projections | `LedgerProjection`, `BankCashBookProjection`, `BudgetAccountProjection`, `BalanceProjection`, `TrialBalanceProjection`, `IncomeExpenseAccountProjection`, `AdvanceDepositProjection`, `InventoryHolding`, `InventoryReportProjection`, `ReportProjectionRun` | **`school_id` required.** Financial books/balances derive from immutable posted history. Budget projections derive from approved budget/revision/transfer/release records plus relevant posted financial history. Inventory quantity/custody projections derive from immutable inventory movement history. Each may be rebuilt and is never editable accounting authority. |

## Accounting source of truth and posting

`PostingRequest` is a school-owned (`school_id` required) application-level record or durable command identity linking one approved business document to an idempotency key, accounting date, fiscal year, selected rule/account-code versions, and transaction facts. It contains no caller-authored authoritative debit/credit lines.

The framework-independent Accounting Engine domain core reads the approved facts and resolved versions, then derives one deterministic `PostingResult`. The application service authorizes and orchestrates this result and persists it through repositories in one transaction. The result creates an immutable `JournalEntry` and its immutable `JournalLine` children. Each entry links to exactly one posting source/business document and one fiscal year; each line references a ledger account and carries the derived debit or credit amount, with income/expense classification code/version context where applicable. All are school-owned (`school_id` required).

`JournalEntry` and `JournalLine` are the financial source of truth. They are append-only after posting. Cash books, budget accounts, balances, trial balance, monthly/annual accounts, and financial reports derive from them and must be rebuildable. `PostingResult` retains the rule/account-code version references and derivation outcome used for a particular post.

`IdempotencyRecord` is school-owned (`school_id` required) and associates the posting operation identity with its completed journal entry/result. Retrying the same approved posting request returns the existing result. `CorrectionLink` is school-owned (`school_id` required) and relates an original posted document/journal entry to the new reversal, adjustment, or replacement document/journal entry. It records correction type, reason, and attribution. It never mutates the original entry.

## Rules, codes, dates, and templates

`RuleSetVersion` is system-owned reference data for statutory/accounting rules. It has stable identity, effective period, rule context, source/review metadata, and status. `AccountCodeVersion` is system-owned reference data for the verified Annex 1/2 income/expense classification catalogue, with code, title/meaning, effective period, source/review metadata, and status. It is not a ledger chart of accounts.

`LedgerAccountDefinition` is a system-owned account semantic: stable identity, accounting role/meaning, normal debit/credit behavior, effective period, and rule mapping context. `SchoolLedgerAccount` is school-owned (`school_id` required) and represents a school-specific ledger account where required, linked to a system definition or other approved semantic. The engine resolves the ledger account(s) for a posting from facts, rules, and account semantics. A journal line always references a ledger account and may additionally carry an `AccountCodeVersion` classification. Exact chart-of-accounts structure, school-specific account creation authority, and the rule mapping model remain unresolved.

Rule resolution produces a recorded selection for the posting. It uses the business document’s accounting/effective date and relevant context, never the current server date or posting timestamp. The exact selected `RuleSetVersion` and `AccountCodeVersion` are permanently pinned to the posted record. Later rule changes do not rewrite postings.

`OfficialTemplateVersion` is system-owned reference data for Forms 1–40 and reports. It has a stable template/form identifier, language, version, effective period, source/review metadata, and rendering definition. `GeneratedOutput` stores the template version, source snapshot, generation timestamp, locale, fiscal-year scope, and archive reference. Exact template authoring/storage format is unresolved.

## History, mutability, and audit

Draft workflow aggregates and mutable planning records may change only through authorized transitions. Their `LifecycleEvent` history is school-owned (`school_id` required) and records status change, actor/membership, UTC time, reason, and related approval or decision evidence.

Financial source records become immutable at Posted/Locked: `PostingResult`, `JournalEntry`, `JournalLine`, and the posted snapshot of their business document facts. Corrections append new linked records. Evidence versions and issued outputs are immutable once retained. Projection records are replaceable/rebuildable and carry provenance to the posting history/projection run from which they were derived.

`AuditEvent` is school-owned (`school_id` required), append-only, and separate from lifecycle history. It records successful and denied sensitive actions, tenant context, actor/membership, affected entity identity, export/evidence access, configuration actions, and relevant before/after summaries. `PlatformAuditEvent` is the separate system-level append-only history for platform authorization, school provisioning, and publishing system rule/account-code/template versions; it does not confer tenant financial-data access. Retention, tamper-evidence implementation, legal holds, and whether all general reads are logged remain unresolved.

## Key relationship summary

```text
School
  ├─ SchoolMembership ─ PermissionAssignment ─ PermissionPreset (system)
  ├─ FiscalYear ─ Budget / Financial documents / JournalEntry / Projections
  ├─ SchoolFund (one per school) / BankAccount ─ BankStatement ─ BankReconciliation
  ├─ ReceiptSeries/ReceiptBook ─ ReceiptIssue; DocumentSequence
  ├─ Business document ─ Approval, DecisionEvidence, EvidenceLink, LifecycleEvent
  │                     └─ PostingRequest ─ PostingResult ─ JournalEntry ─ JournalLine
  │                                                └─ CorrectionLink → later posting
  ├─ InventoryItem ─ InventoryMovement ─ InventoryHolding (rebuildable)
  ├─ EvidenceFile ─ EvidenceFileVersion ─ EvidenceLink
  └─ ReportRequest ─ ReportSnapshot ─ GeneratedOutput ─ OfficialTemplateVersion (system)
```

Every path beginning at a school-owned entity remains within the same `school_id`. System references are read-only inputs to school operations. Cross-tenant references, projections, evidence links, exports, and background-job work require the same explicit school context.

## Unresolved modeling decisions

- Membership fields, invitation/deactivation behavior, and exact platform authorization grant design.
- Student/staff/party fields, import-reference ownership, synchronization behavior, and whether some one-off parties remain document-local.
- Exact shared-document abstraction versus distinct entities for each workflow, including which document facts are reused.
- Business-identifier sequence scope, format, reservation, void/reissue, and fiscal-year reset behavior beyond verified manual rules.
- Exact journal account taxonomy, system account semantics, school-specific account creation authority, and the mapping structure used by the pure accounting core.
- Fiscal-year close/reopen and post-close-adjustment policy.
- Rule/catalogue release workflow, compatibility handling, and the relationship between rule sets and account-code versions.
- Evidence retention, virus-scanning, file-size/type controls, audit-log tamper evidence, legal holds, and PostgreSQL Row Level Security as defense-in-depth.
- Projection refresh strategy, report snapshot retention, and output-template authoring/storage format.
