# Candidate Pool Package Input Validation

## Required inputs

- Require a nonblank target Pool name and a nonblank target process code. The target code must differ from the selected source Pool process code.
- Require one selected source `ORA_IRC_LC` row with `TypeCode=POOL` in a fresh unscoped export.
- Require the requested Pool phase and state-routing set to resolve to exactly one source-backed reusable Pool routing relationship.
- Treat requested state routes as source-backed inputs. Do not create custom state-definition rows unless the selected Pool profile explicitly supports state creation.

## Task nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---:|---|---|---|---|---|
| POOL.VALIDATE_INPUTS | decision | 10 | validate_input | valid->POOL.EXPORT_BASELINE;invalid->POOL.HANDLE_ISSUES | none | stop | Every Pool create-package request |
