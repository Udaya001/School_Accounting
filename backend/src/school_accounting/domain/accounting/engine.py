"""Narrow framework-independent accounting engine slice."""

from dataclasses import dataclass
from datetime import date
from decimal import Decimal, ROUND_HALF_UP
from typing import Literal


class AccountingError(Exception): pass
class ValidationError(AccountingError): pass
class UnsupportedTreatment(AccountingError): pass
class UnresolvedTreatment(UnsupportedTreatment): pass
class ReferenceResolutionError(ValidationError): pass


@dataclass(frozen=True)
class MoneyPolicy:
    source_scale: int = 2
    rounding: str | None = None


@dataclass(frozen=True)
class PostingFact:
    amount: Decimal
    annex_code_version_id: str | None = None
    source_key: str = "line-1"


@dataclass(frozen=True)
class PostingCommand:
    school_id: str; document_id: str; fiscal_year_id: str
    fiscal_year_start: date; fiscal_year_end: date; accounting_date: date
    document_status: str; workflow: str; bank_account_id: str | None
    facts: tuple[PostingFact, ...]; idempotency_key: str
    unresolved_flags: tuple[str, ...] = ()


@dataclass(frozen=True)
class RuleVersion:
    id: str; status: str; effective_from: date; effective_to: date | None; money_policy: MoneyPolicy

@dataclass(frozen=True)
class AnnexCodeVersion:
    id: str; kind: Literal["income", "expense"]; status: str; effective_from: date; effective_to: date | None

@dataclass(frozen=True)
class LedgerDefinition:
    id: str; semantic: str; status: str; effective_from: date; effective_to: date | None

@dataclass(frozen=True)
class SchoolLedgerAccount:
    id: str; definition_id: str; status: str; effective_from: date; effective_to: date | None

@dataclass(frozen=True)
class BankLedgerBinding:
    id: str; bank_account_id: str; ledger_account_id: str; effective_from: date; effective_to: date | None

@dataclass(frozen=True)
class PostingReferences:
    school_id: str
    rule_version: RuleVersion; annex_codes: tuple[AnnexCodeVersion, ...]
    ledger_definitions: tuple[LedgerDefinition, ...]; school_ledger_accounts: tuple[SchoolLedgerAccount, ...]
    bank_ledger_bindings: tuple[BankLedgerBinding, ...]


@dataclass(frozen=True)
class DerivedJournalHeader:
    school_id: str; fiscal_year_id: str; accounting_date: date; description: str

@dataclass(frozen=True)
class DerivedJournalLine:
    line_no: int; ledger_account_id: str; debit: Decimal; credit: Decimal; annex_code_version_id: str | None; trace: str

@dataclass(frozen=True)
class PinnedReferences:
    rule_set_version_id: str; annex_code_version_ids: tuple[str, ...]
    ledger_definition_ids: tuple[str, ...]; school_ledger_account_ids: tuple[str, ...]
    bank_ledger_binding_id: str | None

@dataclass(frozen=True)
class DerivedPosting:
    header: DerivedJournalHeader; lines: tuple[DerivedJournalLine, ...]; pinned_references: PinnedReferences


def _period(start: date, end: date | None, on: date) -> bool:
    return start <= on and (end is None or on <= end)

def _published(status: str, start: date, end: date | None, on: date) -> bool:
    return status == "published" and _period(start, end, on)

def _active(status: str, start: date, end: date | None, on: date) -> bool:
    return status == "active" and _period(start, end, on)


def _money(value: Decimal, policy: MoneyPolicy) -> Decimal:
    if isinstance(value, float) or not isinstance(value, Decimal): raise ValidationError("Money must be Decimal, never float")
    if not value.is_finite() or value < 0: raise ValidationError("Money must be finite and non-negative")
    quantum = Decimal(1).scaleb(-policy.source_scale)
    if value != value.quantize(quantum, rounding=ROUND_HALF_UP): raise ValidationError("Source money exceeds permitted precision")
    if value.as_tuple().exponent >= -2: return value
    if policy.rounding != "ROUND_HALF_UP": raise UnresolvedTreatment("Pinned rounding policy is unsupported")
    return value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def _one(items: list[object], label: str) -> object:
    if len(items) != 1: raise ReferenceResolutionError(f"Expected exactly one {label}, found {len(items)}")
    return items[0]


def derive(command: PostingCommand, references: PostingReferences) -> DerivedPosting:
    if references.school_id != command.school_id: raise ValidationError("Reference bundle belongs to another school")
    if command.document_status != "approved": raise ValidationError("Only approved documents may post")
    if command.fiscal_year_start > command.accounting_date or command.accounting_date > command.fiscal_year_end: raise ValidationError("Accounting date is outside fiscal year")
    rule = references.rule_version
    if not _published(rule.status, rule.effective_from, rule.effective_to, command.accounting_date): raise ReferenceResolutionError("Rule version is not published/effective")
    if command.unresolved_flags or command.workflow not in {"ordinary_income", "simple_expense", "advance_disbursement", "deposit_receipt"}: raise UnresolvedTreatment("Workflow or selected branch is unresolved")
    amounts = tuple(_money(f.amount, rule.money_policy) for f in command.facts)
    if not command.facts or any(amount == 0 for amount in amounts): raise ValidationError("Posting facts require positive amounts")

    def semantic(name: str) -> tuple[LedgerDefinition, SchoolLedgerAccount]:
        definitions = [x for x in references.ledger_definitions if x.semantic == name and _published(x.status, x.effective_from, x.effective_to, command.accounting_date)]
        definition = _one(definitions, f"effective {name} definition")
        ledgers = [x for x in references.school_ledger_accounts if x.definition_id == definition.id and _active(x.status, x.effective_from, x.effective_to, command.accounting_date)]
        return definition, _one(ledgers, f"effective school {name} ledger")

    if command.bank_account_id is None: raise ValidationError("Bank workflow requires bank_account_id")
    bindings = [x for x in references.bank_ledger_bindings if x.bank_account_id == command.bank_account_id and x.effective_from <= command.accounting_date and (x.effective_to is None or command.accounting_date <= x.effective_to)]
    binding = _one(bindings, "effective bank ledger binding")
    bank_ledger = _one([x for x in references.school_ledger_accounts if x.id == binding.ledger_account_id and _active(x.status, x.effective_from, x.effective_to, command.accounting_date)], "effective bound bank ledger")
    bank_definition = _one([x for x in references.ledger_definitions if x.id == bank_ledger.definition_id and x.semantic == "bank" and _published(x.status, x.effective_from, x.effective_to, command.accounting_date)], "published bank ledger definition")
    lines: list[DerivedJournalLine] = []
    used_definitions = [bank_definition.id]; used_ledgers = [bank_ledger.id]; annexes: list[str] = []

    def code(fact: PostingFact, kind: str) -> AnnexCodeVersion:
        if fact.annex_code_version_id is None: raise ValidationError("Classification code is required")
        result = _one([x for x in references.annex_codes if x.id == fact.annex_code_version_id and x.kind == kind and _published(x.status, x.effective_from, x.effective_to, command.accounting_date)], f"effective {kind} Annex code")
        annexes.append(result.id); return result
    def add(ledger: SchoolLedgerAccount, debit: Decimal, credit: Decimal, annex: str | None, trace: str) -> None:
        if (debit > 0) == (credit > 0): raise ValidationError("Journal line requires exactly one positive side")
        lines.append(DerivedJournalLine(len(lines) + 1, ledger.id, debit, credit, annex, trace))

    if command.workflow == "ordinary_income":
        definition, ledger = semantic("income"); used_definitions.append(definition.id); used_ledgers.append(ledger.id)
        for fact, amount in zip(command.facts, amounts): add(ledger, Decimal("0.00"), amount, code(fact, "income").id, f"{fact.source_key}: income → income")
        add(bank_ledger, sum(amounts, Decimal("0.00")), Decimal("0.00"), None, f"{','.join(x.source_key for x in command.facts)}: income → selected bank binding")
        lines.insert(0, lines.pop())
        lines = [DerivedJournalLine(i + 1, x.ledger_account_id, x.debit, x.credit, x.annex_code_version_id, x.trace) for i, x in enumerate(lines)]
    elif command.workflow == "simple_expense":
        definition, ledger = semantic("expense"); used_definitions.append(definition.id); used_ledgers.append(ledger.id)
        for fact, amount in zip(command.facts, amounts): add(ledger, amount, Decimal("0.00"), code(fact, "expense").id, f"{fact.source_key}: expense → expense")
        add(bank_ledger, Decimal("0.00"), sum(amounts, Decimal("0.00")), None, f"{','.join(x.source_key for x in command.facts)}: expense → selected bank binding")
    else:
        role = "advance" if command.workflow == "advance_disbursement" else "deposit_liability"
        definition, ledger = semantic(role); used_definitions.append(definition.id); used_ledgers.append(ledger.id)
        total = sum(amounts, Decimal("0.00"))
        if command.workflow == "advance_disbursement": add(ledger, total, Decimal("0.00"), None, "advance fact → advance"); add(bank_ledger, Decimal("0.00"), total, None, "advance → selected bank binding")
        else: add(bank_ledger, total, Decimal("0.00"), None, "deposit fact → selected bank binding"); add(ledger, Decimal("0.00"), total, None, "deposit fact → deposit liability")
    if sum(x.debit for x in lines) != sum(x.credit for x in lines): raise ValidationError("Derived journal is unbalanced")
    return DerivedPosting(DerivedJournalHeader(command.school_id, command.fiscal_year_id, command.accounting_date, command.workflow), tuple(lines), PinnedReferences(rule.id, tuple(dict.fromkeys(annexes)), tuple(dict.fromkeys(used_definitions)), tuple(dict.fromkeys(used_ledgers)), binding.id))
