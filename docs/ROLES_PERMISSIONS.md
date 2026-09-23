# Roles and Permissions

This is a proposed, small-school permission model derived from `docs/REQUIREMENTS.md`, `docs/MODULES.md`, and `docs/WORKFLOWS.md`. Manual actors below are not automatically software accounts. The product roles and permission boundaries are **security/UX choices**, not additional manual rules. Use the shared transaction lifecycle: posted/locked financial records are not silently edited or deleted; corrections preserve the original through a traceable reversal, adjustment, or replacement.

## Manual actors and non-login participants

The manual assigns responsibilities to the head teacher; accounts staff member/teacher; School Management Committee (SMC); school, store or inventory personnel; travelling staff; and the school. Responsibilities include budget preparation and approval, joint bank signatures, account keeping and reporting, inventory care, audit records, and control plans (for example `SAM-01-012`–`SAM-01-023`, `SAM-04-001`–`SAM-04-011`, `SAM-08-001`–`SAM-08-039`, `SAM-09-001`–`SAM-09-022`). The source requirements specify responsibilities and approvals, not a software role catalogue.

Payers/students/parents, suppliers/payees, banks, local-level or other releasing bodies, donors, auditors, and the public participate in transactions or decisions but do not need product logins in this proposal. The SMC is a collective decision-making body; an authorized member may record its decision in the system, but a member’s login alone does not replace the required committee decision or evidence. Travelling staff and advance recipients can be recorded as named people without an account.

## Proposed permission presets

These are default permission presets, not hardcoded authorization roles or the manual’s assignment of legal authority. Assign only the operational capabilities needed to each named login and combine presets where school staffing requires it. Manual-designated responsibilities still determine who may authorize an action. The product must retain preparer/approver attribution and enforce distinct-authority rules described below.

### Accounts preparer preset

- **Purpose:** Maintain day-to-day accounting records, supporting documents, reconciliations, and reports.
- **Accessible modules/subareas:** Money In; Expenses & Payments (including Payroll, Advances, Deposits, Travel, Petty Cash, and Bank & Reconciliation); Budget & Funding preparation; Reports; read access to Goods & Assets and Controls & Audit; Accounting Engine and Account Codes only through normal transaction use.
- **Permissions (product choice):** Create and view assigned records; edit drafts and returned submissions; submit vouchers, reconciliations, release requests, and reports; record statement details and proposed corrections; export authorized reports. May post only after required approval/verification; posting may be automatic on approval. May cancel drafts or request cancellation of an unposted submission. Cannot directly reverse or edit a posted/locked record; can prepare a reversal/adjustment/replacement for review.
- **Approval responsibilities:** Prepare evidence and statements; obtain and attach the head teacher’s approval/certification for expenditure and financial statements before submission (`SAM-01-021`). Does not approve own transactions merely by being an accounts preparer.
- **Explicitly prohibited (product choice unless separately assigned an authorized role):** Approve own payment, budget transfer, or report; bypass required approval or evidence; alter/delete posted or locked records; change verified account-code definitions or accounting rules.

### Head Teacher / Approver preset

- **Purpose:** Provide oversight, approval, certification, and review according to the head teacher’s documented authority.
- **Accessible modules/subareas:** All operational modules, Reports, and Controls & Audit; Account Codes read-only in transaction context. Accounting Engine remains background-only.
- **Permissions (product choice):** View and review records; approve or return transactions within delegated authority; certify statements; authorize permitted cancellation before posting; approve a proposed reversal/adjustment/replacement within authority; export relevant reports. This preset does not grant broad transaction create/edit/submit or posting powers by default; those entry capabilities may be assigned through another preset. Posting is system-controlled after approval or performed by an authorized posting preset after approval, never as a substitute for authorization.
- **Approval responsibilities:** Approve spending within delegated allocation and rules (`SAM-01-014`); approve/certify statements before submission with accounts staff preparing them (`SAM-01-021`); give written direction where required documents/formalities are incomplete (`SAM-01-023`); perform the head-teacher part of joint bank operation with accounts staff (`SAM-01-015`, `SAM-02-005`). Route decisions reserved for the SMC to the committee.
- **Explicitly prohibited (product choice):** Approve a matter reserved to the SMC as if it were a head-teacher-only decision; alone satisfy the joint-signature requirement; silently edit/delete posted records; alter Accounting Engine rules or verified Account Code definitions.

### Store / Operational Staff preset

- **Purpose:** Record the physical custody and movement of goods and assets and initiate supported operational requests.
- **Accessible modules/subareas:** Goods & Assets (requisitions, receipt evidence, inventory issues/transfers/inspection); create/view own purchase or expense requests and supporting travel/advance claims as applicable; read-only access to relevant Reports.
- **Permissions (product choice):** Create requisitions, receipt/inspection/issue/transfer records and supporting evidence; view assigned stock and request status; edit drafts or returned entries; submit records for review; export only assigned operational lists. No financial posting or approval unless separately assigned an authorized role. Cancel own unsubmitted drafts; request correction of posted inventory or financial records through traceable adjustment/reversal.
- **Approval responsibilities:** Verify physical receipt, custody, issue, and inspection facts within assigned duties; submit evidence to the authorized approver/accounts preparer. This role does not substitute for a required spending approval.
- **Explicitly prohibited (product choice):** Approve or pay own purchase request; change financial books or approved budget; delete posted inventory/financial history; approve a transfer or write-off outside documented authority.

### SMC Decision Evidence preset

- **Purpose:** Link evidence of collective SMC decisions to relevant records without treating one member’s login as the committee itself.
- **Accessible modules/subareas:** A narrow **Decision Evidence** capability across modules, including Budget & Funding, spending/payment records, inventory transfers, internal control, and meeting records; view the linked proposal/record and evidence only.
- **Permissions (product choice):** Create, view, and submit decision-evidence links and attach or view minutes/decision evidence for the related record; export linked evidence where authorized. No permission to edit the underlying transaction, approve or post it, change its status, or cancel/reverse it. A designated recorder cannot attest to a collective decision without the required evidence.
- **Approval responsibilities:** Record evidence of SMC decisions where required, including annual budget/programme approval, qualifying budget transfers, and internal-control work-plan approval (`SAM-01-012`, `SAM-04-004`, `SAM-06-091`–`SAM-06-093`, `SAM-09-008`). `SAM-09-010`–`SAM-09-013` specify internal-control plan scope and reporting/reliability provisions, not SMC approval.
- **Explicitly prohibited (product choice):** Make a collective decision alone; edit, submit, approve, post, cancel, reverse, or alter underlying financial/inventory transactions; approve payments or certify accounts solely by virtue of this preset.

### School Administrator preset

- **Purpose:** Administer ordinary school-level software settings and user access without acquiring accounting authority.
- **Accessible modules/subareas:** User and preset assignment management; school settings; fiscal-year and non-accounting configuration administration; non-financial administration needed to operate the school instance.
- **Permissions (product choice):** Create, view, edit, disable, and assign users to standard permission presets; maintain school settings and fiscal-year/non-accounting configuration metadata; export administrative lists where appropriate. May not change the permission preset definitions. No access to transaction approval/posting/reversal by virtue of administrator status.
- **Approval responsibilities:** None for financial, budget, inventory, or compliance transactions unless separately assigned an applicable operational preset and authorized by the school.
- **Explicitly prohibited (product choice):** Financial approve, post, cancel, reverse, or transaction-edit powers solely from this preset; alter Accounting Engine rules or verified Account Code definitions. Authority for accounting rule/version configuration will be defined separately.

## Permission matrix

Cells describe proposed login capabilities, not a change to the manual’s designated authority. “Prepare” means create/edit drafts and submit; “approve” means record the authorized approval/verification; “post” means commit approved entries (or allow automatic posting); “correct” means initiate a traceable reversal/adjustment/replacement, never overwrite history. External participants are not login roles.

| Major workflow | Accounts preparer preset | Head Teacher / Approver preset | Store / Operational Staff preset | SMC Decision Evidence preset | School Administrator preset |
| --- | --- | --- | --- | --- | --- |
| Fee/income collection; other income | Prepare, verify evidence, submit; post after approval | Approve within authority; joint bank authorization | — | Link decision evidence if required; no transaction action | No financial transaction authority |
| Expense/payment; payroll | Prepare vouchers, payroll, deductions, evidence; post after approval | Approve within delegated authority; joint bank authorization | Initiate request; attach receipt evidence | Link required SMC decision evidence; no transaction action | No financial transaction authority |
| Advances, deposits, travel, petty cash | Prepare, maintain subsidiary records, submit settlement | Review/approve within delegated authority | Submit claims/receipts; attest operational facts | Link decision evidence if required; no transaction action | No financial transaction authority |
| Bank statement/reconciliation | Enter statement, match, explain, prepare adjustment and submit | Review/authorize adjustment as required; joint bank authorization for account operation | — | — | No financial transaction authority |
| Annual budget and budget release | Prepare estimates/requests and supporting account data; submit | Prepare/present annual budget; review release matters as authorized, but not in place of required SMC approval | Provide operational needs | Link evidence of annual meeting and SMC budget approval | No financial transaction authority |
| Budget transfer | Prepare calculation and request; apply after required approval | Approve within own authority; refer reserved cases | — | Link required committee decision evidence; no transaction action | No financial transaction authority |
| Procurement, receipt, inventory issue/transfer/inspection | Record financial voucher and books; post after approval | Review/approve spending within authority | Prepare requisitions and record receipt/custody/movement/inspection | Link required decision evidence, including committee-approved transfer; no transaction action | No financial transaction authority |
| Reports | Prepare, reconcile, submit; export working reports | Review/certify where required; submit/approve as assigned | View relevant operational extracts | View/link authorized decision evidence | Export administrative lists only |
| Audit, beruju, social/internal control, guarantees | Maintain books, finding register and supporting evidence | Arrange audit, respond/authorize action, monitor controls | Supply asset/receipt evidence | Link SMC decision evidence, including internal-control-plan approval; no transaction action | No financial transaction authority |
| Cancel, reverse, adjust, replace | Cancel own draft; prepare correction for approval | Authorize before-posting cancellation or correction within authority | Cancel own draft; request a correction | Link required decision evidence only | No cancellation, reversal, or transaction-edit authority |

## Common boundaries and exceptions

- **Manual requirement:** Joint signatures of the head teacher and accounts staff member/teacher govern operation of the school bank account (`SAM-01-015`); applicable school-fund operation also specifies joint signatures (`SAM-02-005`). A software approval is not a bank signature.
- **Manual requirement:** The head teacher’s responsibilities, accounts staff duties, committee approvals, and supporting evidence remain those recorded in `REQUIREMENTS.md`; the role model cannot transfer them to another login role.
- **Manual requirement:** The head teacher prepares and presents the annual budget/programme (`SAM-01-013`, `SAM-04-001`–`SAM-04-004`); the required SMC decision approves it, and its evidence is linked to the budget (`SAM-01-012`, `SAM-04-004`).
- **Manual requirement:** SMC approval of the internal-control work plan is explicitly required by `SAM-09-008`. `SAM-09-010`–`SAM-09-013` define plan scope, recordkeeping, report timeliness, and report reliability, not additional approval requirements.
- **Product choice:** Where a workflow requires a distinct authority, a person may not approve a record they prepared merely because they hold both the preparer and approver presets. The software must block self-approval and preserve attribution. Any future small-school exception requires an explicit authorized policy and an audit-logged exception; no such exception is granted by this model.
- **Product choice:** Keep preparer, approver, and poster attribution visible. Use separate people where the manual requires distinct authority or where it is a useful control; do not add an unnecessary approval stage where no separate authority is required. Combining presets does not remove the self-approval rule.
- **Product choice:** No ordinary school preset, including School Administrator, may directly alter Accounting Engine rules or verified Account Code definitions. Accounting rule/version configuration authority will be defined separately.
- **Product choice:** Allow cancellation of drafts and unposted submissions with a reason and history. For posted/locked entries, disable edit/delete/cancel; require an authorized, traceable reversal, adjustment, or replacement preserving the original. Keep manual-specific void/cancellation handling, including retaining spoiled/cancelled receipts in their booklet and issuing the next serial receipt.
- **External actors:** Payers, suppliers, banks, local levels, donors/parents, auditors, and the public may provide evidence, receive submissions, verify information, or participate in meetings; they receive no login permissions in this proposal.
