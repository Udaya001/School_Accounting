# Working Guidelines

## Source of truth

- `docs/reference/school guidelines.pdf` is the authoritative School Accounting Manual 2076.
- Capture applicable manual requirements in `docs/REQUIREMENTS.md` as they are verified.
- Prefer `docs/REQUIREMENTS.md` for routine work. Reopen the PDF only when exact wording, interpretation, or verification is needed.

## Delivery standards

- Aim for guideline completeness: implemented behavior and documentation must cover every applicable, verified requirement.
- Design for non-technical school staff. Keep workflows, labels, and error messages simple and clear.
- Preserve auditability. Financial records must retain appropriate history, attribution, dates, and traceable changes; do not silently overwrite meaningful data.
- Keep changes small and scoped to the requested outcome.
- Do not make unrelated refactors or formatting churn.
- Add and maintain tests for implemented logic, proportionate to the change.

## Documentation practice

- Record product intent in `docs/PRODUCT.md`, verified obligations in `docs/REQUIREMENTS.md`, consequential choices in `docs/DECISIONS.md`, and planned work in `docs/ROADMAP.md`.
- Mark assumptions and unverified interpretations explicitly; do not present them as manual requirements.
