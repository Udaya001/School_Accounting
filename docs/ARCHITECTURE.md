# Architecture

This is a proposed implementation architecture derived from the existing product specifications. The backend is a **modular monolith** with one primary transactional database; the Next.js frontend is a separate application layer, preferably in the same repository. The architecture deliberately avoids microservices, distributed ledgers, event brokers, and separate reporting databases until a concrete scale or integration requirement justifies them. `REQUIREMENTS.md` remains the source for verified manual obligations; this document makes implementation decisions, not new accounting rules.

## Recommended stack

| Layer | Recommendation | Rationale |
| --- | --- | --- |
| Frontend | Next.js with TypeScript | A separate, typed web application layer for the task-oriented screens, localization, and print initiation; it does not own authorization or accounting results. |
| Backend | Python 3.12+, FastAPI, Pydantic, SQLAlchemy 2.0 async, and Alembic | A clear, typed API/application layer; Pydantic validates boundaries, SQLAlchemy supports transactional async persistence, and Alembic keeps schema evolution reviewable. Python provides `Decimal` for authoritative accounting arithmetic. |
| Database | PostgreSQL | Reliable ACID transactions, constraints, reporting queries, backups, and mature operational tooling. |
| Files | S3-compatible object storage | Durable storage for scanned evidence and generated official outputs without placing files in the transactional database. |
| Rendering | HTML-based print templates rendered to PDF | Supports exact official Forms 1–40 and reports from the same approved record data. |
| Background execution | Separate scheduler/cron process backed by PostgreSQL, calling the same Python application services | Prevents multiple FastAPI API workers from running the same schedule, while avoiding Celery/Redis initially. |
| Deployment | Containerized Next.js frontend, FastAPI backend, scheduler process, managed PostgreSQL, object storage, and managed TLS | Repeatable releases and recoverable operations with little infrastructure to run. |

Keep frontend and backend in one repository with separate application directories/packages, shared contract-generation or contract-test tooling where useful, and independently deployable processes. Exact hosting provider, identity provider, document-rendering library, API-contract approach, and monitoring vendor are undecided. Select well-supported options during implementation without changing the boundaries below.

## System shape and modular boundaries

The Next.js frontend calls the FastAPI backend; it never directly accesses the database, object store, or accounting logic. Within the backend, FastAPI route handlers call an application layer that coordinates use cases and domain modules that own their rules. Suggested backend package boundaries mirror the modules below (for example `identity`, `financial_documents`, `accounting`, `reporting`, and `evidence`), with shared kernel code kept small. Modules communicate through in-process interfaces and committed domain events; they do not reach into each other’s persistence internals. The UI navigation is not the architecture: related user tasks may use the same domain module.

| Domain module | Owns | Does not own |
| --- | --- | --- |
| Identity & authorization | Users, school membership context, assigned permission presets, access checks, attribution, distinct-authority/self-approval checks | Financial approval policy or accounting calculations |
| School administration | School identity/tenant boundary and fiscal-year metadata | Statutory rules, accounting rules, or verified account codes |
| Financial documents | Income, expense, payroll, advances, deposits, travel, petty cash, bank statement/reconciliation, supporting workflow state | Journal mechanics and account balances |
| Budget & funding | Budget versions, releases, transfers, allocations, linked decision evidence | Payment execution or report rendering |
| Procurement & inventory | Requisitions, orders, receipt evidence, inventory custody, issue, transfer, inspection | Financial posting mechanics |
| Governance & compliance | SMC decision evidence, internal control, audits/beruju, social audit, guarantees | Permission administration or independent bookkeeping |
| Accounting engine | Derivation and posting of journals from approved business facts, books/balances, reconciliation calculations, adjustment treatment | UI flow, approval collection, caller-supplied authoritative journal lines, or user-managed rule editing |
| Reporting & forms | Read-only reporting projections, official-form and report rendering, export/archive metadata | Source transaction editing or accounting calculations |
| Evidence | File intake, immutable file identity, access-controlled retrieval, evidence links | Deciding whether evidence satisfies a workflow requirement |
| Rules catalogue | Effective-dated statutory/accounting rule sets and manual account-code catalogue | Ordinary school settings or routine user editing |

The product is multi-school SaaS-capable from the beginning. Each school is a tenant boundary, and every school-owned record is scoped by `school_id`. The backend enforces tenant scope for every read, write, report, export, evidence access, background job, and audit-history query; frontend filtering is never an isolation control. Normal repositories and query services for school-owned data require explicit tenant/school context and expose no routine unscoped access path. PostgreSQL Row Level Security may be considered later as optional defense-in-depth; it is not decided now. Do not introduce SSP-specific assumptions or defaults. The exact user-to-school membership schema is intentionally undecided until later data-model design.

## Deterministic accounting and posting boundary

Only the Accounting Engine may convert an approved/verified financial document into posted accounting effects. Its domain core is framework-independent pure Python with no FastAPI, SQLAlchemy, HTTP, or persistence dependencies. It receives the approved business document and its transaction facts, selected verified code(s), accounting date, fiscal year, and effective rule/version context, then deterministically derives the required debit/credit posting result itself; the caller must not supply authoritative journal lines. The workflow/application layer may validate completeness and authorization, but must not invent accounting entries. An application service owns authorization and orchestration, then persists the derived result through repositories within the database transaction, including the immutable journal/posting records, derived projections, and source-document Posted state. Repeating the same instruction must be idempotent: it must not create a second posting.

The engine must reject unbalanced derived treatment, invalid code/rule version, unavailable fiscal year, unauthorized transition, or duplicate post. Immutable journal/posting history is the financial source of truth. Bank cash book, budget account, balances, trial balance, monthly/annual accounts, and financial reports are derived/read projections that must be rebuildable from posted history. Cached or materialized projections are allowed for performance but are never authoritative. Bank statement entry and reconciliation exception handling remain user-facing financial-document functions; matching/calculation sits behind the engine boundary.

Authoritative money calculations never use binary floating point. Python accounting logic uses `Decimal`; PostgreSQL uses fixed-precision `numeric` types when the data model is designed. Frontend arithmetic is display/preview only and must never become an authoritative accounting result.

## Lifecycle, corrections, and history

The shared lifecycle is **Draft → Submitted/Review → Approved/Verified → Posted → Locked**, with Returned/Needs information and external-verification states where needed. The application layer enforces allowed transitions and required evidence/decision links before it asks the engine to post.

- Drafts and returned work may be edited by an authorized preparer; cancellation of unposted work records a reason and actor.
- Posted/locked financial records are never silently edited or deleted. A correction is a new, linked reversal, adjustment, or replacement that goes through normal authorization and posting.
- Manual-specific cancellation rules remain separate from the generic lifecycle, including retention of spoiled/cancelled receipts and their serial sequence.
- Every transition, approval/certification, decision-evidence link, posting, correction, export, and evidence action records actor, time, prior/new state, and reason where supplied.

## Authorization and audit trail

Authorization and tenant scope are enforced server-side at the FastAPI application boundary for every read, write, action, report, export, evidence download, job, and audit-history query; hiding a screen or filtering in Next.js is only a usability measure. Permission presets are the defaults in `ROLES_PERMISSIONS.md`, not legal authority. The system evaluates both the assigned preset and the documented authority/evidence required for the particular workflow.

Self-approval is blocked where distinct authority is required, even if one person holds multiple presets. A future staffing exception must be explicitly authorized by policy, visibly marked, and audit-logged. School Administrator access manages users, preset assignment, school metadata, and fiscal-year metadata only; it never confers financial approve, post, reverse, or rule-edit powers. No ordinary school role alters Accounting Engine rules or verified Account Code definitions.

Maintain an append-only audit log separate from business-record history. It must capture successful and denied sensitive actions, user/preset changes, configuration changes, exports, evidence access, and lifecycle changes. Financial journals and posted source documents are immutable application records; database permissions and migrations must prevent routine application paths from updating or deleting them. Retention periods, audit-log tamper-evidence mechanism, and legal-hold policy remain undecided.

## Rules, fiscal years, and Nepali dates

Rules are versioned and effective-dated. Resolve the applicable statutory/accounting rule versions primarily from the transaction’s accounting/effective date and relevant context, not the current server date or posting timestamp. This includes tax withholding, contributions, transfer limits, deadlines, accounting treatments, and other time-sensitive values identified in `MODULES.md`. Permanently pin the exact selected rule-set and account-code version to the posted record. Corrected or later records use the version applicable to their own accounting/effective date; rule changes never rewrite history.

The verified Annex 1/2 code catalogue is version-controlled system reference data, not an administrator setting. Its updates require a separate, system-level configuration/release boundary with source verification, effective dates, review, audit log, and compatibility checks; the concrete operating process is undecided.

Lifecycle timestamps such as `created_at`, `approved_at`, and `posted_at` are UTC timestamps. The accounting/business date is a separate date value, not a timestamp, and fiscal-year identity is stored explicitly. Preserve the user-entered Bikram Sambat date for input/display and use a tested centralized Bikram Sambat ↔ Gregorian conversion service at the domain boundary; do not scatter date conversion across screens or reports. Fiscal-year metadata defines its Nepali start/end dates, reporting periods, and close status. Closing prevents new normal postings to that year while allowing authorized, explicitly dated adjustment handling if the later policy permits it. Exact conversion library and year-close policy are undecided.

## Forms, reports, and evidence

Official Forms 1–40 and required reports are generated from approved/posted source data through the Reporting & Forms module, not maintained as separate editable copies. Each render uses a versioned official template, records source record identifiers, generation time, fiscal year, language, and template version, and can be regenerated while retaining the archived issued version. Printing/exporting does not approve or post a transaction.

Evidence files are stored in object storage with an immutable content identity (for example, checksum), metadata, uploader/time, tenant-scoped access control, and links to the relevant document, decision, audit finding, or guarantee. File replacement creates a new linked version; it never overwrites the prior evidence. Antivirus scanning, maximum file size/types, retention duration, and offline scanning workflow are implementation decisions still to be made.

## Background work and localization

Run background work only for tasks that do not need an interactive response: scheduled deadline/reminder evaluation, queued PDF/report rendering, delivery retries if notification is later added, and integrity/projection checks. Run schedules in a separate scheduler/cron execution process, not in FastAPI API workers, so multiple API workers cannot execute the same schedule. Jobs call the same application services as synchronous work, carry an explicit tenant scope, and remain idempotent, visible when failed, and retryable. Posting, approval, and permission checks remain synchronous and transactional. No Celery or Redis is required initially.

Keep translation keys and locale formatting at the presentation boundary. Nepali and English labels, dates, numbers, and generated-output language are selected per user/school preference; stored financial amounts, codes, statuses, and accounting facts remain locale-neutral. The initial language default and official bilingual form-output policy are undecided.

## Testing and operations

Test the architecture in layers:

- Unit-test Accounting Engine invariants: every derived journal balances; no duplicate posting; valid lifecycle only; posted history is immutable; corrections preserve net traceability; fiscal-year and code/rule versions are valid; and authoritative values use `Decimal`/fixed precision rather than binary floating point.
- Turn internally consistent Annex 4 scenarios into named executable accounting golden/acceptance tests, asserting stated debit/credit treatment, amounts, codes, and affected records. Preserve known source inconsistencies as discrepancy fixtures and explicitly resolve them before using them as authoritative expected engine output; never encode a known printed inconsistency as correct accounting behavior.
- Test workflow authorization, tenant isolation, self-approval blocking, joint-authorization evidence, required decision evidence, report/form output fields, Nepali-date conversion boundaries, and tenant-scoped evidence access controls.
- Add integration tests for database transactions, reporting projections, object-storage evidence links, and backup-restore verification; reserve browser-level tests for a small set of critical user journeys.

Deploy with separate development, test, and production environments; encrypted connections and storage; least-privilege database/object-storage credentials; managed TLS; health checks; structured logs; and alerting for failed jobs, backup failures, and unexpected posting errors. Run API and scheduler processes separately. Take automated PostgreSQL backups with point-in-time recovery where available, versioned object-storage backups, and regular restore drills that verify both records and linked evidence. Recovery objectives, data residency, notification channel, and support/incident process are undecided and must be agreed before production use.
