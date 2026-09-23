# Roles and Permissions

This is a proposed, small-school permission model derived from `docs/REQUIREMENTS.md`, `docs/MODULES.md`, and `docs/WORKFLOWS.md`. Manual actors below are not automatically software accounts. The product roles and permission boundaries are **security/UX choices**, not additional manual rules. Use the shared transaction lifecycle: posted/locked financial records are not silently edited or deleted; corrections preserve the original through a traceable reversal, adjustment, or replacement.

## Manual actors and non-login participants

The manual assigns responsibilities to the head teacher; accounts staff member/teacher; School Management Committee (SMC); school, store or inventory personnel; travelling staff; and the school. Responsibilities include budget preparation and approval, joint bank signatures, account keeping and reporting, inventory care, audit records, and control plans (for example `SAM-01-012`–`SAM-01-023`, `SAM-04-001`–`SAM-04-011`, `SAM-08-001`–`SAM-08-039`, `SAM-09-001`–`SAM-09-022`). The source requirements specify responsibilities and approvals, not a software role catalogue.

Payers/students/parents, suppliers/payees, banks, local-level or other releasing bodies, donors, auditors, and the public participate in transactions or decisions but do not need product logins in this proposal. The SMC is a collective decision-making body; an authorized member may record its decision in the system, but a member’s login alone does not replace the required committee decision or evidence. Travelling staff and advance recipients can be recorded as named people without an account.

## Proposed login roles

Four role types are sufficient for ordinary school operations. Assign roles to named people; a person may hold more than one role if staffing requires it, but preserve distinct recorded preparer/approver attribution wherever school authority or useful financial control calls for it.

### Accounts preparer

- **Purpose:** Maintain day-to-day accounting records, supporting documents, reconciliations, and reports.
- **Accessible modules/subareas:** Money In; Expenses & Payments (including Payroll, Advances, Deposits, Travel, Petty Cash, and Bank & Reconciliation); Budget & Funding preparation; Reports; read access to Goods & Assets and Controls & Audit; Accounting Engine and Account Codes only through normal transaction use.
- **Permissions (product choice):** Create and view assigned records; edit drafts and returned submissions; submit vouchers, reconciliations, release requests, and reports; record statement details and proposed corrections; export authorized reports. May post only after required approval/verification; posting may be automatic on approval. May cancel drafts or request cancellation of an unposted submission. Cannot directly reverse or edit a posted/locked record; can prepare a reversal/adjustment/replacement for review.
- **Approval responsibilities:** Prepare evidence and statements; obtain and attach the head teacher’s approval/certification for expenditure and financial statements before submission (`SAM-01-021`). Does not approve own transactions merely by being an accounts preparer.
- **Explicitly prohibited (product choice unless separately assigned an authorized role):** Approve own payment, budget transfer, or report; bypass required approval or evidence; alter/delete posted or locked records; change verified account-code definitions or accounting rules.

### Head teacher / authorized approver

- **Purpose:** Exercise delegated school spending, certification, and operational oversight responsibilities.
- **Accessible modules/subareas:** All operational modules, Reports, and Controls & Audit; Account Codes read-only in transaction context. Accounting Engine remains background-only.
- **Permissions (product choice):** View records; create/submit authorized requests and decisions; approve or return transactions within delegated authority; certify statements; authorize permitted cancellation before posting; approve a proposed reversal/adjustment/replacement within authority; export relevant reports. Posting is system-controlled after approval or delegated to the Accounts preparer after approval, not a way to bypass authorization.
- **Approval responsibilities:** Approve spending within delegated allocation and rules (`SAM-01-014`); approve/certify statements before submission with accounts staff preparing them (`SAM-01-021`); give written direction where required documents/formalities are incomplete (`SAM-01-023`); perform the head-teacher part of joint bank operation with accounts staff (`SAM-01-015`, `SAM-02-005`). Route decisions reserved for the SMC to the committee.
- **Explicitly prohibited (product choice):** Approve a matter reserved to the SMC as if it were a head-teacher-only decision; alone satisfy the joint-signature requirement; silently edit/delete posted records; alter code catalogues or accounting rules.

### Store / operational staff

- **Purpose:** Record the physical custody and movement of goods and assets and initiate supported operational requests.
- **Accessible modules/subareas:** Goods & Assets (requisitions, receipt evidence, inventory issues/transfers/inspection); create/view own purchase or expense requests and supporting travel/advance claims as applicable; read-only access to relevant Reports.
- **Permissions (product choice):** Create requisitions, receipt/inspection/issue/transfer records and supporting evidence; view assigned stock and request status; edit drafts or returned entries; submit records for review; export only assigned operational lists. No financial posting or approval unless separately assigned an authorized role. Cancel own unsubmitted drafts; request correction of posted inventory or financial records through traceable adjustment/reversal.
- **Approval responsibilities:** Verify physical receipt, custody, issue, and inspection facts within assigned duties; submit evidence to the authorized approver/accounts preparer. This role does not substitute for a required spending approval.
- **Explicitly prohibited (product choice):** Approve or pay own purchase request; change financial books or approved budget; delete posted inventory/financial history; approve a transfer or write-off outside documented authority.

### SMC decision recorder / reviewer

- **Purpose:** Record and review evidence of collective SMC decisions without treating one member’s login as the committee itself.
- **Accessible modules/subareas:** Budget & Funding (annual/revised budget and transfers); Controls & Audit (control plan, social-audit and meeting records); read-only Reports and decision-related evidence.
- **Permissions (product choice):** View relevant proposals and reports; record or attach committee decisions, meeting minutes, and verification evidence; submit recorded decisions for application by authorized staff; export relevant reports. No routine entry or posting in the ledgers. A designated recorder may prepare the decision record but cannot attest to a collective decision without the required evidence.
- **Approval responsibilities:** Evidence SMC decisions where the manual assigns approval or collective action, including the annual budget/programme, qualifying budget transfers, and internal-control work plan (`SAM-01-012`, `SAM-04-004`, `SAM-06-091`–`SAM-06-093`, `SAM-09-010`–`SAM-09-013`).
- **Explicitly prohibited (product choice):** Make a collective decision alone; post accounting entries; approve payments or certify accounts solely by virtue of this role; edit/delete posted financial records.

## Permission matrix

Cells describe proposed login capabilities, not a change to the manual’s designated authority. “Prepare” means create/edit drafts and submit; “approve” means record the authorized approval/verification; “post” means commit approved entries (or allow automatic posting); “correct” means initiate a traceable reversal/adjustment/replacement, never overwrite history. External participants are not login roles.

| Major workflow | Accounts preparer | Head teacher / authorized approver | Store / operational staff | SMC decision recorder / reviewer |
| --- | --- | --- | --- | --- |
| Fee/income collection; other income | Prepare, verify evidence, submit; post after approval | Approve exceptions/authority as applicable; joint bank authorization | — | Approve income headings where assigned; record decision |
| Expense/payment; payroll | Prepare vouchers, payroll, deductions, evidence; post after approval | Approve within delegated authority; joint bank authorization | Initiate request; attach receipt evidence | Approve only a matter reserved to SMC |
| Advances, deposits, travel, petty cash | Prepare, maintain subsidiary records, submit settlement | Approve issue/payment or travel as delegated | Submit claims/receipts; attest operational facts | — |
| Bank statement/reconciliation | Enter statement, match, explain, prepare adjustment and submit | Review/authorize adjustment as required; joint bank authorization for account operation | — | — |
| Annual budget and budget release | Prepare estimates/requests and supporting account data; submit | Prepare/present budget and approve within assigned authority | Provide operational needs | Record/evidence annual meeting and SMC approval; record committee decision |
| Budget transfer | Prepare calculation and request; apply after required approval | Approve within own authority; refer reserved cases | — | Record/evidence SMC decision where required |
| Procurement, receipt, inventory issue/transfer/inspection | Record financial voucher and books; post after approval | Approve spending within authority | Prepare requisitions and record receipt/custody/movement/inspection | Approve only committee-reserved decision |
| Reports | Prepare, reconcile, submit; export working reports | Review/certify where required; submit/approve as assigned | View relevant operational extracts | Review and retain committee/meeting evidence |
| Audit, beruju, social/internal control, guarantees | Maintain books, finding register and supporting evidence | Arrange audit, respond/authorize action, monitor controls | Supply asset/receipt evidence | Record/evidence committee and annual-meeting decisions; review control-plan evidence |
| Cancel, reverse, adjust, replace | Cancel own draft; prepare correction for approval | Authorize before-posting cancellation or correction within authority | Cancel own draft; request a correction | Record decision evidence if committee authority applies |

## Common boundaries and exceptions

- **Manual requirement:** Joint signatures of the head teacher and accounts staff member/teacher govern operation of the school bank account (`SAM-01-015`); applicable school-fund operation also specifies joint signatures (`SAM-02-005`). A software approval is not a bank signature.
- **Manual requirement:** The head teacher’s responsibilities, accounts staff duties, committee approvals, and supporting evidence remain those recorded in `REQUIREMENTS.md`; the role model cannot transfer them to another login role.
- **Product choice:** Keep preparer, approver, and poster attribution visible. Use separate people for preparation and approval when practical, especially payments and corrections; do not impose a multi-step workflow where no separate authority is required. Where one person has multiple roles, the software must still record which capacity was used and retain approval evidence.
- **Product choice:** Allow cancellation of drafts and unposted submissions with a reason and history. For posted/locked entries, disable edit/delete/cancel; require an authorized, traceable reversal, adjustment, or replacement preserving the original. Keep manual-specific void/cancellation handling, including retaining spoiled/cancelled receipts in their booklet and issuing the next serial receipt.
- **External actors:** Payers, suppliers, banks, local levels, donors/parents, auditors, and the public may provide evidence, receive submissions, verify information, or participate in meetings; they receive no login permissions in this proposal.
