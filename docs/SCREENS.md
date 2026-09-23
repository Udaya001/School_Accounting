# Screen Map

This proposed information architecture turns `MODULES.md` and `WORKFLOWS.md` into task-oriented pages for non-technical school staff. Access is permission-based: the named presets below are defaults, not hardcoded authority. Screens and actions remain subject to `ROLES_PERMISSIONS.md`; Accounting Engine and Account Codes are background concepts, not sidebar items.

## Primary navigation

Keep the main navigation to these entries; show only entries a person can access:

1. **Dashboard** — actionable work and status overview.
2. **Money In** — fee/cash collection and other income.
3. **Expenses & Payments** — expenses, payroll, advances, deposits, travel, petty cash, and bank reconciliation.
4. **Goods & Assets** — procurement, receipt, inventory, and asset stewardship.
5. **Budget & Funding** — annual budget, funding releases, and transfers.
6. **Reports** — generated statements and operational reports.
7. **Controls & Audit** — audit/beruju, social and internal control, guarantees, and linked decision evidence.
8. **Settings** — school administration only; hidden from users without configuration permissions.

## Permission key

- **AP — Accounts preparer:** prepare and submit accounting records; post only after required approval or automatic verification.
- **HA — Head Teacher / Approver:** review, approve, certify, or return within documented authority; no broad entry by default.
- **SO — Store / Operational Staff:** enter physical stock, receipt, issue, transfer, inspection, and assigned request evidence.
- **DE — SMC Decision Evidence:** create/view/submit links and evidence of committee decisions only; cannot edit or post the linked transaction.
- **SA — School Administrator:** user/preset assignment and non-accounting configuration only; no financial approval, posting, or reversal authority by virtue of this preset.
- **R** means read/review; **P** prepare/submit; **A** approve/certify; **E** record/link decision evidence; **O** operational inventory/request entry; **C** configure users/settings. A blank means no default access. Presets can be combined, subject to the self-approval and authority limits in `ROLES_PERMISSIONS.md`.

## Dashboard

**Purpose:** Show the user what needs attention today and provide direct entry points to permitted tasks, without presenting accounting codes or bookkeeping internals.

**Actionable information:** Items awaiting review/approval; returned records and missing evidence; receipts or deposits needing follow-up; unreconciled bank items; unposted/locked status; payroll, budget, release, or report deadlines; pending goods receipt/inspection; unsettled advances/deposits; open audit findings/control actions/guarantees; committee evidence requests. Counts and actions are permission-filtered. Dashboard summaries link to the source record; they do not themselves approve or post.

**Access/actions:** AP, HA, SO, DE, and SA may view role-relevant summaries. Each can open only actions allowed by its preset; DE sees evidence tasks and SA sees administration tasks, not financial approval queues by default.

**States shown:** Draft; Submitted/Review; Approved/Verified; Posted; Locked; Returned/Needs information; Pending external verification; Reconciled/Complete; Overdue/Open. These labels are product UX choices and do not amend manual timing or accounting rules.

**Related workflows:** All workflows below; dashboard is a cross-workflow entry point, not a substitute for them.

## Screen map

| Primary navigation / secondary page | Purpose | Primary actions | Presets with access/action | Important status/state | Related workflow(s) |
| --- | --- | --- | --- | --- | --- |
| **Money In → Collect Fee / Cash Income** | Record fee or cash receipt and its supporting control/accounting records. | AP: prepare/submit receipt and voucher, print payer receipt. HA: review exceptions/authority. | AP P; HA R/A as authorized; DE E only if decision evidence is needed. | Draft, receipt issued, deposit due, submitted, posted/locked, cancelled receipt retained. | Fee and cash income collection |
| **Money In → Record Other Income** | Record non-fee income, bank receipts, and earned-but-unreceived income. | AP: record source/evidence and submit voucher. HA: review as authorized. | AP P; HA R/A within authority. | Evidence missing, receivable, submitted, posted/locked, unmatched bank item. | Other income and bank receipts |
| **Expenses & Payments → Record Expense / Payment** | Prepare supported spending and payment records. | AP: enter expense, attach evidence, submit. HA: approve/return within delegated authority. SO: initiate request and attach receipt evidence. | AP P; HA R/A; SO O/request only; DE E when SMC decision applies. | Draft, missing evidence, review, approved, posted/locked, correction required. | Expense and payment |
| **Expenses & Payments → Payroll** | Prepare salary request/payroll, deductions, payments, and remittances. | AP: prepare/payroll details and remittance evidence. HA: review/approve/certify as required. | AP P; HA R/A; DE E only if committee evidence is relevant. | Period due, pending salary approval, deductions/remittance due, posted/locked. | Payroll |
| **Expenses & Payments → Advances** | Issue and track advances and record settlement. | AP: prepare advance, recipient folio and settlement. HA: approve within authority. | AP P; HA R/A; SO submit receipt/settlement evidence. | Pending approval, outstanding, partially settled, settled, posted/locked. | Advances |
| **Expenses & Payments → Deposits** | Record deposits, depositor balances, refunds, and statements. | AP: record receipt/refund and statement. HA: review/approve within authority. | AP P; HA R/A; SO may provide supporting work-completion evidence. | Held, refund due, unresolved depositor, statement difference, closed/posted. | Deposits |
| **Expenses & Payments → Travel** | Record travel order, report, claim, and vehicle-log evidence. | AP: prepare claim/payment. HA: authorize travel and review claim. Travelling staff: provide report/claim evidence. | AP P; HA R/A; SO O/request evidence where assigned. | Awaiting prior approval, travelling, report due, claim review, paid/posted. | Travel |
| **Expenses & Payments → Petty Cash** | Track fund, supported spending, and replenishment. | AP: record expenses/replenishment. HA: approve as required. Custodian: provide receipts. | AP P; HA R/A; SO provide evidence. | Fund balance, draft, evidence missing, replenishment requested/posted. | Petty cash |
| **Expenses & Payments → Reconcile Bank** | Enter statement information, compare with cash book, resolve differences. | AP: enter statement, match, explain differences, propose adjustment, submit. HA: review/authorize as required. | AP P; HA R/A; DE/SA no default transaction action. | Statement period, unmatched items, explanation needed, adjustment review, reconciled. | Bank reconciliation |
| **Goods & Assets → Purchase Requests & Orders** | Initiate a goods request and prepare an authorized purchase order. | SO: prepare requisition/order evidence. HA: approve within authority. AP: attach financial/payment records. | SO O/P; HA R/A; AP P for financial record; DE E where a committee decision is required. | Draft, awaiting approval, ordered, discrepancy/open, completed. | Procurement and goods receipt |
| **Goods & Assets → Receive Goods** | Record inspection and receipt/entry of purchased, transferred, donated, or government-provided goods. | SO: record quantity/condition and submit receipt. HA: certify where required. AP: link purchase/payment records. | SO O/P; HA R/A/certify; AP P for financial records; DE E for linked committee decision. | Awaiting delivery, receipt review, discrepancy, accepted/entered. | Procurement and goods receipt |
| **Goods & Assets → Inventory & Assets** | Record issues, custody, transfers, annual stock and physical inspection, and asset records. | SO: issue/transfer/inspect and record condition. HA: authorize/certify assigned actions. DE: link required SMC transfer decision. AP: view values/reporting records. | SO O/P; HA R/A; DE E only; AP R/P for related accounts. | Available, issued, transfer decision pending, in transit, inspection due, variance/open finding, complete. | Inventory issue, transfer, and inspection |
| **Budget & Funding → Prepare Annual Budget** | Prepare income/expenditure estimates and programme for approval. | HA: prepare/present budget. AP: enter estimates and supporting figures when assigned. SO: provide needs. DE: link annual meeting and SMC approval evidence. | HA P/R; AP P; SO provide input; DE E. | Draft, deficit check, awaiting SMC decision, approved, submitted. | Annual budget |
| **Budget & Funding → Funding Releases** | Request and record funding releases and required supporting materials. | AP: prepare/submit requests and record release. HA: review/authorize as assigned. DE: attach committee decision evidence if required. | AP P; HA R/A; DE E if applicable. | Release period due, missing documents, submitted, released, recorded. | Budget release |
| **Budget & Funding → Budget Transfers** | Request, review, and record a transfer between budget headings. | AP: calculate/prepare request. HA: approve within authority or refer. DE: link required SMC decision. | AP P; HA R/A within authority; DE E; SO no default access. | Draft, limit check, SMC decision pending, approved/rejected, applied. | Budget transfer |
| **Reports → Report Centre** | Generate, review, certify, submit, and retain periodic/annual reports. | AP: generate/reconcile/submit. HA: review/certify where required. DE: view relevant evidence. SO: view assigned inventory outputs. | AP P/export; HA R/A/export; SO R of assigned output; DE R linked evidence. | Period due, incomplete source, difference found, awaiting certification, submitted, retained. | Periodic and annual reporting; related source workflows |
| **Controls & Audit → Audit & Beruju** | Organize audit records, responses, irregularities, and settlement evidence. | AP: maintain records/findings. HA: arrange audit, review response, oversee settlement. Auditor/local body remain external. | AP P; HA R/A/oversight; DE E for required committee decisions. | Audit due, evidence requested, response pending, open/settled finding, report submitted. | Audit and beruju settlement |
| **Controls & Audit → Social Audit** | Prepare public annual review material, record presentation and follow-up. | AP: assemble financial material. HA: coordinate/review. DE: link committee/meeting decision evidence. | AP P; HA R/A/oversight; DE E; external parents/public no login. | Preparation, meeting due, presented, submission due/complete, follow-up open. | Social audit |
| **Controls & Audit → Internal Control Plan** | Prepare, approve, implement, and monitor the school control plan. | HA: review/oversee. AP/SO: provide assigned books, reporting, or inventory evidence. DE: link SMC approval evidence. | HA R/A/oversight; AP P/evidence; SO O/evidence; DE E. | Draft, awaiting SMC approval, approved, monitoring due, corrective action open/complete. | Internal control |
| **Controls & Audit → Bank Guarantees** | Record guarantees, issuing-bank verification, and status/history. | AP or assigned school staff: enter details/evidence and follow-up. HA: review verification status. DE: link committee decision evidence if applicable. | AP P; HA R/oversight; SO P only if assigned guarantee duties; DE E only. | Received, verification pending, verified, discrepancy/follow-up, expired/released/closed as recorded. | Bank guarantees |
| **Controls & Audit → Decision Evidence** | Attach and link evidence of required SMC decisions to relevant budget, spending, inventory-transfer, and control records. | DE: create/submit evidence link and attach minutes/decision record. Other users: view linked evidence within access. | DE E; AP/HA/SO R only where permitted by linked workflow; SA no transaction authority. | Evidence needed, submitted for record, linked/verified, incomplete. | Annual budget; expense/payment when committee decision applies; budget transfer; inventory transfer; internal control; other SMC decisions |
| **Settings → Users & Presets** | Maintain school users and assign standard permission presets. | SA: create/edit/disable users and assign presets. No one changes preset definitions here. | SA C; other presets no default access. | Active, disabled, preset assigned; changes attributed. | No financial workflow; supports all workflows through access administration |
| **Settings → School & Fiscal Year** | Maintain school settings and non-accounting fiscal-year/configuration metadata. | SA: update authorized school and fiscal-year settings. | SA C; AP/HA read relevant configuration. | Current fiscal year, setup incomplete, configuration effective/current. | Annual budget; budget release; reporting and fiscal-year workflows |

## Shared record page and lifecycle

Every listed task page opens a shared record detail/history page appropriate to that workflow. It shows the current status, responsible user, dates, supporting evidence, linked approvals/decision evidence, and any related report or book reference. Available actions are permission-filtered; this is not a separate accounting engine or unrestricted record editor.

Use **Draft → Submitted/Review → Approved/Verified → Posted → Locked** where applicable. Returned/incomplete and external-verification states may be shown without skipping required authority. Before posting, permitted users may edit drafts or cancel an unposted submission with a reason. Posted/locked financial records cannot be silently edited or deleted: authorized corrections create a traceable reversal, adjustment, or replacement that preserves the original and its history. Manual-specific cancellation handling—such as retaining a spoiled/cancelled receipt in its booklet and issuing the next receipt—remains in force.

## Official forms and outputs

Do not expose Forms 1–40 as primary navigation. Generate or print the applicable official form from its task page or Report Centre after entering/reviewing the relevant workflow information. Keep required source records and approvals linked; printing a form does not itself approve or post a transaction. Accounting Engine calculations and Account Codes remain background/system behavior surfaced only as needed within permitted task pages.
