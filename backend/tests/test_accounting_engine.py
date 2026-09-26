from dataclasses import replace
from datetime import date
from decimal import Decimal

import pytest

from school_accounting.domain.accounting.engine import *


D = date(2025, 8, 1)

def refs() -> PostingReferences:
    return PostingReferences("school", RuleVersion("rule", "published", date(2025, 1, 1), None, MoneyPolicy(2, "ROUND_HALF_UP")), (AnnexCodeVersion("income", "income", "published", date(2025, 1, 1), None), AnnexCodeVersion("expense", "expense", "published", date(2025, 1, 1), None)), (LedgerDefinition("bank-def", "bank", "published", date(2025, 1, 1), None), LedgerDefinition("income-def", "income", "published", date(2025, 1, 1), None), LedgerDefinition("expense-def", "expense", "published", date(2025, 1, 1), None), LedgerDefinition("advance-def", "advance", "published", date(2025, 1, 1), None), LedgerDefinition("deposit-def", "deposit_liability", "published", date(2025, 1, 1), None)), (SchoolLedgerAccount("bank", "bank-def", "active", date(2025, 1, 1), None), SchoolLedgerAccount("income-ledger", "income-def", "active", date(2025, 1, 1), None), SchoolLedgerAccount("expense-ledger", "expense-def", "active", date(2025, 1, 1), None), SchoolLedgerAccount("advance-ledger", "advance-def", "active", date(2025, 1, 1), None), SchoolLedgerAccount("deposit-ledger", "deposit-def", "active", date(2025, 1, 1), None)), (BankLedgerBinding("binding", "bank-account", "bank", date(2025, 1, 1), None),))

def command(workflow: str, facts=(PostingFact(Decimal("10.00"), "income"),)) -> PostingCommand:
    return PostingCommand("school", "doc", "fy", date(2025, 7, 17), date(2026, 7, 16), D, "approved", workflow, "bank-account", facts, "key")

def test_income_and_ordering_are_balanced() -> None:
    result = derive(command("ordinary_income", (PostingFact(Decimal("10.00"), "income"), PostingFact(Decimal("5.00"), "income"))), refs())
    assert [(x.ledger_account_id, x.debit, x.credit) for x in result.lines] == [("bank", Decimal("15.00"), Decimal("0.00")), ("income-ledger", Decimal("0.00"), Decimal("10.00")), ("income-ledger", Decimal("0.00"), Decimal("5.00"))]

@pytest.mark.parametrize(("workflow", "facts", "expected"), [("simple_expense", (PostingFact(Decimal("10.00"), "expense"), PostingFact(Decimal("5.00"), "expense")), [("expense-ledger", Decimal("10.00"), Decimal("0.00")), ("expense-ledger", Decimal("5.00"), Decimal("0.00")), ("bank", Decimal("0.00"), Decimal("15.00"))]), ("advance_disbursement", (PostingFact(Decimal("10.00")),), [("advance-ledger", Decimal("10.00"), Decimal("0.00")), ("bank", Decimal("0.00"), Decimal("10.00"))]), ("deposit_receipt", (PostingFact(Decimal("10.00")),), [("bank", Decimal("10.00"), Decimal("0.00")), ("deposit-ledger", Decimal("0.00"), Decimal("10.00"))])])
def test_patterns(workflow, facts, expected) -> None:
    assert [(x.ledger_account_id, x.debit, x.credit) for x in derive(command(workflow, facts), refs()).lines] == expected

def test_references_and_determinism() -> None:
    first = derive(command("ordinary_income"), refs()); assert first == derive(command("ordinary_income"), refs())
    assert first.pinned_references == PinnedReferences("rule", ("income",), ("bank-def", "income-def"), ("bank", "income-ledger"), "binding")
    traced = derive(command("ordinary_income", (PostingFact(Decimal("1.00"), "income", "a"), PostingFact(Decimal("2.00"), "income", "b"))), refs())
    assert [x.trace for x in traced.lines] == ["a,b: income → selected bank binding", "a: income → income", "b: income → income"]

@pytest.mark.parametrize("changed", [lambda r: replace(r, bank_ledger_bindings=()), lambda r: replace(r, rule_version=replace(r.rule_version, effective_to=date(2025, 1, 2))), lambda r: replace(r, annex_codes=(replace(r.annex_codes[0], effective_to=date(2025, 1, 2)),) + r.annex_codes[1:]), lambda r: replace(r, school_ledger_accounts=tuple(replace(x, effective_to=date(2025, 1, 2)) if x.id == "income-ledger" else x for x in r.school_ledger_accounts)), lambda r: replace(r, ledger_definitions=r.ledger_definitions + (LedgerDefinition("income-2", "income", "published", date(2025, 1, 1), None),))])
def test_invalid_references_fail(changed) -> None:
    with pytest.raises(ReferenceResolutionError): derive(command("ordinary_income"), changed(refs()))

def test_kind_float_precision_and_unresolved_fail() -> None:
    with pytest.raises(ReferenceResolutionError): derive(command("ordinary_income", (PostingFact(Decimal("1.00"), "expense"),)), refs())
    with pytest.raises(ValidationError): derive(command("ordinary_income", (PostingFact(1.0, "income"),)), refs())
    with pytest.raises(ValidationError): derive(command("ordinary_income", (PostingFact(Decimal("1.001"), "income"),)), refs())
    with pytest.raises(UnresolvedTreatment): derive(command("payroll"), refs())

def test_tenant_lifecycle_bank_and_rounding_validation() -> None:
    with pytest.raises(ValidationError): derive(command("ordinary_income"), replace(refs(), school_id="other"))
    for changed in (lambda r: replace(r, rule_version=replace(r.rule_version, status="draft")), lambda r: replace(r, annex_codes=(replace(r.annex_codes[0], status="draft"),) + r.annex_codes[1:]), lambda r: replace(r, ledger_definitions=tuple(replace(x, status="draft") if x.id == "income-def" else x for x in r.ledger_definitions)), lambda r: replace(r, school_ledger_accounts=tuple(replace(x, status="inactive") if x.id == "income-ledger" else x for x in r.school_ledger_accounts)), lambda r: replace(r, bank_ledger_bindings=(replace(r.bank_ledger_bindings[0], effective_to=date(2025, 1, 2)),)), lambda r: replace(r, school_ledger_accounts=tuple(replace(x, definition_id="expense-def") if x.id == "bank" else x for x in r.school_ledger_accounts))):
        with pytest.raises(ReferenceResolutionError): derive(command("ordinary_income"), changed(refs()))
    assert derive(command("ordinary_income"), replace(refs(), rule_version=replace(refs().rule_version, money_policy=MoneyPolicy(2, None)))).lines
    with pytest.raises(UnresolvedTreatment): derive(command("ordinary_income", (PostingFact(Decimal("1.005"), "income"),)), replace(refs(), rule_version=replace(refs().rule_version, money_policy=MoneyPolicy(3, None))))
