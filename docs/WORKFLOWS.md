# User Workflows

These concise workflows group obligations already verified in `docs/REQUIREMENTS.md` and assigned to product areas in `docs/MODULES.md`. They do not add accounting rules. **Manual** marks a requirement supported by the cited IDs. The numbered user steps are a proposed UX order for carrying out those obligations; **UX choice** marks proposed system assistance and exception handling. Where the manual prescribes order, timing, approval, or evidence, that requirement is stated explicitly.

## Shared transaction lifecycle and corrections

**UX/system design choice (not a manual-prescribed workflow):** Use Draft → Submitted/Review → Approved/Verified → Posted → Locked as a common lifecycle where appropriate. Do not silently edit or delete posted financial records. Correct them with a traceable reversal, adjustment, or replacement that preserves the original record and its history. This does not replace manual-specific cancellation rules: for example, retain a spoiled or cancelled receipt in its booklet and issue the next receipt.

**Cross-cutting manual authorization:** For operation of the school bank account, require the joint signatures of the head teacher and accounts staff member/teacher (`SAM-01-015`). This applies to bank/payment activity and is not a bank-reconciliation rule.

## Money In

### Fee and cash income collection

- **Purpose:** Receive student fees and other cash income under approved income headings and retain a traceable receipt.
- **Supported actors:** Accounts staff/teacher; student or other payer; School Management Committee approves income headings.
- **Starting condition:** A fee or other cash income is due under an approved heading.
- **User steps (UX order over manual duties):** 1. Select the applicable income heading and record the payer, purpose, amount, and receipt details. 2. Issue the cash/receipt receipt in serial order and give the payer copy. 3. Attach the retained receipt copy to the income voucher and deposit the received money in the bank the same day, or the next day if same-day deposit is not possible. 4. Update the receipt-control and monthly income accounts.
- **Automatic actions (UX choice):** Allocate the next receipt/voucher numbers, carry receipt data into the voucher and account, and show the monthly heading totals.
- **Approvals / verification (Manual):** Use headings approved by the School Management Committee; complete all required receipt-control details.
- **Records/books/reports affected (Manual):** Cash/receipt receipt (Form 3); receipt-control account (Form 4); income general voucher (Form 5); monthly and annual income accounts (Forms 6–7); fee register (Form 8).
- **Exception / correction path:** **Manual:** Keep a spoiled or cancelled receipt in its booklet and issue the next receipt; at year end mark unused receipts and use newly numbered receipts in the next year. **UX choice:** Preserve the cancelled receipt reference and show the replacement receipt link.
- **Completion state:** Receipt issued and retained; bank deposit, voucher, receipt-control entry, and monthly income entry are traceable.
- **Related requirement IDs:** `SAM-06-007`, `SAM-06-010`–`SAM-06-027`, `SAM-06-028`, `SAM-06-019`–`SAM-06-021`, `SAM-10-003`–`SAM-10-008`, `SAM-FORM-03`–`SAM-FORM-08`, `SAM-ANN-01-14223`, `SAM-ANN-01-14229`.

### Other income and bank receipts

- **Purpose:** Record non-fee income and income received through a bank, including grants, rent, sales, donations, and other listed income sources.
- **Supported actors:** Accounts staff/teacher; head teacher; payer or granting body; relevant bank.
- **Starting condition:** A bank voucher/statement or other evidence shows income received, or income for the fiscal year is earned but not yet received.
- **User steps (UX order over manual duties):** 1. Identify the source, date, amount, and applicable income heading. 2. Match bank receipts to the bank voucher or statement; record earned but not yet received income as receivable. 3. Raise the income voucher and attach the bank voucher or statement. 4. Post the receipt by heading to the monthly income account and, at year end, prepare the annual income account.
- **Automatic actions (UX choice):** Suggest the matching income code from the manual catalogue, flag a possible duplicate bank receipt, and update the income and receivable balances after staff confirmation.
- **Approvals / verification (Manual):** Verify the source evidence and record each receipt under the related approved heading; income headings and amounts must follow the manual's classifications.
- **Records/books/reports affected (Manual):** Income general voucher (Form 5); monthly/annual income accounts (Forms 6–7); receipt-control account where applicable (Form 4); bank cash book (Form 12); relevant income code in Annex 1.
- **Exception / correction path:** **Manual:** If the amount is earned but not yet received, record an income receivable; use the source bank voucher/statement as the basis for a bank receipt. **UX choice:** Keep an unmatched receipt pending review with its evidence reference; record corrections as traceable adjustments.
- **Completion state:** Bank/source evidence, income heading, voucher, and monthly/annual account entry agree or the receivable remains identified.
- **Related requirement IDs:** `SAM-02-001`–`SAM-02-008`, `SAM-06-008`, `SAM-06-009`, `SAM-06-018`, `SAM-06-021`–`SAM-06-026`, `SAM-06-029`, `SAM-10-004`–`SAM-10-007`, `SAM-FORM-04`–`SAM-FORM-07`, `SAM-ANN-01-13311`, `SAM-ANN-01-13312`, `SAM-ANN-01-13313`, `SAM-ANN-01-14119`, `SAM-ANN-01-14121`, `SAM-ANN-01-14151`, `SAM-ANN-01-14211`–`SAM-ANN-01-14213`, `SAM-ANN-01-14223`, `SAM-ANN-01-14229`, `SAM-ANN-01-14312`, `SAM-ANN-01-14411`, `SAM-ANN-01-14421`, `SAM-ANN-01-15111`–`SAM-ANN-01-15113`, `SAM-ANN-04-010`.

## Expenses & Payments

### Expense and payment

- **Purpose:** Record and pay an approved school expense with the required support and budget heading.
- **Supported actors:** Requesting staff member; authorized spending officer; accounts staff/teacher; head teacher; supplier/payee.
- **Starting condition:** An expense is proposed under an approved budget/programme and supporting evidence is available or an expenditure obligation has arisen.
- **User steps (UX order over manual duties):** 1. Select the budget/expenditure heading and confirm delegated authority and available allocation. 2. Attach the approved order, bill, payment voucher, and other required evidence. 3. For purchased goods, include the purchase order and receipt/entry report. 4. Raise the expenditure general voucher, record the transaction in the monthly expenditure account and bank cash book, and make payment through the bank by account-payee cheque where procurement is involved.
- **Automatic actions (UX choice):** Check the selected heading against approved allocation; prompt for required attachments; number the voucher and post the confirmed entry to related books. Do not silently create an accounting treatment not stated in the requirements.
- **Approvals / verification (Manual):** Obtain approval/order from the officer with spending authority before spending; stay within approved budget and legal requirements. Attach evidence in order. Head teacher certifies paid bills/vouchers using the required paid stamp.
- **Records/books/reports affected (Manual):** Expenditure general voucher (Form 9); monthly/annual expenditure accounts (Forms 10–11); bank cash book (Form 12); budget account (Form 13); expenditure statement (Form 14); supporting documents and payment record.
- **Exception / correction path:** **Manual:** Do not exceed an expenditure heading allocation; withhold taxes required by prevailing rules; show an arisen obligation as a payment liability if its bill/payment voucher has not yet arrived. **UX choice:** Leave incomplete submissions in a review state with the missing evidence/authority identified; retain corrections and attribution.
- **Completion state:** Approved and supported voucher is recorded under the proper heading, payment is traceable through the bank, and related books reflect the entry.
- **Related requirement IDs:** `SAM-01-014`, `SAM-03-003`, `SAM-03-004`, `SAM-06-030`–`SAM-06-047`, `SAM-06-037`–`SAM-06-040`, `SAM-10-009`–`SAM-10-011`, `SAM-11-006`, `SAM-11-015`, `SAM-11-016`, `SAM-FORM-09`–`SAM-FORM-11`, `SAM-ANN-04-003`, `SAM-ANN-04-008`, `SAM-ANN-04-011`.

### Payroll

- **Purpose:** Request salary funding, record payroll, pay teachers/staff, and account for required deductions and remittances.
- **Supported actors:** Accounts staff/teacher; head teacher; teachers/staff; local level; bank; Inland Revenue Office; Employees Provident Fund or relevant fund.
- **Starting condition:** Salary period is due, approved salary records are available, and a release or budget balance is available.
- **User steps (UX order over manual duties):** 1. Prepare the teacher salary request and staff/amount details for the monthly or four-monthly release request. 2. Verify the salary report approval and calculate applicable pay and deductions under the configured rule version. 3. Raise the expenditure voucher, pay staff through bank accounts, and record each deduction. 4. Deposit withheld amounts under the prescribed heading and send required vouchers, letters, and annual withholding details to the appropriate body.
- **Automatic actions (UX choice):** Compute payroll totals and configured deductions, reconcile totals to the voucher, and produce remittance summaries. Preserve the rule version used; the manual’s historical tax rates/percentages are not silently replaced.
- **Approvals / verification (Manual):** Salary report approval evidence is attached; approved salary request is used; statutory deductions and remittances follow the applicable manual/law requirements.
- **Records/books/reports affected (Manual):** Teacher Salary Request Form (Form 2); expenditure voucher and accounts (Forms 9–11); bank cash book (Form 12); payroll/salary details; withholding and fund remittance records.
- **Exception / correction path:** **Manual:** Do not pay salary without the required salary-report approval proof; withhold and remit according to the stated applicable rules. **UX choice:** Stop submission when payroll totals do not balance, and route mismatched deductions for review without altering historical payroll entries.
- **Completion state:** Staff payments and each deduction/remittance are recorded with approval evidence and a matching voucher.
- **Related requirement IDs:** `SAM-05-004`, `SAM-05-005`, `SAM-06-037`, `SAM-06-041`, `SAM-10-002`, `SAM-10-009`–`SAM-10-012`, `SAM-11-007`–`SAM-11-012`, `SAM-FORM-02`, `SAM-FORM-09`–`SAM-FORM-12`, `SAM-ANN-04-004`.

### Advances

- **Purpose:** Issue an authorized advance, track it by recipient, and settle it against submitted bills/receipts.
- **Supported actors:** Accounts staff/teacher; head teacher or authorized officer; teacher/staff member, person, or institution receiving the advance.
- **Starting condition:** A decision or rule authorizes an advance for purchasing goods, construction, or other work.
- **User steps (UX order over manual duties):** 1. Record recipient, purpose, amount, authority, and voucher. 2. Pay through the bank and open/update a separate subsidiary-account folio for that recipient. 3. On settlement, enter the submitted bill/receipt report and clear the advance according to the source records. 4. Include outstanding balances in the monthly settlement schedule.
- **Automatic actions (UX choice):** Maintain the recipient balance, link each settlement to its advance, and show outstanding amounts in the schedule and bank cash book.
- **Approvals / verification (Manual):** Advance must be made under a decision or rule; settlement follows rules and is supported by submitted documents.
- **Records/books/reports affected (Manual):** General voucher; advance subsidiary account (Form 18); schedule of advances pending settlement (Form 15); bank cash book (Form 12); purchase order/receipt report where the advance funded a purchase (Forms 30–31).
- **Exception / correction path:** **Manual:** Record the advance and its settlement in the same recipient’s folio; report unsettled balances. **UX choice:** Keep unsupported or partial settlement amounts outstanding and request review rather than silently closing the folio.
- **Completion state:** Each advance is either supported as settled or remains listed with its outstanding balance and recipient.
- **Related requirement IDs:** `SAM-06-058`–`SAM-06-060`, `SAM-06-067`–`SAM-06-070`, `SAM-10-015`, `SAM-10-018`, `SAM-FORM-15`, `SAM-FORM-18`, `SAM-ANN-04-009`, `SAM-ANN-04-012`.

### Deposits

- **Purpose:** Record security or other deposits, track each depositor, and refund or report balances under the stated rules.
- **Supported actors:** Accounts staff/teacher; head teacher/authorized officer; depositor or contractor; bank; relevant tax office where a deduction is due.
- **Starting condition:** A deposit is received, refunded, or remains in the school’s deposit account.
- **User steps (UX order over manual duties):** 1. Record receipt in a general voucher and the general and individual deposit accounts. 2. Maintain one individual account for each person or institution. 3. When work is complete or the period ends, verify entitlement and refund under the rules. 4. Prepare the monthly deposit statement from the bank statement when a balance remains.
- **Automatic actions (UX choice):** Update each depositor balance, compare account and bank totals, and list due refunds and long-standing balances for review.
- **Approvals / verification (Manual):** Do not use held deposits for other work; refund to the relevant depositor according to rules after work/period completion. State reasons for bank/account differences.
- **Records/books/reports affected (Manual):** General vouchers; general deposit account (Form 19); individual deposit account (Form 20); deposit financial statement (Form 21); bank cash book and bank statement.
- **Exception / correction path:** **Manual:** If an old deposit is unclaimed or the payee cannot be identified, follow the prescribed legal process before recognizing it as income and depositing it to the school fund. **UX choice:** Flag it as unresolved and preserve the legal-process evidence.
- **Completion state:** Receipt/refund is recorded, depositor balance is current, and monthly statement agrees with or explains the bank balance.
- **Related requirement IDs:** `SAM-06-071`–`SAM-06-081`, `SAM-10-019`–`SAM-10-021`, `SAM-FORM-19`–`SAM-FORM-21`.

### Travel

- **Purpose:** Authorize official school travel, document work completed, and settle eligible travel costs.
- **Supported actors:** Travelling teacher/staff/office holder; head teacher or authorized approving officer; accounts staff/teacher.
- **Starting condition:** School work requires travel to a relevant body or office and funds are available for eligible expenses.
- **User steps (UX order over manual duties):** 1. Obtain approval and record the travel order before travel. 2. After return and reporting to school, prepare the travel report and daily/travel-expense bill. 3. Attach the report to the claim and verify budget availability before payment. 4. For vehicle fuel expenditure, attach a completed logbook certified by the authorized officer.
- **Automatic actions (UX choice):** Carry travel-order details into the claim and flag missing prior approval, report, logbook, or budget balance.
- **Approvals / verification (Manual):** Travel order is approved before travel; vehicle user completes the logbook for every use and authorized officer certifies it; payment requires available budget balance.
- **Records/books/reports affected (Manual):** Travel order (Form 22); daily/travel expense bill (Form 23); travel report; vehicle logbook; expenditure voucher/accounts.
- **Exception / correction path:** **Manual:** Do not authorize travel without approval or pay travel costs without allocated budget and balance; submit report after travel. **UX choice:** Return an incomplete claim for completion while preserving the original order and submitted documents.
- **Completion state:** Approved travel has an order, work report, expense bill, supporting logbook if applicable, and a traceable payment.
- **Related requirement IDs:** `SAM-06-082`–`SAM-06-085`, `SAM-10-022`, `SAM-10-023`, `SAM-11-013`, `SAM-11-014`, `SAM-11-017`, `SAM-11-018`, `SAM-FORM-22`, `SAM-FORM-23`.

### Petty cash

- **Purpose:** Keep a fixed petty-cash fund available for small daily expenditure and replenish it after use.
- **Supported actors:** Petty-cash custodian/accounts staff; head teacher or authorized officer.
- **Starting condition:** The school has set the initial petty-cash amount and a small daily expenditure is approved.
- **User steps (UX order over manual duties):** 1. Record each small expenditure with its support and related heading. 2. Maintain the fund statement and balance. 3. After funds are spent, request reimbursement to replenish the fund.
- **Automatic actions (UX choice):** Show the fund balance and aggregate supported expenditure for a replenishment request.
- **Approvals / verification (Manual):** Set a fixed initial amount; replenish on request after expenditure; comply with the applicable school arrangements.
- **Records/books/reports affected (Manual):** Petty-cash fund statement (Form 24); expenditure voucher and bank cash book; source bills/receipts.
- **Exception / correction path:** **Manual:** The manual specifies replenishment after spending. **UX choice:** Keep unsupported expenditure separate for review and preserve each replenishment as a new traceable entry.
- **Completion state:** Petty-cash expenditure is supported and recorded, with the fund replenished or its remaining balance visible.
- **Related requirement IDs:** `SAM-06-086`, `SAM-06-087`, `SAM-10-024`, `SAM-FORM-24`.

### Bank reconciliation

- **Purpose:** Compare the monthly bank statement with the bank cash book, explain differences, and record required school-account adjustments.
- **Supported actors:** Accounts staff/teacher; head teacher; bank.
- **Starting condition:** Monthly bank statement is obtained for the school account.
- **User steps (UX order over manual duties):** 1. Enter or verify statement transactions and closing balance. 2. Compare the statement with the bank cash book. 3. Review unmatched items, state reasons for differences, and submit required account adjustments. 4. Prepare the reconciliation statement and send it to the relevant body when required.
- **Automatic actions (UX choice):** Match likely corresponding entries, calculate the difference, and update ledger balances only from confirmed transactions/adjustments. Staff enter statement information and handle exceptions.
- **Approvals / verification (Manual):** Obtain a bank statement monthly; reconcile and prepare the statement monthly; clearly state reasons for differences and adjust the school account.
- **Records/books/reports affected (Manual):** Bank statement; bank cash book (Form 12); bank-reconciliation statement (Form 16); monthly report to the relevant body.
- **Exception / correction path:** **Manual:** State the reason for any difference and adjust the school account. **UX choice:** Keep each unmatched amount in an exception list until a staff member records its explanation or confirmed adjustment; preserve the prior reconciliation.
- **Completion state:** Statement and cash-book balances are reconciled, differences are explained/adjusted, and the reconciliation statement is retained/submitted.
- **Related requirement IDs:** `SAM-02-009`, `SAM-06-048`–`SAM-06-050`, `SAM-06-061`–`SAM-06-063`, `SAM-10-016`, `SAM-FORM-12`, `SAM-FORM-16`.

## Budget & Funding

### Annual budget

- **Purpose:** Prepare and obtain approval for the coming fiscal year’s income and expenditure budget and programme.
- **Supported actors:** Head teacher; accounts staff/teacher; School Management Committee; donors/parents at the annual meeting.
- **Starting condition:** Annual planning begins for the coming fiscal year, using prior actual and current revised figures.
- **User steps (UX order over manual duties):** 1. Hold the annual donors/parents meeting and present the preceding academic year’s income and expenditure. 2. Prepare and present the next fiscal year’s budget and programme for approval at that annual meeting and by the School Management Committee. 3. Identify expected internal and external income and required recurrent/capital expenditure; enter estimates by the manual’s headings using preceding actuals and current revised amounts. 4. Check that estimated expenditure does not exceed estimated income. 5. Complete committee approval by the end of Ashar and send the approved form to the local level.
- **Automatic actions (UX choice):** Calculate totals and variances, compare income and expenditure, and highlight missing headings or a deficit before submission.
- **Approvals / verification (Manual):** The School Management Committee holds the annual donors/parents meeting, presents the preceding academic year’s income and expenditure, and approves the next fiscal year’s annual budget/programme (`SAM-01-012`); the head teacher prepares and presents the budget/programme on time (`SAM-01-013`).
- **Records/books/reports affected (Manual):** Annual Budget Form (Form 1); approved budget/programme; budget account (Form 13); supporting prior-year actual and current-year revised figures.
- **Exception / correction path:** **Manual:** If a new heading/programme arises or an approved amount is insufficient, prepare and obtain approval for a revised annual budget. **UX choice:** Keep revisions as dated versions with the approving decision linked.
- **Completion state:** Approved budget/programme is retained and submitted; income and spending headings have approved estimates.
- **Related requirement IDs:** `SAM-01-012`, `SAM-01-013`, `SAM-03-001`–`SAM-03-004`, `SAM-04-001`–`SAM-04-011`, `SAM-10-001`, `SAM-11-001`, `SAM-11-002`, `SAM-FORM-01`.

### Budget release

- **Purpose:** Request monthly or four-monthly release of approved school funding and retain the local-level release notice.
- **Supported actors:** Head teacher/accounts staff; local level; relevant approving/releasing body.
- **Starting condition:** Approved annual budget/programme exists and a release period is due under local-level guidance.
- **User steps (UX order over manual duties):** 1. Select the relevant grant and release period. 2. Prepare the request using the local level’s format and attach the required materials for that request period. 3. For salary release, include the teacher/staff list and monthly amount form. 4. Submit to the local level; record the resulting release and retain the notice.
- **Automatic actions (UX choice):** Show period-specific document requirements, total the requested release, and carry an approved release into the budget account by heading.
- **Approvals / verification (Manual):** Follow current instructions of the local level/competent body; first four-month request includes approved budget and prior-year income/expenditure details; second and third include expenditure through preceding month; third also includes prior-year audit report.
- **Records/books/reports affected (Manual):** Budget Release Request Letter (Form 39); Teacher Salary Request (Form 2); authority/release letters (Forms 38 and 40); bank voucher/statement; budget account (Form 13).
- **Exception / correction path:** **Manual:** If the local level prescribes its own format or later instructions, use and follow them. **UX choice:** Keep each request distinct by period and identify omitted supporting documents before submission.
- **Completion state:** Request and attachments are retained; received release is recorded under the correct heading and notice is filed.
- **Related requirement IDs:** `SAM-05-001`–`SAM-05-010`, `SAM-06-051`–`SAM-06-055`, `SAM-10-002`, `SAM-10-038`–`SAM-10-040`, `SAM-FORM-02`, `SAM-FORM-38`–`SAM-FORM-40`, `SAM-ANN-04-001`, `SAM-ANN-04-005`.

### Budget transfer

- **Purpose:** Move an amount between expenditure headings when the approved budget position requires it.
- **Supported actors:** Head teacher; School Management Committee; accounts staff/teacher.
- **Starting condition:** An approved heading has insufficient funds and one or more other headings have a surplus.
- **User steps (UX order over manual duties):** 1. Enter source and destination headings, amounts, and reason. 2. Check whether the transfer is within the head teacher’s authority or requires committee decision. 3. Obtain the required approval before applying the transfer. 4. Update budget records and retain the decision.
- **Automatic actions (UX choice):** Calculate the transfer percentage and prevent posting until the proper authority is recorded.
- **Approvals / verification (Manual):** Head teacher may transfer up to 20 percent from one heading to another; larger transfers or recurrent-to-capital transfers require School Management Committee decision; capital-to-recurrent transfer is prohibited.
- **Records/books/reports affected (Manual):** Approved budget and budget account (Form 13); amended budget/programme and committee decision where required.
- **Exception / correction path:** **Manual:** Reject a prohibited capital-to-recurrent transfer; refer transfers over the limit or from recurrent to capital to the committee. **UX choice:** Preserve a rejected request and its reason for audit.
- **Completion state:** Permitted transfer is approved, posted to budget headings, and traceable to the authority; prohibited request remains unposted.
- **Related requirement IDs:** `SAM-06-091`–`SAM-06-093`, `SAM-04-011`, `SAM-FORM-01`, `SAM-FORM-13`.

## Goods & Assets

### Procurement and goods receipt

- **Purpose:** Request and purchase goods with proper authority and record goods received into the school inventory.
- **Supported actors:** Requester; authorized purchasing officer; head teacher; accounts staff/teacher; store/inventory staff; supplier.
- **Starting condition:** Goods are needed and the school has an approved budget/programme and available allocation.
- **User steps (UX order over manual duties):** 1. Complete a requisition and obtain authorized approval. 2. For a market purchase, prepare the purchase order and obtain written approval before ordering. 3. Give the supplier two purchase-order copies and retain the school copy. 4. On delivery or receipt by transfer/donation/government, inspect the goods, prepare a receipt/entry report, and record the goods in the applicable inventory account. 5. Attach the purchase order, supplier bill, receipt/entry report, and supporting records to payment materials.
- **Automatic actions (UX choice):** Assign sequential requisition/order/receipt numbers, prompt for required copies and evidence, and update the appropriate inventory balance once the receipt is confirmed.
- **Approvals / verification (Manual):** Use only appropriately registered firms/businesses holding a PAN for purchases/services; obtain requisition and written purchase-order approval; prepare the purchase order in triplicate; record all received items, including non-purchase receipts.
- **Records/books/reports affected (Manual):** Requisition Form (Form 29); Purchase Order (Form 30); Receipt/Entry Report (Form 31); stock account (Form 32 or 33); expenditure voucher (Form 9); payment register and supplier documents.
- **Exception / correction path:** **Manual:** Goods received by transfer require head teacher certification, a copy to the provider, and a retained copy; sequence orders and entry reports from number 1 each fiscal year. **UX choice:** Keep short-delivery/damaged-goods discrepancies pending confirmation and preserve the original order and receipt evidence.
- **Completion state:** Authorized order and actual receipt are documented, stock is posted to the right account, and payment support is complete.
- **Related requirement IDs:** `SAM-06-039`, `SAM-06-040`, `SAM-08-019`–`SAM-08-026`, `SAM-10-009`, `SAM-10-029`–`SAM-10-031`, `SAM-11-006`, `SAM-FORM-09`, `SAM-FORM-29`–`SAM-FORM-31`, `SAM-ANN-04-002`, `SAM-ANN-04-006`, `SAM-ANN-04-007`.

### Inventory issue, transfer, and inspection

- **Purpose:** Keep separate consumable/non-consumable stock records, document issues and transfers, and inspect assets.
- **Supported actors:** Store/inventory staff; requesting staff; head teacher; School Management Committee; senior teacher designated for inspection.
- **Starting condition:** Goods are in stock for issue, an inter-organization transfer is proposed/received, or annual inspection/reporting is due.
- **User steps (UX order over manual duties):** 1. Record a non-consumable issue in its subsidiary account or a consumable movement in that year’s consumable account. 2. For a transfer, obtain the School Management Committee decision, prepare a transfer form, state physical condition, and record both sides. 3. After year end, prepare stock/condition statements and conduct required physical inspection. 4. Maintain land/building and fixed-asset cost/identity records.
- **Automatic actions (UX choice):** Update item balances after confirmed issue/transfer, carry remaining consumable stock as the next year’s opening balance, and compile quantities and values for annual reports.
- **Approvals / verification (Manual):** School Management Committee decision precedes transfer; head teacher certifies receipt of transferred inventory; head teacher designates a senior teacher in writing for inspection within the stated period; inspection checks actual quantity and condition.
- **Records/books/reports affected (Manual):** Non-consumable inventory account (Form 32); consumable inventory account (Form 33); land/building cost book (Form 34); transfer form (Form 35); annual stock statement (Form 36); inventory inspection form/report (Form 37); fixed-asset register.
- **Exception / correction path:** **Manual:** Record physical condition and report shortfall/excess or condition found by inspection; protect assets, repair when appropriate, and follow legal process for assets unusable after repair. **UX choice:** Flag quantity/condition differences for review and preserve the inspection finding with any later correction.
- **Completion state:** Issue/transfer entries balance to stock records and required annual inspection and asset records are completed and submitted.
- **Related requirement IDs:** `SAM-08-001`–`SAM-08-018`, `SAM-08-027`–`SAM-08-039`, `SAM-10-032`–`SAM-10-037`, `SAM-11-004`, `SAM-11-005`, `SAM-FORM-32`–`SAM-FORM-37`.

## Reports

### Periodic and annual reporting

- **Purpose:** Prepare, review, submit, and retain required monthly, four-monthly, and annual financial reports.
- **Supported actors:** Accounts staff/teacher; head teacher; School Management Committee; relevant local level/body; auditor.
- **Starting condition:** Source books for the reporting period are posted and the period’s deadline is approaching.
- **User steps (UX order over manual duties):** 1. Review income/expenditure accounts, budget account, bank cash book, advance/deposit schedules, and trial balance. 2. Prepare the report by required period and budget subheading. 3. Reconcile related report totals and obtain required certification/approval. 4. Submit within the prescribed period and retain a separate fiscal-year copy.
- **Automatic actions (UX choice):** Generate statements from posted books, compare totals across reports, and show the applicable due date and missing source records.
- **Approvals / verification (Manual):** Verify trial balance before monthly/annual reports; prepare reports by heading; report deadlines include 7 days monthly, 15 days four-monthly, and 30 days annual for income/expenditure statements, with other annual reports due within one month as specified.
- **Records/books/reports affected (Manual):** Monthly/annual income and expenditure accounts (Forms 6–7, 10–11); bank cash book and budget account (Forms 12–13); expenditure statement, advance schedule, bank reconciliation, trial balance (Forms 14–17); deposit reports (Forms 19–21); monthly/four-monthly/annual statements and balance sheet (Forms 25–28); annual inventory/asset statements as applicable.
- **Exception / correction path:** **Manual:** Reconcile monthly, four-monthly, and annual reports; prepare any additional report in the form required by the relevant body. **UX choice:** Show the source entries behind a difference and return a report to the preparer for correction without hiding the earlier version.
- **Completion state:** Reports agree with their source accounts, have required review, are submitted on time, and remain available in the fiscal-year file.
- **Related requirement IDs:** `SAM-01-019`–`SAM-01-021`, `SAM-06-044`–`SAM-06-066`, `SAM-06-078`–`SAM-06-081`, `SAM-07-001`–`SAM-07-011`, `SAM-10-006`, `SAM-10-007`, `SAM-10-010`–`SAM-10-017`, `SAM-10-019`–`SAM-10-028`, `SAM-11-002`–`SAM-11-005`, `SAM-FORM-06`, `SAM-FORM-07`, `SAM-FORM-10`–`SAM-FORM-17`, `SAM-FORM-19`–`SAM-FORM-21`, `SAM-FORM-25`–`SAM-FORM-28`.

## Controls & Audit

### Audit and beruju settlement

- **Purpose:** Support annual financial audit, answer findings, settle irregularities, and retain evidence of resolution.
- **Supported actors:** Auditor; head teacher; accounts staff/teacher; School Management Committee office holders; concerned stakeholders; local level/prescribed bodies.
- **Starting condition:** Audit is due, an auditor requests records, or an audit report identifies an irregularity.
- **User steps (UX order over manual duties):** 1. Arrange the audit and provide requested documents/information on time. 2. Review each finding and prepare a factual response with evidence. 3. Discuss income/expenditure with the auditor and committee when requested. 4. Present the received report at the Teacher-Parent Association meeting and send it to the local level/other prescribed bodies. 5. Track settlement by fiscal year and include prior audit settlement status in auditor-selection conditions/reporting.
- **Automatic actions (UX choice):** Create a dated finding list, link responses/evidence, track status and due follow-up, and retain each fiscal year’s audit file.
- **Approvals / verification (Manual):** Audit follows cited acts/rules; responses are factual; prior audit settlement status is evaluated and stated as prescribed.
- **Records/books/reports affected (Manual):** Annual income/expenditure accounts and statements; auditor’s report; responses/evidence; separate fiscal-year irregularity file; social audit meeting record.
- **Exception / correction path:** **Manual:** Settle irregularities promptly and maintain evidence; no unsupported response. **UX choice:** Keep the original finding and each response/resolution as dated history; reopen a finding only with a recorded reason.
- **Completion state:** Every finding is either supported as settled or remains visible with its response, evidence, and status; report distribution is recorded.
- **Related requirement IDs:** `SAM-01-017`, `SAM-01-022`, `SAM-01-023`, `SAM-09-003`, `SAM-09-016`–`SAM-09-022`, `SAM-11-005`.

### Social audit

- **Purpose:** Review and publicly report whether community-school activities comply with prevailing requirements.
- **Supported actors:** Community school; Teacher-Parent Association; School Management Committee; head teacher; parents/community; auditor where applicable.
- **Starting condition:** Annual social audit is due, or annual accounts/audit report are ready for presentation.
- **User steps (UX order over manual duties):** 1. Prepare the school activity and financial information for public review. 2. Present the audit/report in the association meeting. 3. Record findings and follow-up decisions and submit reports to required bodies.
- **Automatic actions (UX choice):** Assemble approved annual report material and retain the meeting’s documented decisions and follow-up status.
- **Approvals / verification (Manual):** Conduct a social audit annually; evaluate activities against prevailing acts, rules, and law; make the audit report public in the Teacher-Parent Association meeting and send it to required bodies.
- **Records/books/reports affected (Manual):** Annual activity and financial reports; auditor’s report; Teacher-Parent Association/meeting record; submission evidence.
- **Exception / correction path:** **Manual:** Address findings through the factual audit-response and settlement process. **UX choice:** Track each action to its owner and evidence while retaining the meeting record.
- **Completion state:** Annual review has been presented publicly, its record retained, and required submissions made.
- **Related requirement IDs:** `SAM-09-002`, `SAM-09-014`, `SAM-09-015`, `SAM-09-020`, `SAM-11-005`.

### Bank guarantees

- **Purpose:** Maintain complete records of guarantees received for construction and other work and verify every guarantee with its issuing bank.
- **Supported actors:** School staff responsible for construction/other work and guarantee records; issuing bank.
- **Starting condition:** A performance, advance-payment, or other bank guarantee is received by the school.
- **User steps (UX order over manual duties):** 1. Record the guarantee type and all related bank-guarantee details in the appropriate separate, organized records. 2. Contact the issuing bank and request verification. 3. Record the verification outcome and retain supporting correspondence/evidence with the guarantee record. 4. Update its status and retain subsequent status/history changes.
- **Automatic actions (UX choice):** Remind staff to verify a newly received guarantee and keep dated status/history entries linked to the evidence.
- **Approvals / verification (Manual):** Every guarantee received by the school must be verified by contacting the issuing bank.
- **Records/books/reports affected (Manual):** Separate organized records of performance guarantees, advance-payment guarantees, and other guarantees received, with all related bank-guarantee details; issuing-bank verification evidence.
- **Exception / correction path:** **Manual:** The manual requires verification of every guarantee. **UX choice:** Keep unverified or discrepant guarantees visibly pending and record follow-up and corrected details without erasing prior history.
- **Completion state:** Guarantee details and issuing-bank verification evidence are recorded; current status and its history remain traceable.
- **Related requirement IDs:** `SAM-11-019`, `SAM-11-020`.

### Internal control

- **Purpose:** Plan, approve, implement, and monitor controls over school activities, financial records, reporting, and assets.
- **Supported actors:** School; head teacher; School Management Committee; accounts staff/teacher; senior teacher/store staff where relevant.
- **Starting condition:** Annual/control planning begins or periodic monitoring identifies a control gap.
- **User steps (UX order over manual duties):** 1. Prepare a plan covering school activities, lawful and accurate books, timely reports, and report reliability. 2. Obtain School Management Committee approval. 3. Implement the plan and periodically monitor/evaluate it. 4. Record corrective actions and keep financial/inventory evidence organized.
- **Automatic actions (UX choice):** Provide a control-task list, due dates, evidence links, and open-action summary; do not mark a control complete without user confirmation.
- **Approvals / verification (Manual):** Committee approval is required for the work plan; the School Management Committee monitors/evaluates implementation; the school maintains effective controls, reliable records, transparency, and accountability.
- **Records/books/reports affected (Manual):** Approved internal-control work plan; financial books and supporting records; periodic reports; inventory/asset records; monitoring and corrective-action evidence.
- **Exception / correction path:** **Manual:** Identify control weaknesses and monitor corrective action; comply with applicable law. **UX choice:** Keep an unresolved issue visible with its owner and dated resolution evidence.
- **Completion state:** Approved plan is in use, monitoring is recorded, and control actions are either evidenced as complete or remain open.
- **Related requirement IDs:** `SAM-01-016`, `SAM-01-018`, `SAM-09-001`–`SAM-09-013`.
