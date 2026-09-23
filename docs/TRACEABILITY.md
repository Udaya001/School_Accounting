# Verified Requirement Traceability

This matrix maps the VERIFIED atomic records in `docs/REQUIREMENTS.md` to planned product capabilities. Each row has one primary module. Behavior describes the planned product responsibility: **User-facing** involves staff entry, review, approval, or submission; **Automatic/system** involves posting, calculation, classification, validation, or generated output. It does not change the manual's stated actor or accounting treatment. All implementation statuses are **PLANNED**.

Scope: 276 chapter requirements, 17 Annex 1 income codes, 45 Annex 2 expense codes, 40 detailed Annex 3 form records, and 12 numbered Annex 4 scenarios: **390 records total**. Navigation prefixes, the 40 form-index rows, and the Annex 4 completed-samples index are references to these records and are not duplicated here.

| Primary capability | Records |
| --- | ---: |
| Accounting rules | 11 |
| Governance and authorization | 7 |
| Budget and funding | 45 |
| Income and fees | 36 |
| Spending and procurement | 31 |
| Payroll and tax | 9 |
| Books and reconciliation | 30 |
| Advances and deposits | 27 |
| Financial reporting | 26 |
| Inventory and assets | 58 |
| Internal control and audit | 28 |
| Travel and petty cash | 16 |
| Account code catalogue | 66 |
| **Total** | **390** |

## Accounting rules

Debit and credit principles, accounting basis, and core financial treatment.

| Requirement ID | Short requirement summary | Primary module | Behavior | Implementation status |
| --- | --- | --- | --- | --- |
| SAM-01-001 | Prepare periodic financial statements in accordance with accounting standards. | Accounting rules | Automatic/system | PLANNED |
| SAM-01-002 | Show the actual assets and liabilities as of the financial-statement preparation date, together with operating results, in the financial statement. | Accounting rules | Automatic/system | PLANNED |
| SAM-01-005 | Record both flows of a transaction under the debit-credit rule. | Accounting rules | Automatic/system | PLANNED |
| SAM-01-006 | For a personal account, debit the receiver and credit the giver. | Accounting rules | Automatic/system | PLANNED |
| SAM-01-007 | For a real account, debit what comes in and credit what goes out. | Accounting rules | Automatic/system | PLANNED |
| SAM-01-008 | For a nominal account, debit expenses and losses and credit income, savings, and profit. | Accounting rules | Automatic/system | PLANNED |
| SAM-01-009 | Select debit and credit accounts according to the nature of each transaction. | Accounting rules | Automatic/system | PLANNED |
| SAM-01-010 | Apply the stated debit-credit rules in reverse when entering an adjustment voucher. | Accounting rules | Automatic/system | PLANNED |
| SAM-01-011 | Treat a negative bank balance as credit and a positive bank balance as debit for adjustment-voucher entry. | Accounting rules | Automatic/system | PLANNED |
| SAM-06-001 | Maintain school accounts on the modified cash basis and internal earning basis, and maintain income and expenditure accounting on the same basis. | Accounting rules | Automatic/system | PLANNED |
| SAM-06-002 | Prepare a balance sheet that accurately shows the school's actual transactions, income, expenditure, assets, liabilities, and fund position. | Accounting rules | Automatic/system | PLANNED |

## Governance and authorization

School roles, responsibility, and spending authority.

| Requirement ID | Short requirement summary | Primary module | Behavior | Implementation status |
| --- | --- | --- | --- | --- |
| SAM-01-012 | Hold an annual meeting of donors and parents, present the preceding academic year's income and expenditure, and approve the next fiscal year's annual… | Governance and authorization | User-facing | PLANNED |
| SAM-01-013 | Prepare the next fiscal year's annual budget and programme on time and present them to the School Management Committee. | Governance and authorization | User-facing | PLANNED |
| SAM-01-014 | After receiving delegated budget allocation and spending authority, spend within the approved budget and according to rules. | Governance and authorization | User-facing | PLANNED |
| SAM-01-015 | Operate the school bank account through the joint signatures of the head teacher and the accounts staff member/teacher. | Governance and authorization | User-facing | PLANNED |
| SAM-01-016 | Keep financial-transaction records organized, correct, and secure. | Governance and authorization | User-facing | PLANNED |
| SAM-01-017 | Arrange timely audit of all financial-transaction records. | Governance and authorization | User-facing | PLANNED |
| SAM-01-018 | Record inventory at the prescribed cost and maintain, protect, and inspect it. | Governance and authorization | User-facing | PLANNED |

## Budget and funding

Budget preparation, allocation, grant release, and funding records.

| Requirement ID | Short requirement summary | Primary module | Behavior | Implementation status |
| --- | --- | --- | --- | --- |
| SAM-02-001 | Maintain one school fund for each school. | Budget and funding | User-facing | PLANNED |
| SAM-02-002 | Deposit every type of school income into the school fund. | Budget and funding | User-facing | PLANNED |
| SAM-02-003 | Complete the required expenditure procedure before spending from the school fund. | Budget and funding | User-facing | PLANNED |
| SAM-02-004 | Spend money deposited in the school fund according to a School Management Committee decision made under prevailing acts, rules, and law. | Budget and funding | User-facing | PLANNED |
| SAM-02-005 | Operate the school fund through the joint signatures of the head teacher and the accounts-related staff member/teacher. | Budget and funding | User-facing | PLANNED |
| SAM-02-006 | Conduct school-fund financial transactions through a bank account. | Budget and funding | User-facing | PLANNED |
| SAM-02-007 | Keep the school-fund account books. | Budget and funding | User-facing | PLANNED |
| SAM-02-008 | Make all school expenditures from money deposited in the school fund. | Budget and funding | User-facing | PLANNED |
| SAM-02-009 | Obtain a bank statement, reconcile the bank account monthly, and send the reconciliation report to the relevant body. | Budget and funding | User-facing | PLANNED |
| SAM-04-001 | Identify the income and expenditure sources expected for the coming fiscal year and prepare the annual budget and programme on that basis. | Budget and funding | User-facing | PLANNED |
| SAM-04-002 | Use the preceding fiscal year's actual income and expenditure and the current fiscal year's revised income and expenditure when preparing the income and… | Budget and funding | User-facing | PLANNED |
| SAM-04-003 | Allocate budget amounts according to the income-code and expenditure-code classifications. | Budget and funding | User-facing | PLANNED |
| SAM-04-004 | Present the coming fiscal year's annual income/expenditure budget and programme to the School Management Committee and have them approved by the end of… | Budget and funding | User-facing | PLANNED |
| SAM-04-005 | Prepare the annual income estimate after identifying expected income from internal income, federal government, provincial government, local level, and… | Budget and funding | User-facing | PLANNED |
| SAM-04-006 | Prepare the income estimate by income heading in accordance with the income-code classification and explanation, using the preceding fiscal year's actual… | Budget and funding | User-facing | PLANNED |
| SAM-04-007 | Identify regular and capital expenditure required for the coming fiscal year and prepare the expenditure estimate on that basis. | Budget and funding | User-facing | PLANNED |
| SAM-04-008 | Prepare the expenditure estimate by expenditure heading in accordance with the expenditure-code classification and explanation, using the preceding fiscal… | Budget and funding | User-facing | PLANNED |
| SAM-04-009 | Show amounts allocated to each expenditure heading accurately in the expenditure estimate. | Budget and funding | User-facing | PLANNED |
| SAM-04-010 | Do not prepare a deficit budget in which the expenditure estimate exceeds the income estimate. | Budget and funding | User-facing | PLANNED |
| SAM-04-011 | Use the Annual Budget Form (Form 1) and its prescribed method of use for income/expenditure budget preparation. | Budget and funding | User-facing | PLANNED |
| SAM-05-001 | Request budget release monthly or four-monthly, under the guidance issued by the relevant local level, for grants received from federal, provincial, and… | Budget and funding | User-facing | PLANNED |
| SAM-05-002 | For the first four-monthly budget-release request, submit a copy of the approved annual budget and programme to the relevant local level. | Budget and funding | User-facing | PLANNED |
| SAM-05-003 | For the first four-monthly budget-release request, submit the preceding fiscal year's income/expenditure details and expenditure statement to the relevant… | Budget and funding | User-facing | PLANNED |
| SAM-05-004 | Submit the name list of teachers and staff and the form showing the monthly salary amount claimed when requesting budget release. | Budget and funding | User-facing | PLANNED |
| SAM-05-005 | Submit a completed Teacher Salary Request Form when requesting monthly teacher salary funds. | Budget and funding | User-facing | PLANNED |
| SAM-05-006 | For the second and third four-monthly budget-release requests, submit expenditure details through the preceding month. | Budget and funding | User-facing | PLANNED |
| SAM-05-007 | For the third four-monthly budget-release request, submit the preceding fiscal year's audit report in addition to the expenditure details. | Budget and funding | User-facing | PLANNED |
| SAM-05-008 | Make budget-release requests according to instructions issued from time to time by the relevant local level or competent body, and comply with those… | Budget and funding | User-facing | PLANNED |
| SAM-05-009 | When requesting budget release from the local level, use the format prescribed by that local level. | Budget and funding | User-facing | PLANNED |
| SAM-05-010 | Use the prescribed Budget Release Request Letter template (Form 39) for a budget-release request letter. | Budget and funding | User-facing | PLANNED |
| SAM-06-091 | Where an approved-budget expenditure heading has an insufficient amount and one or more expenditure headings have a surplus, the head teacher may transfer… | Budget and funding | User-facing | PLANNED |
| SAM-06-092 | For a transfer exceeding 20 percent, or for a transfer from recurrent expenditure to capital expenditure, submit the matter to the School Management… | Budget and funding | User-facing | PLANNED |
| SAM-06-093 | Do not transfer amounts from capital expenditure to recurrent expenditure. | Budget and funding | User-facing | PLANNED |
| SAM-10-001 | Prepare the Annual Budget Form by the end of Ashar each year and send it to the local level. | Budget and funding | User-facing | PLANNED |
| SAM-10-038 | Retain in the school records the authority-letter template issued by the local level to the relevant school. | Budget and funding | User-facing | PLANNED |
| SAM-10-039 | Use the Budget Release Request Letter template when requesting budget release and retain it in school records. | Budget and funding | User-facing | PLANNED |
| SAM-10-040 | Retain in school records the budget-release notice letter issued by the local level. | Budget and funding | User-facing | PLANNED |
| SAM-11-001 | Prepare vouchers separately by budget subheading for conditional recurrent grants, conditional capital grants, unconditional grants, equalization grants… | Budget and funding | User-facing | PLANNED |
| SAM-11-002 | Prepare income/expenditure vouchers, bank cash books, budget accounts, expenditure statements, schedules of advances pending settlement… | Budget and funding | User-facing | PLANNED |
| SAM-FORM-01 | फाराम नं. १ — वार्षिक बजेट तर्जुमा फाराम — documented form structure and use | Budget and funding | User-facing | PLANNED |
| SAM-FORM-38 | फाराम नं. 3८ — विषय : खर्च गर्ने अख्तियारी प्रदान गरिएको सम्बन्धमा । — documented form structure and use | Budget and funding | User-facing | PLANNED |
| SAM-FORM-39 | फाराम नं. 39 — विषय : बजेट रकम निकासा गरिदिने सम्बन्धमा । — documented form structure and use | Budget and funding | User-facing | PLANNED |
| SAM-FORM-40 | फाराम नं. 40 — विषय : बजेट निकासा रकम सम्बन्धमा । — documented form structure and use | Budget and funding | User-facing | PLANNED |
| SAM-ANN-04-001 | काठमाडौं महानगरपालिकाबाट कन्या माध्यमिक विद्यालय, लैनचौरलाई प्रथम चौमासिकको तलब, भत्ता लगायतको रकम निकासा; निकासा मिति २०७६ असोज १ गते, चलानी नं.… | Budget and funding | Automatic/system | PLANNED |
| SAM-ANN-04-005 | २०७६ कार्तिक ३ गते काठमाडौं महानगरपालिकाबाट रकम प्राप्त। | Budget and funding | Automatic/system | PLANNED |

## Income and fees

Receipts, fee collection, income vouchers, and income records.

| Requirement ID | Short requirement summary | Primary module | Behavior | Implementation status |
| --- | --- | --- | --- | --- |
| SAM-06-007 | Issue a cash receipt for cash income received under income headings approved by the School Management Committee. | Income and fees | User-facing | PLANNED |
| SAM-06-008 | Record income received through a bank according to the bank voucher or bank statement. | Income and fees | Automatic/system | PLANNED |
| SAM-06-009 | Raise an income general voucher by income heading for received income and post it to the related account. | Income and fees | Automatic/system | PLANNED |
| SAM-06-010 | Use a cash/receipt receipt for every type of cash income received by the school. | Income and fees | User-facing | PLANNED |
| SAM-06-011 | Prepare each cash receipt in triplicate; give the first copy to the payer, retain the second copy with the related form, and retain the third copy in the… | Income and fees | User-facing | PLANNED |
| SAM-06-012 | Use cash receipts in serial-number order. | Income and fees | Automatic/system | PLANNED |
| SAM-06-013 | Retain a spoiled or cancelled cash receipt in the relevant receipt booklet before issuing another receipt. | Income and fees | User-facing | PLANNED |
| SAM-06-014 | At fiscal-year end, mark unused income receipts as remaining and retain them; for the next fiscal year, bring into use cash receipts printed with new… | Income and fees | User-facing | PLANNED |
| SAM-06-015 | Record income from every cash/receipt receipt used for cash income in the receipt-control account. | Income and fees | Automatic/system | PLANNED |
| SAM-06-016 | Estimate and print the cash/receipt receipts needed by the school at the beginning, record their receipt as income in the receipt-control account, and… | Income and fees | Automatic/system | PLANNED |
| SAM-06-017 | Complete all information in the receipt-control account and keep it up to date. | Income and fees | User-facing | PLANNED |
| SAM-06-018 | Daily, raise an income general voucher for every cash income received, based on the cash receipt or bank voucher/bank statement, and record it under the… | Income and fees | Automatic/system | PLANNED |
| SAM-06-019 | Deposit or submit cash received to the bank on the same day, or the next day if not done on the same day. | Income and fees | User-facing | PLANNED |
| SAM-06-020 | Do not conduct the school's financial transactions in cash. | Income and fees | User-facing | PLANNED |
| SAM-06-021 | Attach the second copy of the cash receipt or the bank voucher to the income general voucher. | Income and fees | User-facing | PLANNED |
| SAM-06-022 | Number income general vouchers sequentially for each fiscal year's income transactions, beginning with voucher number 1 at the beginning of Shrawan. | Income and fees | Automatic/system | PLANNED |
| SAM-06-023 | Enter every income received by the school daily in the monthly income account according to the income general voucher. | Income and fees | User-facing | PLANNED |
| SAM-06-024 | Prepare a monthly income report by income heading from the monthly income account. | Income and fees | User-facing | PLANNED |
| SAM-06-025 | Carry the cumulative income through the preceding month forward into the current month's income amount in sequence. | Income and fees | Automatic/system | PLANNED |
| SAM-06-026 | Close the monthly income account at the end of each fiscal year. | Income and fees | Automatic/system | PLANNED |
| SAM-06-027 | Use the fee register when collecting fees from students. | Income and fees | User-facing | PLANNED |
| SAM-06-028 | Record every cash receipt under its related income heading. | Income and fees | Automatic/system | PLANNED |
| SAM-06-029 | Record income earned within a fiscal year but not yet received in cash as income receivable. | Income and fees | Automatic/system | PLANNED |
| SAM-10-003 | Use the Cash/Receipt Receipt whenever income is received by cash or bank and retain it in the school records. | Income and fees | User-facing | PLANNED |
| SAM-10-004 | Use the Receipt Control Account whenever a receipt/voucher is used to record income or expenditure, and retain it in the school records. | Income and fees | User-facing | PLANNED |
| SAM-10-005 | Raise the Income General Voucher for each income/release document and retain it in the school records. | Income and fees | User-facing | PLANNED |
| SAM-10-006 | Prepare the Monthly Income Account from income general vouchers by the seventh day of each month and send it to the local level. | Income and fees | User-facing | PLANNED |
| SAM-10-007 | Prepare the Annual Income Account within seven days after the fiscal year ends, based on the Monthly Income Account, and send it to the local level. | Income and fees | User-facing | PLANNED |
| SAM-10-008 | Use the Fee Register to record amounts received as fees and retain it in the school records. | Income and fees | User-facing | PLANNED |
| SAM-FORM-03 | फाराम नं. ३ — नगदी/प्राप्ति रसिद — documented form structure and use | Income and fees | User-facing | PLANNED |
| SAM-FORM-04 | फाराम नं. ४ — रसिद नियन्त्रण खाता — documented form structure and use | Income and fees | User-facing | PLANNED |
| SAM-FORM-05 | फाराम नं. ५ — गोश्वारा भौचर -आम्दानी — documented form structure and use | Income and fees | User-facing | PLANNED |
| SAM-FORM-06 | फाराम नं. ६ — मासिक आम्दानी खाता — documented form structure and use | Income and fees | User-facing | PLANNED |
| SAM-FORM-07 | फाराम नं. 7 — वार्षिक आम्दानी खाता — documented form structure and use | Income and fees | User-facing | PLANNED |
| SAM-FORM-08 | फाराम नं. ८ — शुल्क दर्ता किताब — documented form structure and use | Income and fees | User-facing | PLANNED |
| SAM-ANN-04-010 | २०७६ मंसिर ६ गते कन्या माध्यमिक विद्यालयमा देहायका शीर्षकबाट प्राप्त रकमलाई आम्दानी जनाइयो। | Income and fees | Automatic/system | PLANNED |

## Spending and procurement

Expenditure controls, purchases, payment vouchers, and supplier payments.

| Requirement ID | Short requirement summary | Primary module | Behavior | Implementation status |
| --- | --- | --- | --- | --- |
| SAM-06-030 | Record expenditure of amounts approved by the authorized officer on the cash basis. | Spending and procurement | Automatic/system | PLANNED |
| SAM-06-031 | Where an obligation to make an expenditure has arisen but the bill or payment voucher has not been received, show the amount as a payment liability and… | Spending and procurement | User-facing | PLANNED |
| SAM-06-032 | Conduct expenditure-related financial transactions within the budget approved by the School Management Committee, within delegated authority, and in… | Spending and procurement | User-facing | PLANNED |
| SAM-06-033 | Verify expenditure-supporting documents, including bills, payment vouchers, approved orders, and other required evidence; preserve them in order and attach… | Spending and procurement | User-facing | PLANNED |
| SAM-06-034 | Spend only in the budget and programme for which money has been allocated. | Spending and procurement | User-facing | PLANNED |
| SAM-06-035 | Obtain the approval and order of the officer with spending authority before spending budget amounts. | Spending and procurement | User-facing | PLANNED |
| SAM-06-036 | Do not spend more than the amount allocated under an expenditure heading. | Spending and procurement | User-facing | PLANNED |
| SAM-06-037 | Deduct taxes that must be withheld under prevailing rules before making payment. | Spending and procurement | User-facing | PLANNED |
| SAM-06-038 | Conduct the school's financial transactions only through a bank. | Spending and procurement | User-facing | PLANNED |
| SAM-06-039 | Carry out procurement in compliance with the Public Procurement Act, 2063 and Public Procurement Regulations, 2064, and make procurement payments by… | Spending and procurement | User-facing | PLANNED |
| SAM-06-040 | Attach the purchase order, receipt/entry report, and related documents when paying for purchased goods. | Spending and procurement | User-facing | PLANNED |
| SAM-06-041 | Attach proof that the relevant body has passed the salary report when paying teachers' or staff salaries. | Spending and procurement | User-facing | PLANNED |
| SAM-06-042 | Raise an expenditure general voucher for expenditure-related transactions and record the expenditure under the related heading according to the… | Spending and procurement | Automatic/system | PLANNED |
| SAM-06-043 | Number expenditure general vouchers sequentially for each fiscal year's expenditure transactions, beginning with voucher number 1 at the beginning of… | Spending and procurement | Automatic/system | PLANNED |
| SAM-06-044 | Enter every expenditure-related transaction in the monthly expenditure account according to the general voucher. | Spending and procurement | User-facing | PLANNED |
| SAM-06-045 | Prepare a monthly expenditure report by expenditure heading from the monthly expenditure account. | Spending and procurement | User-facing | PLANNED |
| SAM-06-046 | Carry cumulative expenditure through the preceding month forward into the current month's expenditure amount in sequence. | Spending and procurement | Automatic/system | PLANNED |
| SAM-06-047 | Close the monthly expenditure account at the end of each fiscal year. | Spending and procurement | Automatic/system | PLANNED |
| SAM-10-009 | Raise the Expenditure General Voucher for each expenditure with the required bill, payment voucher, and other supporting documents attached, and retain it… | Spending and procurement | User-facing | PLANNED |
| SAM-10-010 | Prepare the Monthly Expenditure Account from expenditure general vouchers by the seventh day of each month and send it to the local level. | Spending and procurement | User-facing | PLANNED |
| SAM-10-011 | Prepare the Annual Expenditure Account within seven days after the fiscal year ends, based on the Monthly Expenditure Account, and send it to the local… | Spending and procurement | User-facing | PLANNED |
| SAM-11-006 | Conduct purchases and service transactions only with firms/businesses registered with the Inland Revenue Office and holding a permanent account number. | Spending and procurement | User-facing | PLANNED |
| SAM-FORM-09 | फाराम नं. 9 — गोश्वारा भौचर - खर्च — documented form structure and use | Spending and procurement | User-facing | PLANNED |
| SAM-FORM-10 | फाराम नं. 10 — मासिक खर्च खाता — documented form structure and use | Spending and procurement | User-facing | PLANNED |
| SAM-FORM-11 | फाराम नं. 11 — वार्षिक खर्च खाता — documented form structure and use | Spending and procurement | User-facing | PLANNED |
| SAM-ANN-04-002 | २०७६ असोज ४ गते विद्यालयका लागि आवश्यक शैक्षिक सामग्री खरिद गरी श्री लक्ष्मी इन्टरप्राइजेजलाई बिल तथा अन्य कागजातबमोजिम नियमानुसार अग्रिम कर कट्टी गरी… | Spending and procurement | Automatic/system | PLANNED |
| SAM-ANN-04-003 | २०७६ असोज ४ गते आधारभूत तहका विपन्न/जेहेन्दार विद्यार्थीलाई छात्रवृत्ति वितरण। | Spending and procurement | Automatic/system | PLANNED |
| SAM-ANN-04-006 | २०७६ कार्तिक ४ गते विद्यालयका लागि नयाँ खरिद गरिएको डेस्क बेन्च, कुर्सी, टेबल लगायतका सामग्रीका लागि श्री विपना ट्रेडर्सलाई नियमानुसार अग्रिम कर कट्टी गरी… | Spending and procurement | Automatic/system | PLANNED |
| SAM-ANN-04-007 | २०७६ कार्तिक १० गते विद्यालय भवन निर्माण समितिलाई कक्षाकोठा निर्माण सामग्री खरिदबापत भुक्तानी। | Spending and procurement | Automatic/system | PLANNED |
| SAM-ANN-04-008 | विद्यालय भवन मर्मतबापत श्री गोविन्द निर्माण सेवालाई संलग्न सम्झौता, Running Bill तथा अन्य कागजातका आधारमा 300,000.00 नियमानुसार धरौटी तथा करकट्टी गरी… | Spending and procurement | Automatic/system | PLANNED |
| SAM-ANN-04-011 | २०७६ मंसिर ८ गते विद्यालय भवन मर्मतबापत श्री गोविन्द निर्माण सेवालाई कार्य सम्पन्न प्रतिवेदन तथा अन्तिम बिल एवं कर बिजकबमोजिम नियमानुसार धरौटी तथा करकट्टी… | Spending and procurement | Automatic/system | PLANNED |

## Payroll and tax

Salary requests, deductions, withholding, and statutory remittances.

| Requirement ID | Short requirement summary | Primary module | Behavior | Implementation status |
| --- | --- | --- | --- | --- |
| SAM-10-002 | Use the Teacher Salary Request Form when requesting salary release monthly or four-monthly and send it to the local level. | Payroll and tax | User-facing | PLANNED |
| SAM-11-007 | Withhold advance income tax from taxable payments, deposit it in the bank under the prescribed revenue heading, send the bank voucher with a letter to the… | Payroll and tax | User-facing | PLANNED |
| SAM-11-008 | Withhold fifty percent of value-added tax from supplier bills from Shrawan 2076 onward, submit that portion to the Inland Revenue Office with the bank… | Payroll and tax | User-facing | PLANNED |
| SAM-11-009 | Withhold annual income tax from unmarried teachers/staff according to the tax slabs and rates stated in the Income Tax Act, 2058 and Regulations, 2059, and… | Payroll and tax | User-facing | PLANNED |
| SAM-11-010 | Withhold annual income tax from married teachers/staff according to the tax slabs and rates stated in the Income Tax Act, 2058 and Regulations, 2059, and… | Payroll and tax | User-facing | PLANNED |
| SAM-11-011 | For permanently appointed teachers/staff covered by the contributory retirement and gratuity arrangement from Shrawan 1, 2076, deduct six percent of… | Payroll and tax | User-facing | PLANNED |
| SAM-11-012 | Send the voucher and statement of amounts withheld for the retirement and gratuity fund to the Employees Provident Fund monthly. | Payroll and tax | User-facing | PLANNED |
| SAM-FORM-02 | फाराम नं. २ — शिक्षक तलव माग फाराम — documented form structure and use | Payroll and tax | User-facing | PLANNED |
| SAM-ANN-04-004 | २०७६ असोज २५ गते शिक्षकहरूको तलब, भत्ता, चाडपर्व खर्च र कट्टी रकम; रकम सम्बन्धित शिक्षकहरूको बैंक खातामा जम्मा। | Payroll and tax | Automatic/system | PLANNED |

## Books and reconciliation

Transaction books, balances, trial balance, and bank reconciliation.

| Requirement ID | Short requirement summary | Primary module | Behavior | Implementation status |
| --- | --- | --- | --- | --- |
| SAM-06-048 | After raising a general voucher, enter income, expenditure, advances, advance settlement, deductions, and other transactions in the bank cash book. | Books and reconciliation | Automatic/system | PLANNED |
| SAM-06-049 | Use the bank cash book to show the actual status of the school's income, expenditure, release amounts, advances, and deductible amounts. | Books and reconciliation | Automatic/system | PLANNED |
| SAM-06-050 | Prepare the bank cash book monthly. | Books and reconciliation | Automatic/system | PLANNED |
| SAM-06-051 | Post general-voucher details to the budget account. | Books and reconciliation | Automatic/system | PLANNED |
| SAM-06-052 | Post the school's approved budget and supplementary budget to budget headings in the budget account. | Books and reconciliation | Automatic/system | PLANNED |
| SAM-06-053 | Post money deposited in the school fund and money released by the local level or another relevant body to the release heading in the budget account. | Books and reconciliation | Automatic/system | PLANNED |
| SAM-06-054 | Post expenditure general vouchers to expenditure headings in the budget account in serial-number order. | Books and reconciliation | Automatic/system | PLANNED |
| SAM-06-055 | Prepare the budget account monthly. | Books and reconciliation | Automatic/system | PLANNED |
| SAM-06-056 | Prepare the expenditure statement monthly on the basis of the budget account. | Books and reconciliation | Automatic/system | PLANNED |
| SAM-06-057 | Use the expenditure statement to provide the head teacher and School Management Committee with the budget position for budget-related decisions. | Books and reconciliation | Automatic/system | PLANNED |
| SAM-06-058 | Prepare the schedule of advances pending settlement each month on the basis of the advance subsidiary account. | Books and reconciliation | Automatic/system | PLANNED |
| SAM-06-059 | Show the status of advances and advance settlement in the schedule of advances pending settlement. | Books and reconciliation | Automatic/system | PLANNED |
| SAM-06-060 | Ensure that the amounts in the schedule of advances pending settlement agree with the advance and advance-settlement columns of the bank cash book. | Books and reconciliation | Automatic/system | PLANNED |
| SAM-06-061 | Reconcile the bank balance shown in the bank cash book with the balance shown in the bank statement and prepare a bank-reconciliation statement each month. | Books and reconciliation | Automatic/system | PLANNED |
| SAM-06-062 | Obtain a bank statement each month for bank-balance reconciliation. | Books and reconciliation | Automatic/system | PLANNED |
| SAM-06-063 | Where the bank cash book and bank statement show different balances, clearly state the reason for the difference and adjust the school account. | Books and reconciliation | Automatic/system | PLANNED |
| SAM-06-064 | Prepare a trial balance monthly to determine whether income and expenditure accounting records agree. | Books and reconciliation | Automatic/system | PLANNED |
| SAM-06-065 | Ensure that the total debit column equals the total credit column in the trial balance. | Books and reconciliation | Automatic/system | PLANNED |
| SAM-06-066 | Prepare a trial balance before preparing monthly and annual financial reports to ensure their accuracy. | Books and reconciliation | Automatic/system | PLANNED |
| SAM-06-088 | The school may keep accounts in a computerized accounting system approved by the Ministry of Education, Science and Technology. | Books and reconciliation | Automatic/system | PLANNED |
| SAM-06-089 | When keeping accounts under the computerized accounting system, record income and expenditure according to debit-credit principles. | Books and reconciliation | Automatic/system | PLANNED |
| SAM-06-090 | A computerized accounting system must prepare the necessary accounts and financial reports from the accounting records maintained under that system. | Books and reconciliation | Automatic/system | PLANNED |
| SAM-10-012 | Prepare the Bank Cash Book by the seventh day of each month and retain it in the school records. | Books and reconciliation | Automatic/system | PLANNED |
| SAM-10-013 | Prepare the Budget Account by the seventh day of each month and retain it in the school records. | Books and reconciliation | Automatic/system | PLANNED |
| SAM-10-016 | Prepare the Bank-Reconciliation Statement by the seventh day of each month and send it to the local level. | Books and reconciliation | Automatic/system | PLANNED |
| SAM-10-017 | Prepare the Trial Balance by the seventh day of each month and send it to the local level. | Books and reconciliation | Automatic/system | PLANNED |
| SAM-FORM-12 | फाराम नं. 12 — बैंक नगदी किताब — documented form structure and use | Books and reconciliation | User-facing | PLANNED |
| SAM-FORM-13 | फाराम नं. 13 — बजेट खाता (Budget Sheet) — documented form structure and use | Books and reconciliation | User-facing | PLANNED |
| SAM-FORM-16 | फाराम नं. १6 — बैंक हिसाब मिलान विवरण — documented form structure and use | Books and reconciliation | User-facing | PLANNED |
| SAM-FORM-17 | फाराम नं. १7 — सन्तुलन परीक्षण — documented form structure and use | Books and reconciliation | User-facing | PLANNED |

## Advances and deposits

Advance issue and settlement, security deposits, and related records.

| Requirement ID | Short requirement summary | Primary module | Behavior | Implementation status |
| --- | --- | --- | --- | --- |
| SAM-06-067 | Record in the advance subsidiary account every advance made, under a decision or rule, to a teacher, staff member, person, or institution for purchasing… | Advances and deposits | Automatic/system | PLANNED |
| SAM-06-068 | Maintain a separate folio in the advance subsidiary account for each person or institution. | Advances and deposits | User-facing | PLANNED |
| SAM-06-069 | Record advance settlement in the advance subsidiary account once an advance is settled according to rules. | Advances and deposits | Automatic/system | PLANNED |
| SAM-06-070 | Use the advance subsidiary account both when an advance is given and when it is settled. | Advances and deposits | User-facing | PLANNED |
| SAM-06-071 | Record in the general deposit account every amount received as a security deposit for work or as a deposit from a person or institution. | Advances and deposits | Automatic/system | PLANNED |
| SAM-06-072 | Raise a general voucher when a deposit is received and when it is refunded. | Advances and deposits | User-facing | PLANNED |
| SAM-06-073 | Refund a deposit to the relevant person or institution according to rules after the work is completed or the period has ended. | Advances and deposits | User-facing | PLANNED |
| SAM-06-074 | Do not spend a deposit held by the school on other work. | Advances and deposits | User-facing | PLANNED |
| SAM-06-075 | For a long-standing deposit that has not been claimed by the relevant person or institution, or whose payee cannot be identified, follow the prescribed… | Advances and deposits | User-facing | PLANNED |
| SAM-06-076 | Record each deposit received by the school according to rules in the individual deposit account. | Advances and deposits | Automatic/system | PLANNED |
| SAM-06-077 | Record each deposit refund in the individual deposit account. | Advances and deposits | Automatic/system | PLANNED |
| SAM-06-078 | Prepare the deposit financial statement by the seventh day of each month, when a balance remains in the school's deposit account, using the bank's… | Advances and deposits | User-facing | PLANNED |
| SAM-06-079 | Use the deposit financial statement to ascertain the actual deposit balance. | Advances and deposits | User-facing | PLANNED |
| SAM-06-080 | Ensure that the bank balance shown in the general deposit account equals the bank balance shown by the bank. | Advances and deposits | Automatic/system | PLANNED |
| SAM-06-081 | Where those deposit-account balances differ, clearly state the reason for the difference. | Advances and deposits | User-facing | PLANNED |
| SAM-10-015 | Prepare the Schedule of Advances Pending Settlement by the seventh day of each month and send it to the local level. | Advances and deposits | User-facing | PLANNED |
| SAM-10-018 | Post each advance and advance-settlement transaction to the Advance Subsidiary Account and retain it in the school records. | Advances and deposits | Automatic/system | PLANNED |
| SAM-10-019 | Post each deposit transaction to the General Deposit Account, prepare it by the seventh day of each month, retain it in school records, and send the… | Advances and deposits | Automatic/system | PLANNED |
| SAM-10-020 | Post each individual's or institution's deposit details to the Individual Deposit Account, retain it in school records, and send the final-Asar transaction… | Advances and deposits | Automatic/system | PLANNED |
| SAM-10-021 | Obtain a bank statement and prepare the Deposit Financial Statement by the seventh day of each month; retain it in school records and send its final-Asar… | Advances and deposits | Automatic/system | PLANNED |
| SAM-FORM-15 | फाराम नं. १5 — फर्छ्यौट गर्न बाँकी पेश्कीको मास्केबारी — documented form structure and use | Advances and deposits | User-facing | PLANNED |
| SAM-FORM-18 | फाराम नं. १8 — पेश्की सहायक खाता — documented form structure and use | Advances and deposits | User-facing | PLANNED |
| SAM-FORM-19 | फाराम नं. १9 — गोश्वारा धरौटी खाता — documented form structure and use | Advances and deposits | User-facing | PLANNED |
| SAM-FORM-20 | फाराम नं. 20 — व्यक्तिगत धरौटी खाता — documented form structure and use | Advances and deposits | User-facing | PLANNED |
| SAM-FORM-21 | फाराम नं. 2१ — धरौटीको वित्तीय विवरण — documented form structure and use | Advances and deposits | User-facing | PLANNED |
| SAM-ANN-04-009 | २०७६ कार्तिक १५ गते विद्यालयलाई सूचना प्रविधि मैत्री बनाउने प्रयोजनार्थ कम्प्युटर लगायतका सामग्री खरिदका लागि शिक्षक श्री रामप्रसाद दाहाललाई पेश्की उपलब्ध। | Advances and deposits | Automatic/system | PLANNED |
| SAM-ANN-04-012 | शिक्षक श्री रामप्रसाद दाहालले लिएको पेश्की रकम 350,000.00 सम्बन्धमा निजले पेश गरेको 400,000.00 को बिल बिजक तथा दाखिला प्रतिवेदनअनुसार 350,000.00 पे.फ. गरी… | Advances and deposits | Automatic/system | PLANNED |

## Financial reporting

Periodic statements, annual reports, and balance sheets.

| Requirement ID | Short requirement summary | Primary module | Behavior | Implementation status |
| --- | --- | --- | --- | --- |
| SAM-01-019 | Keep an account of expenditure from released funds. | Financial reporting | Automatic/system | PLANNED |
| SAM-01-020 | Prepare expenditure statements and financial statements within the prescribed time. | Financial reporting | Automatic/system | PLANNED |
| SAM-01-021 | Obtain the head teacher's approval/certification of expenditure statements and financial statements, then submit them to the relevant local body on time. | Financial reporting | User-facing | PLANNED |
| SAM-07-001 | After recording annual financial transactions in the budget account, bank cash book, and other required accounts, prepare annual account books and… | Financial reporting | Automatic/system | PLANNED |
| SAM-07-002 | Reconcile monthly, four-monthly, and annual financial reports with one another. | Financial reporting | Automatic/system | PLANNED |
| SAM-07-003 | Prepare and submit the monthly income/expenditure report within seven days after the month has passed. | Financial reporting | User-facing | PLANNED |
| SAM-07-004 | Prepare and submit the four-monthly income/expenditure report within fifteen days after the four-month period has passed. | Financial reporting | User-facing | PLANNED |
| SAM-07-005 | Prepare and submit the annual income/expenditure report within thirty days after the fiscal year has ended. | Financial reporting | User-facing | PLANNED |
| SAM-07-006 | Prepare annual financial reports and send them to the relevant body within one month after the fiscal year has ended. | Financial reporting | User-facing | PLANNED |
| SAM-07-007 | Prepare annual reports separately by budget subheading. | Financial reporting | Automatic/system | PLANNED |
| SAM-07-008 | Prepare additional annual reports when required by a relevant body, in the manner it specifies. | Financial reporting | Automatic/system | PLANNED |
| SAM-07-009 | Prepare a balance sheet within one month after the fiscal year has ended. | Financial reporting | Automatic/system | PLANNED |
| SAM-07-010 | Use the balance sheet to show the actual state of the school's assets and liabilities. | Financial reporting | Automatic/system | PLANNED |
| SAM-07-011 | Include fixed assets, investments, properties, financial assets (advances and deposits), inventory, cash and bank, payable amounts, funds, and reserves in… | Financial reporting | Automatic/system | PLANNED |
| SAM-10-014 | Prepare the Expenditure Statement by the seventh day of each month and send it to the local level. | Financial reporting | User-facing | PLANNED |
| SAM-10-025 | Prepare the Monthly Income/Expenditure Statement by the seventh day of each month from monthly income and expenditure accounts and send it to the local… | Financial reporting | User-facing | PLANNED |
| SAM-10-026 | Prepare the Four-Monthly Income/Expenditure Statement within fifteen days after the four-month period ends, based on the monthly statement, and send it to… | Financial reporting | User-facing | PLANNED |
| SAM-10-027 | Prepare the Annual Income/Expenditure Statement within thirty days after the fiscal year ends, based on the four-monthly statement, and send it to the… | Financial reporting | User-facing | PLANNED |
| SAM-10-028 | Prepare the Balance Sheet within thirty days after the fiscal year ends and send it to the local level. | Financial reporting | User-facing | PLANNED |
| SAM-11-003 | Prepare annual statements separately by income/expenditure heading and submit them to the relevant body within thirty days after the fiscal year ends. | Financial reporting | User-facing | PLANNED |
| SAM-11-005 | Send annual income/expenditure and inventory/asset-management statements to the local level, make them available to the auditor and social audit, retain… | Financial reporting | User-facing | PLANNED |
| SAM-FORM-14 | फाराम नं. १4 — खर्चको फाँटवारी — documented form structure and use | Financial reporting | User-facing | PLANNED |
| SAM-FORM-25 | फाराम नं. 25 — मासिक आय व्यय विवरण — documented form structure and use | Financial reporting | User-facing | PLANNED |
| SAM-FORM-26 | फाराम नं. 26 — चौमासिक आय व्यय विवरण — documented form structure and use | Financial reporting | User-facing | PLANNED |
| SAM-FORM-27 | फाराम नं. 27 — वार्षिक आय व्यय विवरण — documented form structure and use | Financial reporting | User-facing | PLANNED |
| SAM-FORM-28 | फाराम नं. 28 — वासलात — documented form structure and use | Financial reporting | User-facing | PLANNED |

## Inventory and assets

Goods requests, receipt, stock records, transfers, inspections, and assets.

| Requirement ID | Short requirement summary | Primary module | Behavior | Implementation status |
| --- | --- | --- | --- | --- |
| SAM-08-001 | Classify school-owned physical goods and assets as current or capital assets. | Inventory and assets | Automatic/system | PLANNED |
| SAM-08-002 | Treat inventory/assets usable within one year or for less than one year as current assets or consumable inventory, and assets usable for more than one year… | Inventory and assets | User-facing | PLANNED |
| SAM-08-003 | Ensure the security of inventory and physical assets. | Inventory and assets | User-facing | PLANNED |
| SAM-08-004 | Maintain records of all inventory and assets owned by the school. | Inventory and assets | Automatic/system | PLANNED |
| SAM-08-005 | Maintain separate accounts for consumable and non-consumable inventory/assets. | Inventory and assets | User-facing | PLANNED |
| SAM-08-006 | Arrange physical protection and preservation of recorded inventory and assets. | Inventory and assets | User-facing | PLANNED |
| SAM-08-007 | Where a fixed asset received by purchase, donation, or transfer has no stated value, coordinate with the relevant local level, form a valuation committee… | Inventory and assets | User-facing | PLANNED |
| SAM-08-008 | Pack inventory and assets properly when moving them so they are not damaged. | Inventory and assets | User-facing | PLANNED |
| SAM-08-009 | Do not allow unauthorized persons to use school property for personal work. | Inventory and assets | User-facing | PLANNED |
| SAM-08-010 | Repair repairable inventory in time and return it to use; for inventory that cannot be used even after repair, follow the legal process for auction sale. | Inventory and assets | User-facing | PLANNED |
| SAM-08-011 | Register land remaining to be registered in the school's name under the legal process and maintain its record in the school's name. | Inventory and assets | User-facing | PLANNED |
| SAM-08-012 | Prevent school land from being mortgaged and use it for the maximum benefit of the school. | Inventory and assets | User-facing | PLANNED |
| SAM-08-013 | Where income due from school land remains unpaid, follow the required process to recover it. | Inventory and assets | User-facing | PLANNED |
| SAM-08-014 | Arrange use of school land and property for school expansion and physical development. | Inventory and assets | User-facing | PLANNED |
| SAM-08-015 | Do not sell or mortgage school land except as provided by law, and do not surrender school land except with Government of Nepal approval. | Inventory and assets | User-facing | PLANNED |
| SAM-08-016 | Keep inventory and asset records current and correct, and submit monthly/annual reports to the relevant body within the prescribed time. | Inventory and assets | User-facing | PLANNED |
| SAM-08-017 | Update fixed-asset records with appropriate identification codes based on the property's storage location and identification needs, and maintain cost… | Inventory and assets | User-facing | PLANNED |
| SAM-08-018 | Include the value of land, buildings, furniture, machinery/equipment, and vehicles in the annual balance sheet. | Inventory and assets | User-facing | PLANNED |
| SAM-08-019 | Obtain approval from the authorized officer after submitting a requisition form before buying required inventory from stock or the market. | Inventory and assets | User-facing | PLANNED |
| SAM-08-020 | Purchase inventory from the market under an approved requisition form only after preparing a purchase order and obtaining the authorized officer's written… | Inventory and assets | User-facing | PLANNED |
| SAM-08-021 | Prepare the purchase order in triplicate; give two copies to the supplier and attach the supplier's bill and one certified purchase-order copy to the… | Inventory and assets | User-facing | PLANNED |
| SAM-08-022 | Number and file purchase orders sequentially by date, beginning each fiscal year's orders with number 1 in Shrawan. | Inventory and assets | Automatic/system | PLANNED |
| SAM-08-023 | Prepare a receipt/entry report to record as income inventory purchased under a purchase order or received from government, local level, another… | Inventory and assets | Automatic/system | PLANNED |
| SAM-08-024 | For transferred inventory, certify the receipt/entry report through the head teacher, send a copy to the providing body or institution, and retain a copy… | Inventory and assets | User-facing | PLANNED |
| SAM-08-025 | Number receipt/entry reports sequentially by date, beginning each fiscal year's first report with number 1 in Shrawan. | Inventory and assets | Automatic/system | PLANNED |
| SAM-08-026 | After preparing the receipt/entry report for non-consumable inventory received by purchase or transfer, record it in the non-consumable inventory account… | Inventory and assets | Automatic/system | PLANNED |
| SAM-08-027 | Use the subsidiary inventory account for non-consumable inventory issued for use according to its work nature. | Inventory and assets | User-facing | PLANNED |
| SAM-08-028 | Inspect non-consumable inventory annually to determine its actual condition. | Inventory and assets | User-facing | PLANNED |
| SAM-08-029 | After preparing the receipt/entry report for consumable inventory received by purchase or transfer, record it in the consumable inventory account. | Inventory and assets | Automatic/system | PLANNED |
| SAM-08-030 | Maintain a separate consumable inventory account for each fiscal year, state the remaining balance, and keep the stated stock physically in the store. | Inventory and assets | User-facing | PLANNED |
| SAM-08-031 | After the end of Ashar, record the remaining consumable inventory as the opening balance before using it in the following fiscal year. | Inventory and assets | Automatic/system | PLANNED |
| SAM-08-032 | Maintain a land/building cost book for land and buildings owned or controlled by the school. | Inventory and assets | User-facing | PLANNED |
| SAM-08-033 | Prepare a transfer form when inventory is received by transfer from, or transferred to, another government/non-government body or person. | Inventory and assets | User-facing | PLANNED |
| SAM-08-034 | Transfer school inventory only after a School Management Committee decision. | Inventory and assets | User-facing | PLANNED |
| SAM-08-035 | State the physical condition of inventory when it is transferred or received by transfer. | Inventory and assets | User-facing | PLANNED |
| SAM-08-036 | Within seven days after the fiscal year ends, prepare the annual inventory-stock and physical-condition statement, send it to the relevant body with other… | Inventory and assets | User-facing | PLANNED |
| SAM-08-037 | Within one month after the fiscal year ends, have the head teacher decide to designate a senior teacher in writing for inventory inspection. | Inventory and assets | User-facing | PLANNED |
| SAM-08-038 | Prepare the inventory inspection form and submit it to the senior teacher designated for inspection. | Inventory and assets | User-facing | PLANNED |
| SAM-08-039 | Conduct an on-site inspection of the physical quantity and condition of inventory, and submit an inventory-inspection report with findings to the head… | Inventory and assets | User-facing | PLANNED |
| SAM-10-029 | Use the Requisition Form whenever inventory is requested and when it is released, and retain it in school records. | Inventory and assets | User-facing | PLANNED |
| SAM-10-030 | Prepare a Purchase Order for each market purchase and retain it in school records. | Inventory and assets | User-facing | PLANNED |
| SAM-10-031 | Prepare a Receipt/Entry Report whenever goods are entered/received and retain it in school records. | Inventory and assets | User-facing | PLANNED |
| SAM-10-032 | Post a non-consumable inventory Receipt/Entry Report to the Non-consumable Inventory Account and retain it in school records. | Inventory and assets | Automatic/system | PLANNED |
| SAM-10-033 | Post a consumable inventory Receipt/Entry Report to the Consumable Inventory Account and retain it in school records. | Inventory and assets | Automatic/system | PLANNED |
| SAM-10-034 | Prepare the Land/Building Cost Book within thirty days after the fiscal year ends and send it to the local level. | Inventory and assets | User-facing | PLANNED |
| SAM-10-035 | Use a Transfer Form for every inventory transfer and retain it in school records. | Inventory and assets | User-facing | PLANNED |
| SAM-10-036 | Prepare the Annual Inventory-Stock Statement within seven days after the fiscal year ends and send it to the local level. | Inventory and assets | User-facing | PLANNED |
| SAM-10-037 | Complete the Inventory Inspection Form within thirty days after the fiscal year ends and send it to the local level. | Inventory and assets | User-facing | PLANNED |
| SAM-11-004 | Prepare the annual inventory and asset-management statements: Annual Inventory-Stock Statement, Inventory Inspection Form, and Land/Building Cost Book. | Inventory and assets | User-facing | PLANNED |
| SAM-FORM-29 | फाराम नं. 29 — माग फाराम — documented form structure and use | Inventory and assets | User-facing | PLANNED |
| SAM-FORM-30 | फाराम नं. 30 — खरिद आदेश — documented form structure and use | Inventory and assets | User-facing | PLANNED |
| SAM-FORM-31 | फाराम नं. 31 — दाखिला प्रतिवेदन — documented form structure and use | Inventory and assets | User-facing | PLANNED |
| SAM-FORM-32 | फाराम नं. 32 — खर्च भएर नजाने (नखप्ने मालसामान) सामानको जिन्सी खाता — documented form structure and use | Inventory and assets | User-facing | PLANNED |
| SAM-FORM-33 | फाराम नं. 33 — खर्च भएर जाने (नखप्ने मालसामान) सामानको जिन्सी खाता — documented form structure and use | Inventory and assets | User-facing | PLANNED |
| SAM-FORM-34 | फाराम नं 34 — घर जग्गाको लगत किताब — documented form structure and use | Inventory and assets | User-facing | PLANNED |
| SAM-FORM-35 | फाराम नं. 35 — हस्तान्तरण फारम — documented form structure and use | Inventory and assets | User-facing | PLANNED |
| SAM-FORM-36 | फाराम नं. 3६ — जिन्सी मौज्दातको वार्षिक विवरण — documented form structure and use | Inventory and assets | User-facing | PLANNED |
| SAM-FORM-37 | फाराम नं. 37 — जिन्सी निरीक्षण फाराम — documented form structure and use | Inventory and assets | User-facing | PLANNED |

## Internal control and audit

Control plans, audit evidence, social audit, and guarantee records.

| Requirement ID | Short requirement summary | Primary module | Behavior | Implementation status |
| --- | --- | --- | --- | --- |
| SAM-01-022 | Maintain a register of audit irregularities and retain evidence for their settlement. | Internal control and audit | User-facing | PLANNED |
| SAM-01-023 | Where documents or formalities required by prevailing law are incomplete for a payment, state the reason in writing to the head teacher and act on the head… | Internal control and audit | User-facing | PLANNED |
| SAM-09-001 | Establish effective internal control while using school resources, sources, and inventory/assets to the maximum benefit. | Internal control and audit | User-facing | PLANNED |
| SAM-09-002 | Inform the public of the school's annual activities through an annual social audit. | Internal control and audit | User-facing | PLANNED |
| SAM-09-003 | Arrange timely audit of each fiscal year's income and expenditure accounts in accordance with the applicable acts, rules, laws, and directives, and settle… | Internal control and audit | User-facing | PLANNED |
| SAM-09-004 | Conduct financial transactions economically, efficiently, and effectively. | Internal control and audit | User-facing | PLANNED |
| SAM-09-005 | Keep financial-transaction records and reports reliable and maximize use of school resources and means. | Internal control and audit | User-facing | PLANNED |
| SAM-09-006 | Comply with prevailing acts, rules, and law, and increase financial transparency and accountability. | Internal control and audit | User-facing | PLANNED |
| SAM-09-007 | Prepare and implement an internal-control work plan. | Internal control and audit | User-facing | PLANNED |
| SAM-09-008 | Prepare an internal-control work plan under prevailing acts, rules, and law; obtain School Management Committee approval; and implement it. | Internal control and audit | User-facing | PLANNED |
| SAM-09-009 | Monitor and evaluate implementation of the approved internal-control work plan from time to time. | Internal control and audit | User-facing | PLANNED |
| SAM-09-010 | Include the school's complete activities in the internal-control work plan. | Internal control and audit | User-facing | PLANNED |
| SAM-09-011 | Include in the internal-control work plan arrangements to keep financial-transaction books and records correct under law. | Internal control and audit | User-facing | PLANNED |
| SAM-09-012 | Include in the internal-control work plan timely submission of monthly, four-monthly, and annual reports to the relevant body. | Internal control and audit | User-facing | PLANNED |
| SAM-09-013 | Include in the internal-control work plan verification of report reliability. | Internal control and audit | User-facing | PLANNED |
| SAM-09-014 | Form an eleven-member Teacher-Parent Association executive committee, including the School Management Committee chairperson, head teacher, at least one… | Internal control and audit | User-facing | PLANNED |
| SAM-09-015 | Conduct an annual social audit to evaluate whether community-school activities comply with prevailing acts, rules, and law. | Internal control and audit | User-facing | PLANNED |
| SAM-09-016 | Audit the school's financial transactions in accordance with the Education Act, 2028, Education Regulations, 2059, and Local Government Operation Act… | Internal control and audit | User-facing | PLANNED |
| SAM-09-017 | Provide the documents and information requested by the appointed auditor in time. | Internal control and audit | User-facing | PLANNED |
| SAM-09-018 | Provide a factual response to every audit irregularity identified by the auditor. | Internal control and audit | User-facing | PLANNED |
| SAM-09-019 | Arrange discussion between the auditor and School Management Committee office holders on the school's income and expenditure when the auditor wishes to do… | Internal control and audit | User-facing | PLANNED |
| SAM-09-020 | Make the audit report received from the auditor public in the Teacher-Parent Association meeting and send it to the local level and other prescribed… | Internal control and audit | User-facing | PLANNED |
| SAM-09-021 | Maintain separate fiscal-year files of audit irregularities and settle them in time. | Internal control and audit | User-facing | PLANNED |
| SAM-09-022 | In the auditor-selection conditions, require evaluation of the settlement status of irregularities identified in the preceding audit and require that… | Internal control and audit | User-facing | PLANNED |
| SAM-11-015 | Have the head teacher certify bills and payment vouchers for all expenditure under the approved annual programme and budget with a “paid” stamp, and use an… | Internal control and audit | User-facing | PLANNED |
| SAM-11-016 | Maintain organized income-side and expenditure-side bills and payment vouchers. | Internal control and audit | User-facing | PLANNED |
| SAM-11-019 | Maintain separate, organized records of performance guarantees, advance-payment guarantees, and other guarantees received for construction and other work… | Internal control and audit | User-facing | PLANNED |
| SAM-11-020 | Contact the issuing bank and have every bank guarantee received by the school verified. | Internal control and audit | User-facing | PLANNED |

## Travel and petty cash

Travel approval, claims, vehicle logs, and small cash funds.

| Requirement ID | Short requirement summary | Primary module | Behavior | Implementation status |
| --- | --- | --- | --- | --- |
| SAM-06-082 | Undertake travel for school work to a relevant body or office only after a travel order has been approved. | Travel and petty cash | User-facing | PLANNED |
| SAM-06-083 | Maintain records of travel orders. | Travel and petty cash | User-facing | PLANNED |
| SAM-06-084 | After approved travel for school work is completed and the traveller has reported to the school, submit the daily and travel-expense bill together with the… | Travel and petty cash | User-facing | PLANNED |
| SAM-06-085 | Pay daily and travel expenses only when budget allocation and balance are available in the school fund. | Travel and petty cash | User-facing | PLANNED |
| SAM-06-086 | Set a fixed initial amount in the petty-cash fund for small daily expenditure payments. | Travel and petty cash | User-facing | PLANNED |
| SAM-06-087 | After petty-cash money is spent, request reimbursement to replenish the fund and keep it in continuous operation. | Travel and petty cash | User-facing | PLANNED |
| SAM-10-022 | Obtain approval for a Travel Order for each official school travel and retain it in school records. | Travel and petty cash | User-facing | PLANNED |
| SAM-10-023 | Prepare the Daily and Travel-Expense Bill after completing travel according to rules and retain it in school records. | Travel and petty cash | User-facing | PLANNED |
| SAM-10-024 | Use the Petty-Cash Fund Statement as needed under applicable arrangements and retain it in school records. | Travel and petty cash | User-facing | PLANNED |
| SAM-11-013 | Complete and attach the vehicle logbook to the records when recording fuel expenditure for school work. | Travel and petty cash | User-facing | PLANNED |
| SAM-11-014 | Have the teacher, staff member, or office holder using a vehicle complete the vehicle logbook for every use and have it certified by the authorized… | Travel and petty cash | User-facing | PLANNED |
| SAM-11-017 | After approved travel for school work is completed and the traveller has reported to the school, prepare and submit a travel report covering work done… | Travel and petty cash | User-facing | PLANNED |
| SAM-11-018 | Attach the travel report when paying daily and travel expenses. | Travel and petty cash | User-facing | PLANNED |
| SAM-FORM-22 | फाराम नं. 22 — अन्तरदेशीय भ्रमण आदेश — documented form structure and use | Travel and petty cash | User-facing | PLANNED |
| SAM-FORM-23 | फाराम नं. 23 — दैनिक तथा भ्रमण खर्चको बिल — documented form structure and use | Travel and petty cash | User-facing | PLANNED |
| SAM-FORM-24 | फाराम नं. 24 — सानो नगदी कोषको विवरण — documented form structure and use | Travel and petty cash | User-facing | PLANNED |

## Account code catalogue

The manual's exact income and expense classification codes.

| Requirement ID | Short requirement summary | Primary module | Behavior | Implementation status |
| --- | --- | --- | --- | --- |
| SAM-03-001 | Record every school income transaction under an income heading. | Account code catalogue | Automatic/system | PLANNED |
| SAM-03-002 | Apply the income-code classification and explanation in Annex 1 when recording income. | Account code catalogue | Automatic/system | PLANNED |
| SAM-03-003 | Record every school expenditure transaction under an expenditure heading. | Account code catalogue | Automatic/system | PLANNED |
| SAM-03-004 | Apply the expenditure-code classification and explanation in Annex 2 when recording expenditure. | Account code catalogue | Automatic/system | PLANNED |
| SAM-ANN-01-13311 | Income code 13311 — समानीकरण अनुदान | Account code catalogue | Automatic/system | PLANNED |
| SAM-ANN-01-13312 | Income code 13312 — सशर्त चालु अनुदान | Account code catalogue | Automatic/system | PLANNED |
| SAM-ANN-01-13313 | Income code 13313 — सशर्त पुँजीगत अनुदान | Account code catalogue | Automatic/system | PLANNED |
| SAM-ANN-01-14119 | Income code 14119 — अन्य निकायबाट प्राप्त ब्याज | Account code catalogue | Automatic/system | PLANNED |
| SAM-ANN-01-14121 | Income code 14121 — वित्तीय निकायबाट प्राप्त लाभांश | Account code catalogue | Automatic/system | PLANNED |
| SAM-ANN-01-14151 | Income code 14151 — सरकारी सम्पत्तिको वहालबाट प्राप्त आय | Account code catalogue | Automatic/system | PLANNED |
| SAM-ANN-01-14211 | Income code 14211 — कृषि उत्पादनको बिक्री बाट प्राप्त रकम | Account code catalogue | Automatic/system | PLANNED |
| SAM-ANN-01-14212 | Income code 14212 — सरकारी सम्पत्तिको बिक्री बाट प्राप्त रकम | Account code catalogue | Automatic/system | PLANNED |
| SAM-ANN-01-14213 | Income code 14213 — अन्य बिक्री बाट प्राप्त रकम | Account code catalogue | Automatic/system | PLANNED |
| SAM-ANN-01-14223 | Income code 14223 — शिक्षा क्षेत्रको आम्दानी | Account code catalogue | Automatic/system | PLANNED |
| SAM-ANN-01-14229 | Income code 14229 — अन्य प्रशासनिक सेवा शुल्क | Account code catalogue | Automatic/system | PLANNED |
| SAM-ANN-01-14312 | Income code 14312 — प्रशासनिक दण्ड, जरिवाना र जफत | Account code catalogue | Automatic/system | PLANNED |
| SAM-ANN-01-14411 | Income code 14411 — चालु हस्तान्तरण | Account code catalogue | Automatic/system | PLANNED |
| SAM-ANN-01-14421 | Income code 14421 — पुँजीगत हस्तान्तरण | Account code catalogue | Automatic/system | PLANNED |
| SAM-ANN-01-15111 | Income code 15111 — बेरुजू | Account code catalogue | Automatic/system | PLANNED |
| SAM-ANN-01-15112 | Income code 15112 — निकासा फिर्ता | Account code catalogue | Automatic/system | PLANNED |
| SAM-ANN-01-15113 | Income code 15113 — पेश्की फिर्ता | Account code catalogue | Automatic/system | PLANNED |
| SAM-ANN-02-21111 | Expense code 21111 — पारिश्रमिक शिक्षक कर्मचारी | Account code catalogue | Automatic/system | PLANNED |
| SAM-ANN-02-21121 | Expense code 21121 — पोशाक | Account code catalogue | Automatic/system | PLANNED |
| SAM-ANN-02-21123 | Expense code 21123 — औषधी उपचार खर्च | Account code catalogue | Automatic/system | PLANNED |
| SAM-ANN-02-21131 | Expense code 21131 — स्थानीय भत्ता | Account code catalogue | Automatic/system | PLANNED |
| SAM-ANN-02-21132 | Expense code 21132 — महँगी भत्ता | Account code catalogue | Automatic/system | PLANNED |
| SAM-ANN-02-21134 | Expense code 21134 — बैठक भत्ता | Account code catalogue | Automatic/system | PLANNED |
| SAM-ANN-02-21135 | Expense code 21135 — शिक्षक/कर्मचारी प्रोत्साहन पुरस्कार | Account code catalogue | Automatic/system | PLANNED |
| SAM-ANN-02-21139 | Expense code 21139 — अन्य भत्ता | Account code catalogue | Automatic/system | PLANNED |
| SAM-ANN-02-21211 | Expense code 21211 — कर्मचारीको सामाजिक सुरक्षा कोष खर्च | Account code catalogue | Automatic/system | PLANNED |
| SAM-ANN-02-21212 | Expense code 21212 — कर्मचारीको योगदानमा आधारित निवृत्तभरण तथा उपदान कोष खर्च | Account code catalogue | Automatic/system | PLANNED |
| SAM-ANN-02-21213 | Expense code 21213 — कर्मचारीको योगदानमा आधारित बीमाकोष खर्च | Account code catalogue | Automatic/system | PLANNED |
| SAM-ANN-02-21214 | Expense code 21214 — कर्मचारी कल्याण कोष | Account code catalogue | Automatic/system | PLANNED |
| SAM-ANN-02-22111 | Expense code 22111 — पानी तथा बिजुली | Account code catalogue | Automatic/system | PLANNED |
| SAM-ANN-02-22112 | Expense code 22112 — सञ्चार महसुल | Account code catalogue | Automatic/system | PLANNED |
| SAM-ANN-02-22212 | Expense code 22212 — इन्धन कार्यालय प्रयोजन | Account code catalogue | Automatic/system | PLANNED |
| SAM-ANN-02-22213 | Expense code 22213 — सवारी साधन मर्मत खर्च | Account code catalogue | Automatic/system | PLANNED |
| SAM-ANN-02-22214 | Expense code 22214 — बीमा तथा नवीकरण खर्च | Account code catalogue | Automatic/system | PLANNED |
| SAM-ANN-02-22221 | Expense code 22221 — मेसिनरी तथा औजार सञ्चालन तथा सम्भार खर्च | Account code catalogue | Automatic/system | PLANNED |
| SAM-ANN-02-22231 | Expense code 22231 — निर्मित सार्वजनिक सम्पत्तिको मर्मत सम्भार खर्च | Account code catalogue | Automatic/system | PLANNED |
| SAM-ANN-02-22311 | Expense code 22311 — मसलन्द तथा कार्यालय सामग्री | Account code catalogue | Automatic/system | PLANNED |
| SAM-ANN-02-22312 | Expense code 22312 — पशुपंक्षीहरूको आहार | Account code catalogue | Automatic/system | PLANNED |
| SAM-ANN-02-22313 | Expense code 22313 — पुस्तक तथा सामग्री खर्च | Account code catalogue | Automatic/system | PLANNED |
| SAM-ANN-02-22315 | Expense code 22315 — पत्रपत्रिका, छपाइ तथा सूचना प्रकाशन खर्च | Account code catalogue | Automatic/system | PLANNED |
| SAM-ANN-02-22411 | Expense code 22411 — सेवा र परामर्श खर्च | Account code catalogue | Automatic/system | PLANNED |
| SAM-ANN-02-22412 | Expense code 22412 — सूचना प्रणाली तथा सफ्टवेयर सञ्चालन खर्च | Account code catalogue | Automatic/system | PLANNED |
| SAM-ANN-02-22413 | Expense code 22413 — करार सेवा शुल्क | Account code catalogue | Automatic/system | PLANNED |
| SAM-ANN-02-22511 | Expense code 22511 — कर्मचारी तालिम खर्च | Account code catalogue | Automatic/system | PLANNED |
| SAM-ANN-02-22512 | Expense code 22512 — सीप विकास तथा जनचेतना तालिम तथा गोष्ठी सम्बन्धी खर्चहरू | Account code catalogue | Automatic/system | PLANNED |
| SAM-ANN-02-22521 | Expense code 22521 — उत्पादन सामग्री/सेवा | Account code catalogue | Automatic/system | PLANNED |
| SAM-ANN-02-22529 | Expense code 22529 — विविध कार्यक्रम खर्च | Account code catalogue | Automatic/system | PLANNED |
| SAM-ANN-02-22612 | Expense code 22612 — भ्रमण खर्च | Account code catalogue | Automatic/system | PLANNED |
| SAM-ANN-02-22619 | Expense code 22619 — अन्य भ्रमण खर्च | Account code catalogue | Automatic/system | PLANNED |
| SAM-ANN-02-22711 | Expense code 22711 — विविध खर्च | Account code catalogue | Automatic/system | PLANNED |
| SAM-ANN-02-27211 | Expense code 27211 — छात्रवृत्ति | Account code catalogue | Automatic/system | PLANNED |
| SAM-ANN-02-28142 | Expense code 28142 — घरभाडा | Account code catalogue | Automatic/system | PLANNED |
| SAM-ANN-02-28143 | Expense code 28143 — सवारी साधन तथा मेसिन र औजार भाडा | Account code catalogue | Automatic/system | PLANNED |
| SAM-ANN-02-31112 | Expense code 31112 — गैर आवासीय भवन निर्माण/खरिद | Account code catalogue | Automatic/system | PLANNED |
| SAM-ANN-02-31113 | Expense code 31113 — निर्मित भवनको संरचनात्मक सुधार | Account code catalogue | Automatic/system | PLANNED |
| SAM-ANN-02-31114 | Expense code 31114 — जग्गा विकास कार्य | Account code catalogue | Automatic/system | PLANNED |
| SAM-ANN-02-31115 | Expense code 31115 — फर्निचर तथा फिक्चर्स | Account code catalogue | Automatic/system | PLANNED |
| SAM-ANN-02-31121 | Expense code 31121 — सवारी साधन | Account code catalogue | Automatic/system | PLANNED |
| SAM-ANN-02-31122 | Expense code 31122 — मेसिन तथा औजार | Account code catalogue | Automatic/system | PLANNED |
| SAM-ANN-02-31134 | Expense code 31134 — कम्प्युटर सफ्टवेयर निर्माण तथा खरिद खर्च | Account code catalogue | Automatic/system | PLANNED |
| SAM-ANN-02-31159 | Expense code 31159 — अन्य सार्वजनिक निर्माण | Account code catalogue | Automatic/system | PLANNED |
| SAM-ANN-02-31411 | Expense code 31411 — जग्गा प्राप्ति खर्च | Account code catalogue | Automatic/system | PLANNED |
